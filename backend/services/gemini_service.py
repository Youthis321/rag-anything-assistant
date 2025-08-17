import os
import json
import asyncio
import aiohttp
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class GeminiService:
    """
    Service untuk integrasi dengan Gemini Pro API
    """
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.session = None
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def generate_response(self, question: str, context: Dict[str, Any]) -> str:
        """
        Generate response menggunakan Gemini Pro API dengan context dari RAG
        """
        if not self.api_key:
            return "Error: Gemini API key tidak ditemukan. Silakan tambahkan GEMINI_API_KEY ke file .env"
        
        try:
            # Format context untuk prompt
            formatted_context = self._format_context(context)
            
            # Buat prompt yang menggabungkan question dan context
            prompt = self._create_prompt(question, formatted_context)
            
            # Kirim request ke Gemini API
            response = await self._call_gemini_api(prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Maaf, terjadi error saat memproses pertanyaan Anda: {str(e)}"
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """
        Format context dari RAG service menjadi string yang readable
        """
        formatted_parts = []
        
        # Format articles
        if context.get("articles"):
            formatted_parts.append("=== ARTIKEL TERKAIT ===")
            for i, article in enumerate(context["articles"], 1):
                formatted_parts.append(f"Artikel {i} ({article['source']}):")
                formatted_parts.append(article["content"])
                formatted_parts.append("")
        
        # Format GitHub projects
        if context.get("github_projects"):
            formatted_parts.append("=== GITHUB PROJECTS TERKAIT ===")
            for i, project in enumerate(context["github_projects"], 1):
                formatted_parts.append(f"Project {i} ({project['source']}):")
                formatted_parts.append(project["content"])
                formatted_parts.append("")
        
        return "\n".join(formatted_parts)
    
    def _create_prompt(self, question: str, context: str) -> str:
        """
        Buat prompt yang optimal untuk Gemini Pro
        """
        system_prompt = """Anda adalah asisten AI yang membantu menjawab pertanyaan berdasarkan knowledge base yang tersedia. 

Tugas Anda:
1. Analisis pertanyaan user dengan teliti
2. Gunakan context/informasi yang diberikan untuk menjawab
3. Berikan jawaban yang akurat, lengkap, dan mudah dipahami
4. Jika informasi tidak cukup dalam context, berikan jawaban umum yang membantu
5. Selalu jawab dalam bahasa Indonesia yang baik dan benar
6. Jika ada kode atau contoh teknis, berikan penjelasan yang jelas

Context yang tersedia:
""" + context + """

Pertanyaan user: """ + question + """

Jawaban:"""

        return system_prompt
    
    async def _call_gemini_api(self, prompt: str) -> str:
        """
        Panggil Gemini Pro API
        """
        url = f"{self.base_url}?key={self.api_key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        session = await self._get_session()
        
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                
                # Extract response text
                if "candidates" in result and len(result["candidates"]) > 0:
                    candidate = result["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        return candidate["content"]["parts"][0]["text"]
                
                return "Maaf, tidak ada response yang valid dari Gemini API"
                
            else:
                error_text = await response.text()
                logger.error(f"Gemini API error: {response.status} - {error_text}")
                return f"Error dari Gemini API: {response.status}"
    
    async def close(self):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        if self.session and not self.session.closed:
            # Try to close session in event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self.close())
            except:
                pass
