# SoundVault

**Premium royalty-free sample library for music creators.**

SoundVault gives producers instant access to 500,000+ high-quality samples across every genre — from trap 808s to ambient pads. Drop in a sample, analyze its BPM and key, then find matching sounds in seconds.

---

## Tech Stack

![Vue 3](https://img.shields.io/badge/Vue-3.x-4FC08D?logo=vue.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57?logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS_3-06B6D4?logo=tailwindcss&logoColor=white)

---

## Features

- **Sample Browser** — Search and filter 60+ seed samples by genre, BPM range, key, and type. Live filter updates with 300ms debounce.
- **Pack System** — Samples organized into 10 themed packs with beautiful gradient cover art.
- **Audio Preview** — Click any sample to preview it via the Web Audio API (oscillator tone mapped to sample key). Global persistent player bar with prev/next/volume controls.
- **Audio Analyzer** — Upload any audio file (MP3, WAV, FLAC, OGG, M4A) and instantly detect BPM, key, and duration using librosa.
- **Deep Linking** — Analyze page "Find samples in this key" navigates directly to `/sounds?key=X`.
- **Pricing Plans** — Free / Creator / Pro tiers with monthly/annual toggle.
- **Dark Premium UI** — Custom design system with DM Serif Display, DM Sans, JetBrains Mono fonts.

---

## Local Development

### Prerequisites
- Node.js 20+
- Python 3.11+
- pip

### Backend

```bash
cd backend/app
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. On first run, the database is automatically seeded with 10 packs and 60 samples.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The dev server starts at `http://localhost:5173`. API calls to `/api/*` are proxied to `http://localhost:8000` via Vite's dev proxy.

---

## Docker Setup

Build and run the entire stack with one command:

```bash
docker-compose up --build
```

Then open **http://localhost:5173** in your browser.

- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:5173`

The frontend Docker container serves through nginx, which proxies `/api` requests to the backend service internally.

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check — returns `{"status": "ok"}` |
| `GET` | `/api/packs` | List all packs |
| `GET` | `/api/samples` | List samples with filtering & pagination |
| `GET` | `/api/samples/{id}` | Get a single sample by ID |
| `POST` | `/api/samples/{id}/play` | Increment play count for a sample |
| `POST` | `/api/analyze` | Analyze an uploaded audio file |

### Sample Query Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `q` | string | — | Search term (filename, pack name, genre) |
| `genre` | string | — | Filter by genre |
| `bpm_min` | float | 0 | Minimum BPM |
| `bpm_max` | float | 300 | Maximum BPM |
| `key` | string | — | Musical key (e.g. `Am`, `F#`) |
| `sample_type` | string | — | `loop`, `one_shot`, `vocal`, `fx` |
| `pack_id` | int | — | Filter by pack |
| `sort` | string | `trending` | `trending`, `newest`, `bpm_asc`, `bpm_desc` |
| `limit` | int | 20 | Pagination limit |
| `offset` | int | 0 | Pagination offset |

---

## Architecture Decisions

### SQLite for demo simplicity
SQLite requires zero infrastructure setup — the database file lives alongside the app at `/app/soundvault.db`. For production, swap to PostgreSQL by updating the SQLAlchemy connection string in `database/db.py`.

### Pinia for global audio player state
The audio player is a singleton that persists across route changes. Pinia's `defineStore` pattern makes it trivial to share `currentSample`, `isPlaying`, and `queue` state between the SoundsView sample list, the floating AudioPlayer bar, and the SamplePreviewStrip on the landing page.

### Web Audio API for simulated previews
Rather than requiring actual audio file hosting infrastructure, SoundVault uses the browser's Web Audio API to generate a synthesized tone that represents each sample. The oscillator frequency is mapped from the sample's key (A=440Hz, etc.), the waveform type matches sample type (sine for loops, triangle for one-shots/vocals/fx), and the gain envelope applies a 100ms attack and 300ms release for a natural feel.

### Vue Router for deep-linking from Analyze to Sounds
The Analyze page's "Find samples in this key" button uses `router.push({ path: '/sounds', query: { key: result.key } })`. SoundsView reads `route.query.key` on mount and applies it to the filter state, enabling seamless cross-page navigation without needing a global filter store.

---

## Project Structure

```
sound-vault/
├── docker-compose.yml
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── database/
│       │   ├── db.py
│       │   └── seed.py
│       ├── models/
│       │   └── schemas.py
│       └── routers/
│           ├── packs.py
│           ├── samples.py
│           └── analyze.py
└── frontend/
    ├── Dockerfile
    ├── nginx.conf
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.js
    ├── index.html
    └── src/
        ├── App.vue
        ├── main.ts
        ├── style.css
        ├── types/index.ts
        ├── router/index.ts
        ├── stores/playerStore.ts
        ├── composables/
        │   ├── useSamples.ts
        │   └── useAudioAnalysis.ts
        ├── components/
        │   ├── layout/
        │   │   ├── Navbar.vue
        │   │   └── Footer.vue
        │   ├── landing/
        │   │   ├── HeroSection.vue
        │   │   ├── SamplePreviewStrip.vue
        │   │   ├── FeaturesSection.vue
        │   │   └── PricingCards.vue
        │   ├── sounds/
        │   │   ├── FilterBar.vue
        │   │   ├── PackCard.vue
        │   │   ├── WaveformBar.vue
        │   │   ├── SampleRow.vue
        │   │   └── AudioPlayer.vue
        │   └── analyze/
        │       ├── DropZone.vue
        │       └── ResultCard.vue
        └── views/
            ├── HomeView.vue
            ├── SoundsView.vue
            ├── PlansView.vue
            └── AnalyzeView.vue
```

---

## Production Roadmap

- **Real audio hosting** — Replace Web Audio API tone generation with actual S3-hosted audio files. Add a streaming endpoint or signed S3 URLs for secure delivery.
- **Stripe payments** — Integrate Stripe Checkout for Creator/Pro plan subscriptions. Webhook handler to update user plan in the database on successful payment.
- **JWT authentication** — Add FastAPI-Users or a custom JWT auth flow. Protect download endpoints behind plan-tier middleware.
- **PostgreSQL** — Swap SQLite for PostgreSQL for production workloads. Add Alembic for schema migrations.
- **Elasticsearch** — Replace SQLAlchemy ILIKE search with Elasticsearch for full-text search, typo tolerance, and faceted filtering at scale.
- **CDN & caching** — Put CloudFront in front of S3 assets. Cache API responses with Redis.
- **Waveform visualization** — Pre-generate waveform images (e.g. with audiowaveform) and store alongside audio files for rich visual previews.
