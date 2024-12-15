import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Tabs, Tab } from 'react-bootstrap';
import apiService from '../apiService';
import PDFUploader from '../components/PDFUploader';
import QueryInterface from '../components/QueryInterface';

function ProjectPage() {
  const { projectId } = useParams();
  const [project, setProject] = useState(null);
  const [uploadedPDFs, setUploadedPDFs] = useState([]);

  useEffect(() => {
    // Fetch project details when component mounts
    const fetchProjectDetails = async () => {
      try {
        // You might need to modify the API service to get project details
        const projectDetails = await apiService.getProject(projectId);
        setProject(projectDetails);
        setUploadedPDFs(Object.keys(projectDetails.pdfs));
      } catch (error) {
        console.error('Error fetching project details:', error);
      }
    };

    fetchProjectDetails();
  }, [projectId]);

  const handleUploadComplete = (uploadResult) => {
    setUploadedPDFs(prev => [...prev, uploadResult.filename]);
  };

  if (!project) {
    return <div>Loading...</div>;
  }

  return (
    <Container>
      <h1 className="my-4">{project.name}</h1>

      <Tabs defaultActiveKey="upload" className="mb-3">
        <Tab eventKey="upload" title="Upload PDFs">
          <PDFUploader 
            projectId={projectId} 
            onUploadComplete={handleUploadComplete} 
          />

          <h3 className="mt-4">Uploaded PDFs</h3>
          <ul>
            {uploadedPDFs.map((pdf, index) => (
              <li key={index}>{pdf}</li>
            ))}
          </ul>
        </Tab>

        <Tab eventKey="query" title="Query PDFs">
          <QueryInterface projectId={projectId} />
        </Tab>
      </Tabs>
    </Container>
  );
}

export default ProjectPage;