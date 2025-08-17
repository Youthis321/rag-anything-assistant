import os
import json
import glob
from datetime import datetime, date, timedelta
from typing import List, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class HistoryService:
    """
    Service untuk menyimpan dan mengambil riwayat chat
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent / "rag-data" / "data-history"
        
        # Pastikan folder history ada
        os.makedirs(self.base_path, exist_ok=True)
    
    def save_chat(self, question: str, answer: str, timestamp: str, sources: List[str] = None) -> bool:
        """
        Simpan percakapan chat ke file JSON berdasarkan tanggal
        """
        try:
            # Parse timestamp untuk mendapatkan tanggal
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00') if timestamp.endswith('Z') else timestamp)
            date_str = dt.strftime("%Y-%m-%d")
            
            # Path file untuk tanggal tersebut
            file_path = self.base_path / f"chat_{date_str}.json"
            
            # Data percakapan
            conversation = {
                "timestamp": timestamp,
                "question": question,
                "answer": answer,
                "sources": sources or [],
                "id": dt.strftime("%Y%m%d_%H%M%S")  # Unique ID berdasarkan timestamp
            }
            
            # Baca file existing atau buat baru
            existing_data = []
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON in {file_path}, creating new file")
                    existing_data = []
            
            # Tambah percakapan baru
            existing_data.append(conversation)
            
            # Simpan kembali ke file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Chat saved to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving chat: {str(e)}")
            return False
    
    def get_history_by_date(self, date_str: str) -> List[Dict[str, Any]]:
        """
        Ambil history chat berdasarkan tanggal (format: YYYY-MM-DD)
        """
        try:
            # Validasi format tanggal
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Format tanggal harus YYYY-MM-DD")
            
            file_path = self.base_path / f"chat_{date_str}.json"
            
            if not file_path.exists():
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Sort berdasarkan timestamp
            data.sort(key=lambda x: x.get('timestamp', ''))
            
            return data
            
        except Exception as e:
            logger.error(f"Error getting history for {date_str}: {str(e)}")
            return []
    
    def get_recent_history(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Ambil history chat dalam beberapa hari terakhir
        """
        try:
            all_history = []
            
            # Ambil file history dalam range tanggal
            for i in range(days):
                target_date = date.today() - timedelta(days=i)
                date_str = target_date.strftime("%Y-%m-%d")
                
                daily_history = self.get_history_by_date(date_str)
                for chat in daily_history:
                    chat['date'] = date_str
                    all_history.append(chat)
            
            # Sort berdasarkan timestamp
            all_history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return all_history
            
        except Exception as e:
            logger.error(f"Error getting recent history: {str(e)}")
            return []
    
    def count_total_conversations(self) -> int:
        """
        Hitung total jumlah percakapan dalam semua history
        """
        try:
            total = 0
            
            # Cari semua file chat_*.json
            pattern = str(self.base_path / "chat_*.json")
            history_files = glob.glob(pattern)
            
            for file_path in history_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    total += len(data)
                except Exception as e:
                    logger.warning(f"Error reading {file_path}: {str(e)}")
                    continue
            
            return total
            
        except Exception as e:
            logger.error(f"Error counting conversations: {str(e)}")
            return 0
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """
        Ambil statistik percakapan
        """
        try:
            stats = {
                "total_conversations": 0,
                "total_days": 0,
                "first_conversation": None,
                "last_conversation": None,
                "conversations_by_date": {}
            }
            
            # Cari semua file chat_*.json
            pattern = str(self.base_path / "chat_*.json")
            history_files = glob.glob(pattern)
            
            all_timestamps = []
            
            for file_path in history_files:
                try:
                    date_from_filename = os.path.basename(file_path).replace("chat_", "").replace(".json", "")
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    conversation_count = len(data)
                    stats["total_conversations"] += conversation_count
                    stats["conversations_by_date"][date_from_filename] = conversation_count
                    
                    # Collect timestamps
                    for chat in data:
                        if chat.get('timestamp'):
                            all_timestamps.append(chat['timestamp'])
                    
                except Exception as e:
                    logger.warning(f"Error processing {file_path}: {str(e)}")
                    continue
            
            stats["total_days"] = len(history_files)
            
            if all_timestamps:
                all_timestamps.sort()
                stats["first_conversation"] = all_timestamps[0]
                stats["last_conversation"] = all_timestamps[-1]
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting conversation stats: {str(e)}")
            return {
                "total_conversations": 0,
                "total_days": 0,
                "error": str(e)
            }
    
    def delete_history_by_date(self, date_str: str) -> bool:
        """
        Hapus history berdasarkan tanggal
        """
        try:
            file_path = self.base_path / f"chat_{date_str}.json"
            
            if file_path.exists():
                os.remove(file_path)
                logger.info(f"Deleted history for {date_str}")
                return True
            else:
                logger.warning(f"No history found for {date_str}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting history for {date_str}: {str(e)}")
            return False
