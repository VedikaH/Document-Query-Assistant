# backend/app/services/pdf_service.py
import pdfplumber
from typing import List, Dict
import tempfile


class PDFService:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> List[Dict]:
        """Extract text and tables from PDF using pdfplumber"""
        chunks = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract text
                text = page.extract_text()
                if text:
                    chunks.append({
                        "content": text,
                        "metadata": {
                            "page": page_num,
                            "type": "text"
                        }
                    })
                
                # Extract tables
                tables = page.extract_tables()
                for table_num, table in enumerate(tables, 1):
                    table_str = "\n".join([" | ".join([str(cell) if cell else "" for cell in row]) for row in table])
                    chunks.append({
                        "content": f"Table {table_num} on page {page_num}:\n{table_str}",
                        "metadata": {
                            "page": page_num,
                            "type": "table",
                            "table_num": table_num
                        }
                    })
        
        return chunks
    


    @staticmethod
    def process_uploaded_file(uploaded_file) -> str:
        """Process uploaded file and return temporary path"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name