import React, { useState, useEffect } from "react";
import { Container, Row, Col, Button } from 'react-bootstrap';
import TaskCard from './TaskCard';
import AddTaskModal from './AddTaskModal'; // If you want to add tasks/subtasks here
import { useGetTasks } from '../hooks/useGetTasks'; // Custom hook to fetch tasks
import { useCreateTask } from '../hooks/useCreateTask'; // Custom hook to create tasks

const TasksPage = () => {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [parentTask, setParentTask] = useState(null); // For subtasks

    // Custom hook for fetching tasks (projects + subtasks)
    const { data: taskData, isLoading, isError, error: fetchError } = useGetTasks();

    // Custom hook for creating a task
    const { mutate: createTaskMutation, isLoading: isCreating, isError: isCreateError } = useCreateTask();

    useEffect(() => {
        if (fetchError) {
            setError("Failed to fetch tasks.");
        }
    }, [fetchError]);

    useEffect(() => {
        if (taskData) {
            setTasks(taskData.tasks);
            setLoading(false);
        }
    }, [taskData]);

    // Modal handler for adding a new task or subtask
    const handleCreateTask = async (taskToCreate) => {
        try {
            const token = localStorage.getItem('authToken');
            if (!token) {
                setError("User is not authenticated");
                return;
            }

            createTaskMutation(taskToCreate, {
                onSuccess: (data) => {
                    setTasks(prevTasks => [data.task, ...prevTasks]);
                    setError(null);
                    setShowModal(false);
                    setParentTask(null);
                },
                onError: (error) => {
                    setError("Failed to create task. Please try again.");
                }
            });
        } catch (error) {
            setError("Failed to create task. Please try again.");
        }
    };

    const handleShowModal = (task = null) => {
        setParentTask(task); // If it's a subtask, the parent task is passed here
        setShowModal(true);
    };

    if (isLoading) {
        return <Container className="my-4">Loading tasks...</Container>;
    }

    return (
        <Container className="my-4">
            <h1>All Tasks</h1>

            {error && <p style={{ color: 'red' }}>{error}</p>}

            <Button variant="primary" onClick={() => handleShowModal()}>
                Add New Task
            </Button>

            {tasks.length > 0 ? (
                <Row>
                    {tasks.map(task => (
                        <Col xs={12} sm={6} md={4} key={task.uuid} className="mb-3">
                            <TaskCard task={task} onCreateSubtask={handleShowModal} />
                        </Col>
                    ))}
                </Row>
            ) : (
                <p>No tasks available.</p>
            )}

            {/* Add Task Modal for creating new tasks/subtasks */}
            <AddTaskModal
                showModal={showModal}
                onHide={() => setShowModal(false)}
                onCreateTask={handleCreateTask}
                parentTask={parentTask}
            />
        </Container>
    );
};

export default TasksPage;