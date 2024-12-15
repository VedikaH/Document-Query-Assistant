# Document Query Assistant

## Overview

This is a full-stack web that enables dynamic document management and intelligent querying across multiple projects. Users can seamlessly upload, organize, and query documents within different project contexts, allowing for efficient knowledge management and retrieval. The system intelligently handles context switching between projects while maintaining separate document spaces for each project. The application leverages FastAPI for the backend, React for the frontend, and implements an intelligent document querying system with caching mechanisms.

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python
- **Key Libraries**:
  - Groq API for language model interactions
  - ChromaDB for vector storage
  - python-dotenv for environment management

### Frontend
- **Framework**: React
- **Language**: JavaScript
- **Styling**: 
  - CSS
  - Bootstrap

### Key Features
- Document upload and parsing
- Intelligent context-based querying
- Caching mechanism
- Vector-based document retrieval

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm
- Groq API Key
- ChromaDB

## Backend Setup

1. Clone the repository
```bash
git clone https://github.com/VedikaH/Document-Query-Assistant.git
cd backend
```

2. Install Python dependencies
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory
```
GROQ_API_KEY=your_groq_api_key_here
```

5. Run the FastAPI server
```bash
uvicorn main:app --reload
```

## Frontend Setup

1. Navigate to the frontend directory
```bash
cd frontend
```

2. Install dependencies
```bash
npm install
```

3. Start the React development server
```bash
npm start
```
