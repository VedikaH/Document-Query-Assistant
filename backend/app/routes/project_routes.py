# backend/app/routes/project_routes.py
from typing import Dict
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.vector_store import VectorStore


router = APIRouter()
vector_store = VectorStore()

class ProjectCreate(BaseModel):
    project_name: str

class Project(BaseModel):
    id: str
    name: str
    collection_name: str
    pdfs: dict = {}

projects = {}

@router.post("/create", response_model=Project)
def create_project(project_data: ProjectCreate):
    # Generate unique collection name
    collection_name = f"project_{str(uuid.uuid4())[:8]}"
    
    # Create collection in vector store
    vector_store.create_collection(collection_name)
    
    # Create project entry
    project = {
        "id": str(uuid.uuid4()),
        "name": project_data.project_name,
        "collection_name": collection_name,
        "pdfs": {}
    }
    
    projects[project['id']] = project
    return project

@router.get("/list")
def list_projects():
    return list(projects.values())

@router.get("/{project_id}")
def get_project(project_id: str):
    project = projects.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}")
def delete_project(project_id: str):
    # Check if project exists
    project = projects.get(project_id)
    print(project)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        # Delete collection from vector store
        vector_store.delete_collection(project['collection_name'])
        
        # Remove project from in-memory storage
        del projects[project_id]
        
        return {"message": f"Project '{project['name']}' deleted successfully"}
    
    except Exception as e:
        # Handle any errors during deletion
        raise HTTPException(
            status_code=500, 
            detail=f"Error deleting project: {str(e)}"
        )