import os
import json
import glob
from typing import Dict, List, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class RAGService:
    """
    Service untuk mengelola knowledge base dari data-artikel dan data-clone-github
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent / "rag-data"
        self.articles_path = self.base_path / "data-artikel"
        self.github_path = self.base_path / "data-clone-github"
        
        # Pastikan folder ada
        os.makedirs(self.articles_path, exist_ok=True)
        os.makedirs(self.github_path, exist_ok=True)
    
    def retrieve_context(self, question: str) -> Dict[str, Any]:
        """
        Retrieve context dari knowledge base berdasarkan pertanyaan
        """
        try:
            # Gabungkan context dari artikel dan github projects
            article_context = self._search_articles(question)
            github_context = self._search_github_projects(question)
            
            # Kombinasikan hasil
            combined_context = {
                "articles": article_context,
                "github_projects": github_context,
                "sources": []
            }
            
            # Tambahkan sources untuk tracking
            combined_context["sources"].extend([item["source"] for item in article_context])
            combined_context["sources"].extend([item["source"] for item in github_context])
            
            return combined_context
            
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return {"articles": [], "github_projects": [], "sources": []}
    
    def _search_articles(self, question: str) -> List[Dict[str, Any]]:
        """
        Cari artikel yang relevan dengan pertanyaan
        """
        results = []
        
        try:
            # Cari semua file artikel (txt, md, json)
            article_files = []
            for ext in ["*.txt", "*.md", "*.json"]:
                article_files.extend(glob.glob(str(self.articles_path / "**" / ext), recursive=True))
            
            for file_path in article_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Simple keyword matching (bisa diperbaiki dengan semantic search)
                    if self._is_relevant(content, question):
                        results.append({
                            "content": content[:1000],  # Limit content
                            "source": os.path.basename(file_path),
                            "type": "article",
                            "path": file_path
                        })
                        
                except Exception as e:
                    logger.warning(f"Error reading article {file_path}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error searching articles: {str(e)}")
        
        return results[:5]  # Limit to top 5 results
    
    def _search_github_projects(self, question: str) -> List[Dict[str, Any]]:
        """
        Cari GitHub projects yang relevan dengan pertanyaan
        """
        results = []
        
        try:
            # Cari folder project di data-clone-github
            for project_dir in os.listdir(self.github_path):
                project_path = self.github_path / project_dir
                
                if os.path.isdir(project_path):
                    # Baca README.md jika ada
                    readme_path = project_path / "README.md"
                    if readme_path.exists():
                        try:
                            with open(readme_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            if self._is_relevant(content, question):
                                results.append({
                                    "content": content[:1000],  # Limit content
                                    "source": f"GitHub: {project_dir}",
                                    "type": "github_project",
                                    "path": str(project_path)
                                })
                                
                        except Exception as e:
                            logger.warning(f"Error reading README for {project_dir}: {str(e)}")
                    
                    # Cari file kode yang relevan
                    code_files = self._find_relevant_code_files(project_path, question)
                    for code_file in code_files:
                        results.append(code_file)
                        
        except Exception as e:
            logger.error(f"Error searching GitHub projects: {str(e)}")
        
        return results[:5]  # Limit to top 5 results
    
    def _find_relevant_code_files(self, project_path: Path, question: str) -> List[Dict[str, Any]]:
        """
        Cari file kode yang relevan dalam project
        """
        results = []
        code_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.html', '.css']
        
        try:
            for ext in code_extensions:
                for file_path in project_path.rglob(f"*{ext}"):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if self._is_relevant(content, question) and len(content) < 5000:  # Skip very large files
                            results.append({
                                "content": content[:800],  # Limit content
                                "source": f"Code: {file_path.name}",
                                "type": "code_file",
                                "path": str(file_path)
                            })
                            
                    except Exception as e:
                        logger.warning(f"Error reading code file {file_path}: {str(e)}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error finding code files: {str(e)}")
        
        return results[:3]  # Limit code files
    
    def _is_relevant(self, content: str, question: str) -> bool:
        """
        Simple relevance check (bisa diperbaiki dengan semantic similarity)
        """
        content_lower = content.lower()
        question_lower = question.lower()
        
        # Extract keywords from question
        keywords = [word.strip() for word in question_lower.split() if len(word.strip()) > 2]
        
        # Check if any keyword exists in content
        relevance_score = 0
        for keyword in keywords:
            if keyword in content_lower:
                relevance_score += 1
        
        # Return True if at least 1 keyword found or if content is short (likely important)
        return relevance_score > 0 or len(content) < 200
    
    def count_articles(self) -> int:
        """
        Hitung jumlah artikel yang tersedia
        """
        try:
            count = 0
            for ext in ["*.txt", "*.md", "*.json"]:
                count += len(glob.glob(str(self.articles_path / "**" / ext), recursive=True))
            return count
        except Exception as e:
            logger.error(f"Error counting articles: {str(e)}")
            return 0
    
    def count_projects(self) -> int:
        """
        Hitung jumlah GitHub projects yang tersedia
        """
        try:
            return len([d for d in os.listdir(self.github_path) 
                       if os.path.isdir(self.github_path / d)])
        except Exception as e:
            logger.error(f"Error counting projects: {str(e)}")
            return 0
