import React, { useState } from 'react';
import { Button, Modal, Form, Alert } from 'react-bootstrap';
import { useCreateTask } from '../hooks/useCreateTask'; // Custom hook for creating tasks

const AddTaskModal = ({ showModal, onHide, parentTask, onCreateTask }) => {
    const [taskTitle, setTaskTitle] = useState('');
    const [taskDescription, setTaskDescription] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const { mutate: createTask, isLoading, isError } = useCreateTask();

    const handleCreateTask = () => {
        console.log('Button clicked to create task'); // Log when button is clicked

        if (taskTitle && taskDescription) {
            // Prepare task data
            const taskData = {
                title: taskTitle,
                description: taskDescription,
            };

            // Conditionally add parent_uuid only if parentTask exists (subtask case)
            if (parentTask?.uuid) {
                taskData.parent_uuid = parentTask.uuid; // Assign parent task uuid for subtasks
            }

            console.log('Creating task with:', taskData);

            // Call the mutation to create the task
            createTask(taskData, {
                onSuccess: (newTask) => {
                    console.log('Task creation successful:', newTask); // Log success
                    onCreateTask(newTask); // Notify parent component about the new task
                    setTaskTitle('');
                    setTaskDescription('');
                    setErrorMessage(''); // Clear any previous error messages
                    onHide(); // Close the modal on success
                },
                onError: (error) => {
                    console.error('Error creating task:', error); // Log the full error
                    setErrorMessage('Failed to create task. Please try again.');
                },
            });
        } else {
            console.log('Missing title or description:', { taskTitle, taskDescription }); // Log missing fields
            setErrorMessage('Please provide both a title and a description.');
        }
    };

    return (
        <Modal show={showModal} onHide={onHide}>
            <Modal.Header closeButton>
                <Modal.Title>Create New Task</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {isError && <Alert variant="danger">{errorMessage}</Alert>}
                <Form>
                    <Form.Group controlId="taskTitle">
                        <Form.Label>Title</Form.Label>
                        <Form.Control
                            type="text"
                            value={taskTitle}
                            onChange={(e) => setTaskTitle(e.target.value)}
                            placeholder="Enter task title"
                        />
                    </Form.Group>
                    <Form.Group controlId="taskDescription">
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={3}
                            value={taskDescription}
                            onChange={(e) => setTaskDescription(e.target.value)}
                            placeholder="Enter task description"
                        />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={onHide}>
                    Close
                </Button>
                <Button variant="primary" onClick={handleCreateTask} disabled={isLoading}>
                    {isLoading ? 'Creating...' : 'Create Task'}
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default AddTaskModal