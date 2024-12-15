import React, { useState } from 'react';
import { Button, Form, Alert } from 'react-bootstrap';
import apiService from '../apiService';

function PDFUploader({ projectId, onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please select a valid PDF file');
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a PDF file');
      return;
    }

    setUploading(true);
    try {
      const result = await apiService.uploadPDF(projectId, file);
      onUploadComplete(result);
      setFile(null);
    } catch (err) {
      setError('Error uploading PDF: ' + err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <Form>
        <Form.Group>
          <Form.Label>Upload PDF</Form.Label>
          <Form.Control 
            type="file" 
            accept=".pdf" 
            onChange={handleFileChange} 
          />
        </Form.Group>
        
        {error && <Alert variant="danger">{error}</Alert>}
        
        <Button 
          variant="primary" 
          onClick={handleUpload} 
          disabled={!file || uploading}
          className="mt-3"
        >
          {uploading ? 'Uploading...' : 'Upload PDF'}
        </Button>
      </Form>
    </div>
  );
}

export default PDFUploader;