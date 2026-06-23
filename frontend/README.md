# Frontend – URL-Shortener

Single-Page-Anwendung zum Verwalten der eigenen Kurzlinks und ihrer Klick-Statistik.
Sie nutzt die REST-API aus dem Hauptprojekt.

**Stack:** Vue 3 (`<script setup>`, Composition API) · Vite · TypeScript · Pinia ·
Vue Router · Tailwind CSS · Vitest.

## Einrichtung

```sh
npm install
```

Die API-Basis-URL lässt sich über `VITE_API_BASE_URL` setzen
(Standard: `http://localhost:8000`). Das Backend muss laufen und die Frontend-Herkunft
per CORS erlauben (bereits konfiguriert für `http://localhost:5173`).

## Skripte

```sh
npm run dev          # Entwicklungsserver (http://localhost:5173)
npm run build        # Type-Check + Produktions-Build
npm run test         # Unit-/Store-Tests (Vitest)
npm run lint         # ESLint
npm run type-check   # vue-tsc
```

## Struktur

| Pfad | Aufgabe |
|---|---|
| `src/api/client.ts` | Fetch-Client mit Bearer-Token und Fehlerbehandlung |
| `src/stores/auth.ts` | Pinia-Store: Login, Registrierung, Logout, Token-Persistenz |
| `src/router/index.ts` | Routen inkl. Auth-Guard |
| `src/views/LoginView.vue` | Anmeldung und Registrierung |
| `src/views/DashboardView.vue` | Kurzlinks anlegen, auflisten, kopieren, löschen |
| `src/views/StatsView.vue` | Klick-Statistik (gesamt und pro Tag) |
