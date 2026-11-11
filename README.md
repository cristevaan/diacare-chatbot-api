# diacare-chatbot-api

Chatbot kesehatan (diabetes melitus tipe 2) berbasis RAG — menjawab berdasarkan pedoman PNPK/Kemenkes.

## Perintah

| Perintah | Fungsi |
|---|---|
| `python main.py` | Jalankan chatbot di terminal (ketik `exit` untuk keluar) |
| `python -m rag.pipeline` | Bangun ulang index `.chroma/` — jalankan setelah menambah/mengganti PDF atau mengubah chunk size/model embedding |
| `python -m pytest tests/ -v` | Jalankan test — pastikan retrieval & jawaban masih berfungsi setelah ubah kode |

## Catatan

- Index vector disimpan di `.chroma/` (di-gitignore); dibangun otomatis saat pertama kali dijalankan, lalu dimuat dari disk.
- Konfigurasi (model, prompt, chunk) di `rag/config.py`.
- Satu pintu masuk RAG untuk kode lain: `from rag.service import answer` lalu `answer("pertanyaan")`.
