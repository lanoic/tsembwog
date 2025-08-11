# tsembwog
Run: `docker compose up --build`
Backend: http://localhost:8000/docs
Frontend: http://localhost:3000

---
## CI/CD

### Backend (Docker Hub + optional Render)
- Set repo **Secrets**:
  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`
  - Optional: `RENDER_DEPLOY_HOOK` (Render build hook URL)
- Push to `main`/`master` → builds Docker image `tsembwog-backend:latest`
- If `RENDER_DEPLOY_HOOK` is set, Render redeploys automatically

### Frontend (Netlify)
- Set repo **Secrets**:
  - `NETLIFY_AUTH_TOKEN` (User > Applications > New access token)
  - `NETLIFY_SITE_ID` (Site settings > Site information)
  - `REACT_APP_API_URL`, `REACT_APP_SOCKET_URL`, `REACT_APP_MAILCHIMP_URL` as needed
- Push to `main`/`master` → builds `/frontend` and deploys to Netlify

## Monitoring (Prometheus + Grafana)
Launch alongside your stack:

```bash
docker compose up --build -d
docker compose -f docker-compose.monitoring.yml up -d
```

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (user: admin / pass: admin)
- Add Prometheus data source at `http://prometheus:9090`
- Import a basic dashboard and add panels for:
  - `tsembwog_requests_total`
  - `tsembwog_model_trains_total`
  - `histogram_quantile(0.95, sum(rate(tsembwog_rego_predict_seconds_bucket[5m])) by (le))`


---
## Disruptor Additions
- S3-backed model artifact storage (fallback to local) via env: `USE_S3`, `S3_BUCKET`, `MODEL_DIR`
- Train-now endpoint: `POST /admin/train-now` (admin only)
- API keys issuing & service protection (`/keys/issue`, `/keys/mine`, `/keys/service/ping` with `x-api-key`)
- Organizations and roles (admin/member) with seeded org
- Audit logging middleware to `/app/logs/audit.log`
- Simple built-in rate limiter (100 req/min per IP, configurable by editing middleware)
- Sentry DSN support (set `SENTRY_DSN` to enable)
- PWA: manifest + service worker
- Netlify `_headers` for strong security and CDN caching
- Grafana dashboard JSON sample in `monitoring/grafana_dashboards/`


---
## One-liners

### Push repo and enable CI
```bash
git add .
git commit -m "chore: add render.yaml, netlify.toml, CI workflows, scripts"
git push origin main
```

### Set GitHub secrets (requires GitHub CLI)
```bash
./scripts/gh_secrets.sh lanoic tsembwog
# Then set actual values:
gh secret set NETLIFY_AUTH_TOKEN --repo lanoic/tsembwog --body "<token>"
gh secret set NETLIFY_SITE_ID --repo lanoic/tsembwog --body "<site-id>"
gh secret set DOCKERHUB_USERNAME --repo lanoic/tsembwog --body "your-dockerhub-user"
gh secret set DOCKERHUB_TOKEN --repo lanoic/tsembwog --body "<dockerhub-access-token>"
# Optional Render build hook for auto-redeploy after image push:
gh secret set RENDER_DEPLOY_HOOK --repo lanoic/tsembwog --body "https://api.render.com/deploy/srv-..."
# Frontend env:
gh secret set REACT_APP_API_URL --repo lanoic/tsembwog --body "https://<render-backend>"
gh secret set REACT_APP_SOCKET_URL --repo lanoic/tsembwog --body "wss://<render-backend>/ws/alerts"
```

### Render (Blueprint deploy)
- Connect repo → deploy `render.yaml`. After first deploy, set `SECRET_KEY` & (optional) S3 and Sentry values in service env.

### Netlify
- Connect repo → `netlify.toml` auto-configures build. Add env variables as above.

```)


---
## Admin Console
- **Users**: role edit (`member`, `operator`, `analyst`, `admin`)
- **Orgs**: list/create
- **Ops**: enqueue model retraining (Celery), admin-only

## Migrations
- Pre-generated revision `0002_models_init.py` included; run `alembic upgrade head`.

## Queue
- `POST /queue/train-now` enqueues retraining task (`tasks.retrain_rego_model_task`).
- Bring up Celery with: `docker compose -f docker-compose.celery.yml up -d`.
