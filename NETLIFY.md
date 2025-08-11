# Netlify setup

1. Create/import the site from GitHub (repo root includes `netlify.toml`).
2. In Netlify → **Site settings → Environment variables**, add:
   - `REACT_APP_API_URL` = `https://<your-render-backend>`
   - `REACT_APP_SOCKET_URL` = `wss://<your-render-backend>/ws/alerts`
   - (Optional) `REACT_APP_MAILCHIMP_URL`
3. Deploy. Point your domain to Netlify (CNAME `www` → `your-site.netlify.app`, A for root to Netlify IPs).
