from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.rag_service import RAGService
from services.gemini_service import GeminiService
from services.history_service import HistoryService

app = FastAPI(
    title="RAG Anything Assistant API",
    description="Backend API untuk RAG Assistant dengan integrasi Gemini Pro",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
rag_service = RAGService()
gemini_service = GeminiService()
history_service = HistoryService()

# Pydantic models
class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    timestamp: str
    sources: list = []

@app.get("/")
async def root():
    """Root endpoint untuk cek status API"""
    return {
        "message": "RAG Anything Assistant API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint utama untuk chat dengan RAG system
    """
    try:
        # Ambil context dari knowledge base
        context = rag_service.retrieve_context(request.question)
        
        # Generate response menggunakan Gemini
        answer = await gemini_service.generate_response(
            question=request.question,
            context=context
        )
        
        # Simpan ke history
        timestamp = datetime.now().isoformat()
        history_service.save_chat(
            question=request.question,
            answer=answer,
            timestamp=timestamp,
            sources=context.get("sources", [])
        )
        
        return ChatResponse(
            answer=answer,
            timestamp=timestamp,
            sources=context.get("sources", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/history/{tanggal}")
async def get_history(tanggal: str):
    """
    Ambil history chat berdasarkan tanggal (format: YYYY-MM-DD)
    """
    try:
        history = history_service.get_history_by_date(tanggal)
        return {
            "date": tanggal,
            "conversations": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@app.get("/stats")
async def get_stats():
    """
    Ambil statistik: jumlah artikel, project, dan history
    """
    try:
        stats = {
            "total_articles": rag_service.count_articles(),
            "total_projects": rag_service.count_projects(),
            "total_conversations": history_service.count_total_conversations(),
            "last_updated": datetime.now().isoformat()
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "rag_service": "operational",
            "gemini_service": "operational",
            "history_service": "operational"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
