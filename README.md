# diacare-chatbot-api

Chatbot kesehatan (diabetes melitus tipe 2) berbasis RAG — menjawab berdasarkan pedoman PNPK/Kemenkes.

## Perintah

| Perintah | Fungsi |
|---|---|
| `uvicorn main:app --reload` | Jalankan API — buka `http://127.0.0.1:8000/docs` (Swagger) |
| `python cli.py` | Jalankan chatbot di terminal (ketik `exit` untuk keluar) |
| `python -m rag.pipeline` | Bangun ulang index `.chroma/` — jalankan setelah menambah/mengganti PDF atau mengubah chunk size/model embedding |
| `python -m pytest tests/ -v` | Jalankan test — pastikan retrieval & jawaban masih berfungsi setelah ubah kode |

- Endpoint API: `POST /chat` dengan body `{"question": "..."}`, balasan berupa record `user` dan `chatbot` (masing-masing berisi `sender`, `message`, `timestamp`).

## Catatan

- Index vector disimpan di `.chroma/` (di-gitignore); dibangun otomatis saat pertama kali dijalankan, lalu dimuat dari disk.
- Konfigurasi (model, prompt, chunk) di `rag/config.py`.
- Satu pintu masuk RAG untuk kode lain: `from rag.service import answer` lalu `answer("pertanyaan")`; `request_chatbot(query)` dipakai untuk record lengkap user + chatbot.
- Struktur API: `main.py` (entry FastAPI) → `api/routes.py` (endpoint) → `api/schemas.py` (model request/response); `cli.py` untuk mode terminal.
