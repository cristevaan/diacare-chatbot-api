# diacare-chatbot-api

Chatbot kesehatan (diabetes melitus tipe 2) berbasis RAG — menjawab berdasarkan pedoman PNPK/Kemenkes.

## Setup

- Salin template env lalu isi API key-nya: `cp .env.example .env`
- `.env` berisi `GROQ_API_KEY` dan tidak ikut ke git (sudah masuk `.gitignore`).

## Perintah

| Perintah | Fungsi |
|---|---|
| `uvicorn main:app --reload` | Jalankan API — buka `http://127.0.0.1:8000/docs` (Swagger) |
| `python cli.py` | Jalankan chatbot di terminal (ketik `exit` untuk keluar) |
| `python -m rag.pipeline` | Bangun ulang index `.chroma/` — jalankan setelah menambah/mengganti PDF atau mengubah chunk size/model embedding |
| `python -m pytest tests/ -v` | Jalankan test — pastikan retrieval & jawaban masih berfungsi setelah ubah kode |

- Endpoint API: `POST /chat` dengan body `{"question": "..."}`, balasan berupa record `user` dan `chatbot` (masing-masing berisi `sender`, `message`, `timestamp`).

## Docker

| Perintah | Fungsi |
|---|---|
| `docker build -t diacare .` | Build image — index `.chroma` dan model embedding dibangun di dalam image (butuh jaringan saat build) |
| `docker run --rm -e GROQ_API_KEY=... -p 8000:8000 diacare` | Jalankan container — index sudah siap sejak startup, `/chat` langsung cepat |
| `docker pull <username>/diacare-chatbot-api:latest` | Ambil image hasil CI dari Docker Hub |
| `docker compose up -d` | Jalankan via `docker-compose.yml` — baca `.env` otomatis, `restart: unless-stopped` |
| `docker compose pull && docker compose up -d` | Update container ke image terbaru dari Docker Hub |
| `docker compose logs -f` | Pantau log realtime |

- Setiap push ke `main`, GitHub Actions (`.github/workflows/docker-hub.yml`) mem-build image lalu push ke Docker Hub — butuh secret `DOCKERHUB_USERNAME` dan `DOCKERHUB_TOKEN` di repo GitHub (Settings → Secrets and variables → Actions).
- `.env` tidak ikut ke image; `GROQ_API_KEY` cukup di-pass saat runtime.
- Deploy di VPS: upload `docker-compose.yml` + `.env`, lalu `docker compose up -d`. Update image cukup `docker compose pull && docker compose up -d` — tidak perlu build ulang.

## Catatan

- Index vector disimpan di `.chroma/` (di-gitignore); dibangun saat startup server bila belum ada, lalu dimuat dari disk.
- Konfigurasi (model, prompt, chunk) di `rag/config.py`.
- Satu pintu masuk RAG untuk kode lain: `from rag.service import answer` lalu `answer("pertanyaan")`; `request_chatbot(query)` dipakai untuk record lengkap user + chatbot.
- Struktur API: `main.py` (entry FastAPI) → `api/routes.py` (endpoint) → `api/schemas.py` (model request/response); `cli.py` untuk mode terminal.
