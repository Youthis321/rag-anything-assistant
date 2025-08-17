# Perbedaan Frontend dan Backend

## 1. Definisi
- **Frontend**  
  Bagian dari aplikasi atau website yang **berhubungan langsung dengan pengguna (User Interface)**.  
  Segala sesuatu yang dilihat, diklik, atau diinteraksi user berada di frontend.  

- **Backend**  
  Bagian dari aplikasi atau website yang berjalan di **server**.  
  Bertanggung jawab pada **logika bisnis, database, autentikasi, dan komunikasi data** ke frontend.  

---

## 2. Tugas Utama
- **Frontend**
  - Menyajikan tampilan UI/UX (chat, tombol, tabel, grafik).
  - Mengatur interaksi pengguna dengan aplikasi.
  - Mengambil/mengirim data dari/ke backend melalui API.

- **Backend**
  - Menyimpan dan mengolah data di database.
  - Menangani request dari frontend.
  - Menyediakan API/endpoint untuk komunikasi data.
  - Menjaga keamanan (autentikasi, otorisasi).

---

## 3. Teknologi Umum
- **Frontend**
  - HTML, CSS, JavaScript
  - Framework: React, Vue, Angular, Svelte, Next.js, Nuxt.js, SvelteKit
  - Tools UI: Tailwind, Bootstrap, shadcn/ui

- **Backend**
  - Bahasa: Python, Java, PHP, Node.js, Go, Ruby
  - Framework: Django, Flask, FastAPI, Laravel, Express.js, Spring Boot
  - Database: MySQL, PostgreSQL, MongoDB, Redis
  - API: REST, GraphQL, gRPC

---

## 4. Contoh Peran dalam Aplikasi Chat (RAG-Anything)
- **Frontend**
  - Menampilkan chat UI (input pertanyaan, bubble jawaban).
  - Dashboard jumlah artikel, project, dan history.
  - Viewer history chat berdasarkan tanggal.

- **Backend**
  - Menyimpan semua percakapan ke database.
  - Mengambil artikel dari `data-artikel` dan project dari `data-clone-github`.
  - Menjalankan proses **RAG (Retrieval Augmented Generation)** untuk menjawab pertanyaan.
  - Menyediakan API untuk frontend.

---

## 5. Kesimpulan
- **Frontend = Wajah aplikasi** (apa yang dilihat & digunakan user).  
- **Backend = Otak aplikasi** (proses di belakang layar yang mengatur data & logika).  

Keduanya saling melengkapi → frontend tidak bisa jalan tanpa backend, begitu juga sebaliknya.
