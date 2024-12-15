import React, { useState, useEffect } from 'react';
import { Container, Form, Button, Card, Alert } from 'react-bootstrap';
import apiService from '../apiService';

function QueryPage() {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState('');
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const projectList = await apiService.listProjects();
        setProjects(projectList);
      } catch (err) {
        setError('Failed to load projects');
        console.error(err);
      }
    };

    fetchProjects();
  }, []);

  const handleQuery = async () => {
    if (!selectedProject) {
      setError('Please select a project');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await apiService.queryPDFs(selectedProject, query);
      setResponse(result);
    } catch (err) {
      setError('Error processing your query');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <h1 className="my-4">PDF Query Interface</h1>

      <Form>
        <Form.Group className="mb-3">
          <Form.Label>Select Project</Form.Label>
          <Form.Select 
            value={selectedProject}
            onChange={(e) => setSelectedProject(e.target.value)}
          >
            <option value="">Choose a project</option>
            {projects.map(project => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Your Query</Form.Label>
          <Form.Control 
            type="text"
            placeholder="Enter your question"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={!selectedProject}
          />
        </Form.Group>

        <Button 
          variant="primary" 
          onClick={handleQuery}
          disabled={loading || !selectedProject || !query}
        >
          {loading ? 'Searching...' : 'Search'}
        </Button>
      </Form>

      {error && (
        <Alert variant="danger" className="mt-3">
          {error}
        </Alert>
      )}

      {response && (
        <Card className="mt-4">
          <Card.Body>
            <Card.Title>Query Result</Card.Title>
            <Card.Text>{response.answer}</Card.Text>
            
            <h6 className="mt-3">Sources:</h6>
            <ul>
              {response.sources.map((source, index) => (
                <li key={index}>
                  {source.pdf_name} (Page {source.page})
                </li>
              ))}
            </ul>
          </Card.Body>
        </Card>
      )}
    </Container>
  );
}

export default QueryPage;