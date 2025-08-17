# Panduan Lengkap FastAPI untuk Pemula

FastAPI adalah framework web modern dan cepat untuk membangun API dengan Python. Framework ini dikembangkan oleh Sebastian Ramirez dan telah menjadi pilihan populer untuk pengembangan API karena performanya yang tinggi dan kemudahan penggunaan.

## Mengapa Memilih FastAPI?

1. **Performa Tinggi**: FastAPI adalah salah satu framework Python tercepat, sebanding dengan NodeJS dan Go
2. **Type Hints**: Memanfaatkan type hints Python untuk validasi otomatis
3. **Auto Documentation**: Menghasilkan dokumentasi API secara otomatis dengan Swagger UI
4. **Async Support**: Dukungan penuh untuk async/await
5. **Easy to Learn**: Sintaks yang mudah dipahami dan dipelajari

## Instalasi FastAPI

```bash
pip install fastapi uvicorn[standard]
```

## Contoh Aplikasi Sederhana

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

## Menjalankan Aplikasi

```bash
uvicorn main:app --reload
```

## Fitur-Fitur Utama

### 1. Path Parameters
FastAPI memungkinkan Anda mendefinisikan parameter dalam URL path:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### 2. Query Parameters
Parameter query dapat didefinisikan sebagai parameter fungsi:

```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

### 3. Request Body
Menggunakan Pydantic models untuk validasi request body:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
def create_item(item: Item):
    return item
```

### 4. Response Models
Mendefinisikan model untuk response:

```python
class ItemResponse(BaseModel):
    name: str
    price: float

@app.post("/items/", response_model=ItemResponse)
def create_item(item: Item):
    return item
```

## Best Practices

1. **Gunakan Pydantic Models**: Selalu gunakan Pydantic untuk validasi data
2. **Type Hints**: Manfaatkan type hints untuk dokumentasi otomatis
3. **Error Handling**: Implementasikan error handling yang proper
4. **Dependency Injection**: Gunakan sistem dependency FastAPI
5. **Testing**: Tulis unit test untuk semua endpoint

## Tips Pengembangan

- Gunakan `--reload` flag saat development
- Akses dokumentasi otomatis di `/docs`
- Manfaatkan fitur async untuk operasi I/O
- Gunakan middleware untuk cross-cutting concerns
- Implementasikan logging yang baik

FastAPI sangat cocok untuk pengembangan microservices, API RESTful, dan aplikasi backend modern. Dengan dokumentasi yang lengkap dan komunitas yang aktif, FastAPI adalah pilihan yang tepat untuk proyek Python Anda.
