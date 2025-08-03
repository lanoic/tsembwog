
# tsembwog: Energy Aggregation Platform

`tsembwog` is a full-stack platform designed for renewable energy aggregation including:
- REGO/GO Certificate Trading
- Demand-Side Response (DSR) Aggregation
- Behind-the-Meter (BTM) Solar + Storage Optimization

## 📦 Project Structure
```
tsembwog/
├── backend/       # FastAPI app with PostgreSQL + JWT auth
├── frontend/      # React frontend with expanded UI and auth
├── docker-compose.yml
├── .env
└── README.md
```

---

## 🚀 Local Development

### Prerequisites
- Docker + Docker Compose
- Node.js (for frontend)

### Backend
```bash
docker-compose up --build
```

### Frontend
```bash
cd frontend
npm install
npm start
```

---

## 🔐 Authentication

- JWT-based auth in FastAPI
- Login/Register screens in React
- Token is stored in `localStorage` and used with Axios

---

## 🌐 Cloud Deployment

### Render.com (Recommended)

1. Push your code to GitHub.
2. Create a PostgreSQL DB using Render's Database service.
3. Create a new Web Service for the backend:
   - Environment:
     - `DATABASE_URL` from DB settings
     - `SECRET_KEY` = your-random-secret
   - Start command: `uvicorn main:app --host 0.0.0.0 --port 8000`
4. Deploy the React frontend to Vercel or Netlify:
   - Set `REACT_APP_API_URL` to your backend URL

### GCP / Railway / Heroku

You can use Docker and Postgres on any platform that supports containers.

---

## 📊 Admin Dashboard (Planned Features)

- User & Certificate Management
- DSR Event Logs & Analytics
- BTM Energy Flow Charts
- Notifications and Audit Logs

---

## ✅ CI/CD (Optional)

### GitHub Actions Example
```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      - name: Login to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          push: true
          tags: yourdockerhubuser/tsembwog:latest
```

---

## 🤝 Contributing

We welcome contributions! Feel free to fork and submit PRs for features or bugfixes.

---

## 📧 Contact

For questions, reach out to the project maintainer or open a GitHub issue.

---


---

## ☁️ One-Click Deploy

### Backend (Render)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Frontend (Netlify)

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start)

---
