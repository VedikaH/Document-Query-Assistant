import React, { useState } from 'react';
import { Form, Button, Card } from 'react-bootstrap';
import apiService from '../apiService';

function QueryInterface({ projectId }) {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleQuery = async () => {
    if (!query) return;

    setLoading(true);
    try {
      const result = await apiService.queryPDFs(projectId, query);
      setResponse(result);
    } catch (error) {
      console.error('Query error:', error);
      setResponse({ 
        answer: 'Error processing your query', 
        sources: [] 
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Form>
        <Form.Group>
          <Form.Label>Ask a Question</Form.Label>
          <Form.Control 
            type="text" 
            placeholder="Enter your question" 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </Form.Group>
        <Button 
          variant="primary" 
          onClick={handleQuery} 
          disabled={loading}
          className="mt-3"
        >
          {loading ? 'Searching...' : 'Ask'}
        </Button>
      </Form>

      {response && (
        <Card className="mt-4">
          <Card.Body>
            <Card.Title>Answer</Card.Title>
            <Card.Text>{response.answer}</Card.Text>
            
            <h6>Sources:</h6>
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
    </div>
  );
}

export default QueryInterface;