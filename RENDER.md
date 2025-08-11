# Render setup

1. In **Render**, click "Blueprints" → "New Blueprint" and connect your GitHub repo.
2. Select `render.yaml` and deploy.
3. After deploy:
   - In the **tsembwog-backend** service → **Environment**:
     - Set `SECRET_KEY` to a long random string
     - (Optional) Set `USE_S3=true`, `S3_BUCKET=<your-bucket>`, `S3_PREFIX=models/`
     - (Optional) Set `SENTRY_DSN=<dsn>`
4. Verify Disk mount at `/data` exists; models persist at `/data/models`.
5. Copy the backend public URL (e.g. `https://tsembwog-backend.onrender.com`) and set it in Netlify as `REACT_APP_API_URL` and `REACT_APP_SOCKET_URL` (`wss://.../ws/alerts`).
