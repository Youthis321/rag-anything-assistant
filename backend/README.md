# RAG Anything Assistant - Backend

Backend API untuk RAG (Retrieval-Augmented Generation) Assistant menggunakan FastAPI dan Gemini Pro API.

## Features

- **Knowledge Base Management**: Membaca dan mengelola data dari `data-artikel` dan `data-clone-github`
- **Gemini Pro Integration**: Mengintegrasikan dengan Google Gemini Pro API untuk generasi response
- **Chat History**: Menyimpan dan mengambil riwayat percakapan
- **Statistics**: Menyediakan statistik jumlah artikel, project, dan percakapan

## API Endpoints

### 1. Chat Endpoint
```
POST /chat
```
**Request Body:**
```json
{
  "question": "Pertanyaan Anda"
}
```

**Response:**
```json
{
  "answer": "Jawaban dari AI",
  "timestamp": "2025-08-17T10:30:00.000Z",
  "sources": ["source1.txt", "GitHub: project-name"]
}
```

### 2. History Endpoint
```
GET /history/{tanggal}
```
**Parameter:**
- `tanggal`: Format YYYY-MM-DD (contoh: 2025-08-17)

**Response:**
```json
{
  "date": "2025-08-17",
  "conversations": [
    {
      "id": "20250817_103000",
      "timestamp": "2025-08-17T10:30:00.000Z",
      "question": "Pertanyaan",
      "answer": "Jawaban",
      "sources": []
    }
  ]
}
```

### 3. Statistics Endpoint
```
GET /stats
```

**Response:**
```json
{
  "total_articles": 10,
  "total_projects": 5,
  "total_conversations": 25,
  "last_updated": "2025-08-17T10:30:00.000Z"
}
```

### 4. Health Check
```
GET /health
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Environment Variables

1. Copy `.env` file dan edit dengan API key Anda:
```bash
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

2. Untuk mendapatkan Gemini API key:
   - Kunjungi [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Login dengan akun Google
   - Buat API key baru
   - Copy dan paste ke file `.env`

### 3. Setup Knowledge Base

Struktur folder yang diperlukan:
```
rag-data/
├── data-artikel/          # File artikel (.txt, .md, .json)
├── data-clone-github/     # Folder project GitHub yang sudah di-clone
└── data-history/          # History chat (otomatis dibuat)
```

**Menambah artikel:**
- Letakkan file artikel (.txt, .md, .json) di folder `rag-data/data-artikel/`
- Bisa dalam subfolder

**Menambah GitHub projects:**
- Clone repository ke folder `rag-data/data-clone-github/`
- Contoh: `git clone https://github.com/user/repo.git rag-data/data-clone-github/repo`

### 4. Run the Application

```bash
python app.py
```

Atau menggunakan uvicorn:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Server akan berjalan di: `http://localhost:8000`

### 5. Test API

Buka browser ke `http://localhost:8000/docs` untuk mengakses Swagger UI dan test API endpoints.

## Project Structure

```
backend/
├── app.py                 # Entry point FastAPI
├── services/
│   ├── rag_service.py     # Logic retrieval dari knowledge base
│   ├── gemini_service.py  # Koneksi ke Gemini API
│   └── history_service.py # Simpan & ambil chat history
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

## Troubleshooting

### Error: GEMINI_API_KEY tidak ditemukan
- Pastikan file `.env` ada dan berisi `GEMINI_API_KEY=your_key`
- Pastikan API key valid dan aktif

### Error: Knowledge base kosong
- Pastikan folder `rag-data/data-artikel/` dan `rag-data/data-clone-github/` berisi data
- Periksa permission folder

### Error: Import tidak ditemukan
- Jalankan `pip install -r requirements.txt`
- Pastikan menggunakan Python virtual environment

## Development

Untuk development mode dengan auto-reload:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

1. Set environment variable `APP_ENV=production`
2. Update `ALLOWED_ORIGINS` di `.env` dengan domain frontend yang sebenarnya
3. Gunakan server production seperti Gunicorn:
```bash
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
