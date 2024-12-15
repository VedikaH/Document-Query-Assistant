import React, { useState, useEffect } from 'react';
import { Button, ListGroup } from 'react-bootstrap';
import apiService from '../apiService';
import CreateProjectModal from './CreateProjectModal';
import '../styles/Sidebar.css';
import { Link } from 'react-router-dom';


function Sidebar() {
  const [projects, setProjects] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedProject, setSelectedProject] = useState(null);

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

  return (
    <div className="sidebar">
      <h3>PDF RAG Projects</h3>
      <nav>
        <ListGroup>
          <ListGroup.Item action as={Link} to="/">
            Home
          </ListGroup.Item>
          <ListGroup.Item action as={Link} to="/query">
            Query PDFs
          </ListGroup.Item>
        </ListGroup>
      </nav>

    </div>
  );
}

export default Sidebar;