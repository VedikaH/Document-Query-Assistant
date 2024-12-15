import axios from 'axios';
import { API_BASE_URL } from './config';

const apiService = {
  createProject: async (projectName) => {
    const response = await axios.post(`${API_BASE_URL}/projects/create`, { project_name: projectName });
    return response.data;
  },

  listProjects: async () => {
    const response = await axios.get(`${API_BASE_URL}/projects/list`);
    return response.data;
  },

  uploadPDF: async (projectId, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_BASE_URL}/pdfs/upload/${projectId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    return response.data;
  },

  queryPDFs: async (projectId, query) => {
    const response = await axios.post(`${API_BASE_URL}/query/ask`, { 
      project_id: projectId,
      query: query 
    });

    return response.data;
  },

  // Add this method to the existing apiService
  getProject: async (projectId) => {
    const response = await axios.get(`${API_BASE_URL}/projects/${projectId}`);
    return response.data;
  },

  deleteProject: async (projectId) => {
    const response = await axios.delete(`${API_BASE_URL}/projects/${projectId}`);
    return response.data;
  }


};

export default apiService;