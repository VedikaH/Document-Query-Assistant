
import chromadb
from chromadb.config import Settings
from typing import List, Dict


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="data/vector_store")


    def create_collection(self, name: str):
        """Create a new collection"""
        return self.client.create_collection(name=name)

    def get_collection(self, name: str):
        """Get existing collection"""
        return self.client.get_collection(name=name)

    def add_documents(self, collection_name: str, chunks: List[Dict], pdf_name: str, project_name: str):
        """Add documents to collection"""
        collection = self.get_collection(collection_name)
        
        texts = [chunk["content"] for chunk in chunks]
        metadatas = [
            {
                **chunk["metadata"],
                "pdf_name": pdf_name,
                "project": project_name
            } for chunk in chunks
        ]
        ids = [f"{pdf_name}_{i}" for i in range(len(chunks))]
        
        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    def query_documents(self, collection_name: str, query: str, project_name: str, n_results: int = 5):
        """Query documents from collection"""
        collection = self.get_collection(collection_name)
        return collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"project": project_name}
        )
    
    def delete_collection(self, collection_name: str):
        try:
            # Delete collection from ChromaDB
            self.client.delete_collection(name=collection_name)
            
        except Exception as e:
            # Log the error or handle it as needed
            print(f"Error deleting collection {collection_name}: {e}")
            raise

