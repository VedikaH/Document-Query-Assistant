from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.llm_service import LLMService
from app.vector_store import VectorStore


router = APIRouter()
vector_store = VectorStore()
llm_service = LLMService()

class QueryRequest(BaseModel):
    project_id: str
    query: str

@router.post("/ask")
def query_pdfs(request: QueryRequest):
    # Check project 
    from app.routes.project_routes import projects
    project = projects.get(request.project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Retrieve relevant chunks
    results = vector_store.query_documents(
        project['collection_name'], 
        request.query,
        project['name'],
        5  # number of results
    )
    print(project['collection_name'])
    print(results)
    
    # Generate response
    response = llm_service.generate_response(
        request.query, 
        results["documents"][0]
    )
    
    return {
        "answer": response,
        "sources": [
            {
                "pdf_name": metadata['pdf_name'], 
                "page": metadata['page']
            } for metadata in results["metadatas"][0]
        ]
    }