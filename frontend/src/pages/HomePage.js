import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import apiService from '../apiService';
import CreateProjectModal from '../components/CreateProjectModal';

function HomePage() {
  const [projects, setProjects] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const projectList = await apiService.listProjects();
      setProjects(projectList);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  const handleCreateProject = async (projectName) => {
    try {
      const newProject = await apiService.createProject(projectName);
      setProjects([...projects, newProject]);
      setShowCreateModal(false);
    } catch (error) {
      console.error('Error creating project:', error);
    }
  };

  const handleDeleteProject = async (projectId) => {
    try {
      await apiService.deleteProject(projectId);
      // Remove the deleted project from the state
      setProjects(projects.filter(project => project.id !== projectId));
    } catch (error) {
      console.error('Error deleting project:', error);
    }
  };

  return (
    <Container>
      <h1 className="my-4">PDF RAG Application</h1>
      
      <Button 
        variant="primary" 
        onClick={() => setShowCreateModal(true)} 
        className="mb-3"
      >
        Create New Project
      </Button>
      
      <Row>
        {projects.map(project => (
          <Col md={4} key={project.id} className="mb-3">
            <Card>
              <Card.Body>
                <Card.Title>{project.name}</Card.Title>
                
                <Card.Text>
                  PDFs: {Object.keys(project.pdfs).length}
                </Card.Text>
                
                <div className="d-flex justify-content-between">
                  <Button 
                    variant="outline-primary" 
                    href={`/project/${project.id}`}
                  >
                    View Project
                  </Button>
                  
                  <Button 
                    variant="danger" 
                    onClick={() => handleDeleteProject(project.id)}
                  >
                    Delete Project
                  </Button>
                </div>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <CreateProjectModal 
        show={showCreateModal} 
        onHide={() => setShowCreateModal(false)} 
        onCreateProject={handleCreateProject} 
      />
    </Container>
  );
}

export default HomePage;