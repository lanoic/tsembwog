# Tsembwog Energy Platform (Frontend)

This is the production-ready frontend for the Tsembwog energy aggregation platform.

---

## 🚀 Features

- 🌙 Dark Mode toggle
- 🌍 Multilingual support (i18n-ready)
- 📡 Live API integration (REACT_APP_API_URL)
- 📊 Charts & analytics for REGO certificates
- 🔔 WebSocket real-time alerts
- 🧑‍💼 Admin dashboard routes
- ✉️ CRM-ready email capture (Mailchimp)

---

## 🛠 Local Development

```bash
cd frontend
npm install
npm start
```

### Build for Production

```bash
npm run build
```

---

## 🌐 Deployment (Netlify)

### Build Settings

- **Build Command**: `npm run build`
- **Publish Directory**: `frontend/build`

### Environment Variables

Set these in Netlify or `.env`:

```env
REACT_APP_API_URL=https://your-backend.onrender.com
REACT_APP_SOCKET_URL=wss://your-backend.onrender.com/ws
REACT_APP_MAILCHIMP_URL=https://<your-datacenter>.api.mailchimp.com/3.0/lists/<list-id>/members
REACT_APP_MAILCHIMP_API_KEY=your-mailchimp-api-key
```

---

## 🧪 Testing Websocket & API

Ensure your backend exposes:
- `/ws/alerts` for WebSocket
- `/api/certificates`, `/api/users`, etc. for analytics & dashboard

---

## 📁 Folder Structure

```
frontend/
├── src/
│   ├── pages/
│   ├── components/
│   ├── i18n/
│   ├── App.js
│   └── index.js
```

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch
3. Push changes & open PR

---

## 📧 Contact

For support: hello@tsembwog.com