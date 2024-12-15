from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
import os
import uuid
from app.pdf_service import PDFService
from app.vector_store import VectorStore

router = APIRouter()
pdf_service = PDFService()
vector_store = VectorStore()

@router.post("/upload/{project_id}")
async def upload_pdf(project_id: str, file: UploadFile = File(...)):
    # Check if project exists 
    from app.routes.project_routes import projects
    project = projects.get(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    uploads_dir = './uploads/'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join("./uploads/", unique_filename)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    try:
        # Extract chunks from PDF
        chunks = pdf_service.extract_text_from_pdf(file_path)
        
        # Add to vector store
        vector_store.add_documents(
            project['collection_name'], 
            chunks, 
            file.filename, 
            project['name']
        )
        
        # Update project PDFs
        project['pdfs'][file.filename] = {
            "chunks": len(chunks)
        }
        
        return {
            "message": "PDF uploaded and processed successfully",
            "filename": file.filename,
            "chunks": len(chunks)
        }
    finally:
        # Clean up the temporary file
        os.unlink(file_path)