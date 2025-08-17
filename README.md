# RAG Anything Assistant

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Node 18+](https://img.shields.io/badge/Node-18%2B-green)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Proyek ini adalah implementasi RAG (Retrieval-Augmented Generation) Assistant sederhana yang terdiri dari backend (FastAPI) dan frontend (Svelte + Vite). Backend mengambil data dari koleksi dokumen lokal (artikel dan salinan repository GitHub) untuk menambahkan konteks saat menghasilkan jawaban lewat model (integrasi dengan Gemini Pro pada contoh ini). Frontend menyediakan antarmuka chat, dashboard metrik, dan viewer riwayat percakapan.

## Ringkasan isi repository

- `backend/` – API server (FastAPI)
  - `app.py` – entry point FastAPI
  - `services/` – logika RAG, koneksi ke Gemini, penyimpanan history
  - `requirements.txt` – dependensi Python
  - `start.bat` – contoh skrip start untuk Windows
  - `test_api.py` – tes ringan untuk endpoint
- `frontend/` – aplikasi Svelte + Vite
  - `src/` – sumber aplikasi (komponen, store, API client)
  - `package.json` – dependensi & script npm
- `rag-data/` – data knowledge base dan history
  - `data-artikel/` – artikel (.md/.txt/.json) untuk retrieval
  - `data-clone-github/` – salinan project GitHub untuk indexing
  - `data-history/` – riwayat chat (automatis ditulis oleh backend)

## Fitur utama

- Retrieval dari koleksi dokumen lokal untuk menjawab pertanyaan (RAG)
- Integrasi contoh ke Gemini Pro (via service di `backend/services/gemini_service.py`)
- Penyimpanan riwayat percakapan per-tanggal
- Frontend chat dengan attribution (source) dan dashboard metrik

## Prasyarat

- Python 3.10+ (disarankan digunakan virtual environment)
- Node.js 18+ dan npm
- (Opsional) Akun & API key Google Gemini Pro jika memakai integrasi model

## Setup & Menjalankan

Catatan: langkah di bawah disusun untuk Windows PowerShell. Sesuaikan bila menggunakan shell lain atau container.

1) Backend

- Masuk ke folder backend:

```powershell
cd c:\laragon\www\rag-anything-assistant\backend
```

- Buat dan aktifkan virtual environment (opsional tapi disarankan):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- Install dependensi:

```powershell
pip install -r requirements.txt
```

- Siapkan environment variables: buat file `.env` (di `backend/`) dan tambahkan minimal:

```
GEMINI_API_KEY=your_gemini_api_key_here
APP_ENV=development
ALLOWED_ORIGINS=http://localhost:5173
```

- Pastikan folder data ada di root proyek (`rag-data/`) dan berisi `data-artikel/` atau `data-clone-github/` bila ingin menguji retrieval.

- Jalankan server (mode development):

```powershell
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

- Akses API docs: `http://localhost:8000/docs`

2) Frontend

- Masuk ke folder frontend:

```powershell
cd c:\laragon\www\rag-anything-assistant\frontend
```

- Install dependensi:

```powershell
npm install
```

- Jalankan development server:

```powershell
npm run dev
```

- Buka aplikasi di browser (default Vite): `http://localhost:5173`

## Struktur API (singkat)

- POST `/chat` – kirim objek `{ "question": "..." }`, backend melakukan retrieval + generation, mengembalikan jawaban dan daftar sumber
- GET `/history/{tanggal}` – ambil riwayat chat pada tanggal (format `YYYY-MM-DD`)
- GET `/stats` – metrik jumlah artikel, project, dan percakapan
- GET `/health` – health-check sederhana

(Lihat `backend/README.md` untuk dokumentasi endpoint lebih lengkap.)

## Kontrak sederhana

- Input: pertanyaan teks dari frontend
- Output: jawaban teks + metadata sumber dan timestamp
- Error mode: validasi body request, error 400 pada input tidak valid, 500 pada kesalahan server atau integrasi model

## Edge cases yang diantisipasi

- Knowledge base kosong — berikan pesan informatif dan fallback ke model generatif bila tersedia
- File tidak terbaca / permission issue — log error dan lanjutkan service lain
- API key tidak tersedia/invalid — nonaktifkan jalur model eksternal dan laporkan pada endpoint health

## Troubleshooting cepat

- ``GEMINI_API_KEY tidak ditemukan``: pastikan `.env` berisi kunci dan service/environment telah direstart
- ``Dependencies missing``: jalankan `pip install -r requirements.txt` di `backend/` dan `npm install` di `frontend/`
- ``Frontend tidak terhubung ke backend``: periksa `API_BASE_URL` di `frontend/src/lib/api/backend.ts` dan CORS/`ALLOWED_ORIGINS` di `.env`

## Development & Pengujian

- Backend: ada `test_api.py` untuk tes ringan. Jalankan dengan `python test_api.py` atau integrasikan ke test runner pilihan Anda.
- Frontend: gunakan `npm run dev` dan `svelte-check` untuk pemeriksaan tipe dan linting (`npm run check` disediakan di `package.json`).

## Deploy singkat (production hints)

- Backend: set `APP_ENV=production`, konfigurasikan variabel lingkungan nyata, gunakan Gunicorn + Uvicorn worker untuk deployment di Linux. Contoh:

```powershell
# di server Linux (contoh) - bukan PowerShell
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

- Frontend: build static files `npm run build` lalu layankan via static web server (Netlify, Vercel, atau Nginx)

## Kontribusi

1. Fork / clone repo
2. Jalankan backend & frontend secara lokal
3. Buat branch fitur/bugfix
4. Buka pull request dengan deskripsi perubahan

## File penting

- `backend/app.py` — titik masuk API
- `frontend/src/lib/api/backend.ts` — base URL & client request
- `rag-data/` — tempat menaruh dokumen yang akan di-retrieve

## Lisensi & Acknowledgements

Gunakan lisensi yang sesuai untuk proyek Anda (mis. MIT). Jika memakai API berbayar (Gemini Pro), perhatikan aturan penggunaan dan rate limits.

---

Jika Anda mau, saya bisa:
- Menambahkan badge status build atau contoh `.env.example` di `backend/`
- Menulis skrip Dockerfile + docker-compose untuk menjalankan frontend + backend + data secara lokal

Status: README global dibuat pada `README.md` (root).
