import React, { useState } from 'react';
import { Button, Card } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import AddTaskModal from './AddTaskModal'; // Modal for creating tasks/subtasks
import { useCreateTask } from '../hooks/useCreateTask'; // Assuming createTask is a custom hook now
import { useDeleteTask } from '../hooks/useDeleteTask'; // Import delete task hook

const TaskCard = ({ task, onDelete }) => {
    const navigate = useNavigate();
    const [showModal, setShowModal] = useState(false);
    const { mutateAsync: createSubtask, isLoading: isCreatingSubtask } = useCreateTask();
    const { mutateAsync: deleteTask, isLoading: isDeletingTask } = useDeleteTask();

    // Handle subtask creation
    const handleCreateSubtask = async (newSubtaskData) => {
        try {
            const createdSubtask = await createSubtask({ ...newSubtaskData, parentTaskId: task.uuid });
            onDelete(task.uuid, createdSubtask); // Update parent with new subtask
            setShowModal(false);
        } catch (error) {
            console.error('Error creating subtask:', error);
            alert('Failed to create subtask. Please try again.');
        }
    };

    const handleTaskComplete = async () => {
        if (window.confirm('Are you sure you want to complete this task?')) {
            try {
                await deleteTask(task.uuid); // Call the delete task mutation
                onDelete(task.uuid); // Inform the parent to remove the task from the list
            } catch (error) {
                console.error('Error completing task:', error);
                alert('Failed to complete task. Please try again.');
            }
        }
    };

    return (
        <Card className="mb-3">
            <Card.Body>
                <Card.Title
                    style={{ cursor: 'pointer', textDecoration: 'underline' }}
                    onClick={() => navigate(`/tasks/${task.uuid}`)}
                >
                    {task?.title || 'Loading task...'}
                </Card.Title>

                <Card.Text>{task.description}</Card.Text>
                <Card.Text>Status: <strong>{task.status}</strong></Card.Text>

                <div className="d-flex justify-content-between">
                    <Button
                        variant="danger"
                        onClick={handleTaskComplete}
                        disabled={isDeletingTask}
                    >
                        {isDeletingTask ? 'Completing...' : task.deleted ? 'Completed' : 'Complete'}
                    </Button>

                    {task.subtask_count > 0 && (
                        <Button
                            variant="link"
                            onClick={() => navigate(`/tasks/${task.uuid}`)}
                        >
                            See Subtasks
                        </Button>
                    )}
                </div>
            </Card.Body>

            <AddTaskModal
                showModal={showModal}
                onHide={() => setShowModal(false)}
                onCreateTask={handleCreateSubtask}
                parentTask={task}
                isLoading={isCreatingSubtask}
            />
        </Card>
    );
};

export default TaskCard;