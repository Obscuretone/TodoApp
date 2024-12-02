import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useGetTaskDetails } from '../hooks/useGetTaskDetails'; // Custom hook for fetching task details
import { useSplitTask } from '../hooks/useSplitTask'; // Custom hook for splitting tasks
import { Container, Button, Row, Col } from 'react-bootstrap';
import TaskCard from './TaskCard'; // Import the TaskCard component
import AddTaskModal from './AddTaskModal'; // Import AddTaskModal
import SplitTaskForm from './SplitTaskForm'; // Import the new SplitTaskForm component
import BackButton from './BackButton'; // Import BackButton component
import TaskDetail from './TaskDetail'; // Import TaskDetail component

const TaskPage = () => {
    const { taskId } = useParams();
    const navigate = useNavigate();

    const [subtasks, setSubtasks] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [splitCount, setSplitCount] = useState(1);

    // Fetch task details using the custom hook
    const { data, isLoading, isError, error: fetchError } = useGetTaskDetails(taskId);

    // Use the split task mutation hook
    const { mutate: splitTask, isLoading: isSplitting, isError: isSplitError } = useSplitTask();

    // Handle any errors when fetching data
    const error = fetchError || (isError && "Failed to fetch task details.");

    // Set subtasks when task details are available
    useEffect(() => {
        if (data && data.subtasks) {
            setSubtasks(data.subtasks);  // Ensure we set only the subtasks related to the current task
        }
    }, [data]); // Run only when `data` changes

    // Early return for loading or error states
    if (isLoading || isSplitting) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    if (!data || !data.task) {
        return <div>No task details available</div>;
    }

    const taskDetails = data.task;

    const handleAddSubtask = () => {
        setShowModal(true); // Open the modal when the user wants to add a subtask
    };

    const handleTaskDelete = (taskId) => {
        setSubtasks((prevSubtasks) => prevSubtasks.filter((subtask) => subtask.uuid !== taskId));
    };

    const handleCreateSubtask = (newSubtask) => {
        setSubtasks((prev) => [...prev, newSubtask]); // Add new subtask to the list
    };

    return (
        <Container>
            {/* Back Button Component */}
            <BackButton taskDetails={taskDetails} />

            {/* Task Details */}
            <TaskDetail taskDetails={taskDetails} navigate={navigate} />

            {/* Split Task Form */}
            <SplitTaskForm
                taskId={taskId}
                splitCount={splitCount}
                setSplitCount={setSplitCount}
                isSplitting={isSplitting}
                splitTask={splitTask}
            />

            {/* Subtasks Section */}
            {subtasks.length > 0 && (
                <div>
                    <h3>Subtasks</h3>
                    {subtasks.map((subtask) => (
                        <div key={subtask.uuid} className="col-md-4 mb-3">
                            <TaskCard task={subtask} onDelete={handleTaskDelete} />
                        </div>
                    ))}
                </div>
            )}

            {/* Add Task Modal Button */}
            <Button variant="success" onClick={handleAddSubtask}>
                Add New Subtask
            </Button>

            {/* AddTaskModal for Creating Subtasks */}
            <AddTaskModal
                showModal={showModal}
                onHide={() => setShowModal(false)}
                onCreateTask={handleCreateSubtask}
                parentTask={taskDetails}
            />
        </Container>
    );
};

export default TaskPage;