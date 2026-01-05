# OCEGS Frontend (Vue 3)

This is the Vue 3 frontend for OCEGS - Online Consultation and Emergency Guidance System.

## Quick Start

```bash
cd frontend/vue-app

# Install dependencies
pnpm install
# or
npm install

# Start development server
pnpm dev
# or
npm run dev
```

Open http://localhost:5173 in your browser.

## Project Structure

```
src/
├── main.js           # App entry
├── App.vue           # Root component
├── router/           # Vue Router
├── api/              # HTTP client
├── stores/           # Pinia stores (Step 2+)
├── views/            # Page components
│   ├── HomeView.vue
│   └── ConsultationView.vue
├── components/       # Reusable components (Step 2+)
└── assets/           # Styles & static files
```

## Backend Integration

The Vite dev server proxies `/api/*` requests to `http://localhost:8000`.

Make sure the backend is running:
```bash
cd backend
uvicorn app.main:app --reload
```

## Design Reference

The `../` directory contains a static HTML/CSS/JS prototype that served as design inspiration for the consultation page styling.
