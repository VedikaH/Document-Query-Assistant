from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routes import pdf_routes, project_routes, query_routes

app = FastAPI(title="PDF RAG Application")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(project_routes.router, prefix="/api/projects")
app.include_router(pdf_routes.router, prefix="/api/pdfs")
app.include_router(query_routes.router, prefix="/api/query")

@app.get("/")
def read_root():
    return {"message": "Welcome to PDF RAG Application"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)