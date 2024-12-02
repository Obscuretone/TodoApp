import React, { useState, useEffect } from "react";
import { Container, Button } from 'react-bootstrap';
import { useGetProjects } from '../hooks/useGetProjects'; // Import the custom hook for fetching projects
import { useCreateProject } from '../hooks/useCreateProject'; // Import the custom hook for creating a project
import TaskCard from './TaskCard';
import AddTaskModal from './AddTaskModal';

const ProjectList = () => {
    const [showModal, setShowModal] = useState(false);
    const [parentTask, setParentTask] = useState(null); // Store the parent task
    const [error, setError] = useState(null);

    const token = localStorage.getItem('authToken');

    // Use the custom hook to fetch projects
    const { data: projects, isLoading, isError, error: fetchError } = useGetProjects(token);

    // Use the custom hook to create a project
    const { mutateAsync: createProject, isLoading: isCreating } = useCreateProject();

    useEffect(() => {
        if (fetchError) {
            setError("Failed to fetch projects.");
        }
    }, [fetchError]);

    const handleCreateSubtask = (task) => {
        setParentTask(task);
        setShowModal(true);
    };

    const handleCreateTask = async (taskToCreate) => {
        try {
            await createProject(taskToCreate); // Await the project creation
            setShowModal(false);
            setParentTask(null); // Reset parent task after creating subtask
        } catch (error) {
            setError("Failed to create project. Please try again.");
        }
    };

    const handleShowModal = (task = null) => {
        setParentTask(task);
        setShowModal(true);
    };

    return (
        <Container className="my-4">
            <h1>Projects</h1>

            {error && <p style={{ color: 'red' }}>{error}</p>}

            <Button variant="primary" onClick={() => handleShowModal()}>
                Add New Project
            </Button>

            {isLoading ? (
                <p>Loading projects...</p>
            ) : isError ? (
                <p style={{ color: 'red' }}>Failed to load projects. Please try again later.</p>
            ) : projects && projects.length > 0 ? (
                <div className="row">
                    {projects.map((project) => (
                        <div key={project.uuid} className="col-md-4 mb-3">
                            <TaskCard
                                task={project}
                                onCreateSubtask={handleCreateSubtask}
                            />
                        </div>
                    ))}
                </div>
            ) : (
                <p>No projects available.</p>
            )}

            <AddTaskModal
                showModal={showModal}
                onHide={() => setShowModal(false)}
                onCreateTask={handleCreateTask}
                parentTask={parentTask}
                isLoading={isCreating} // Optionally show loading indicator when creating a project
            />
        </Container>
    );
};

export default ProjectList;