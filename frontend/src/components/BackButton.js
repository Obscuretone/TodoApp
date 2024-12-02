import { Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useGetTaskDetails } from '../hooks/useGetTaskDetails'; // Import your hook

const BackButton = ({ taskDetails }) => {
    const navigate = useNavigate();

    // Check if there's a valid parent_id and if it's not the placeholder value
    const hasParentTask = taskDetails?.parent_id && taskDetails?.parent_id !== '00000000-0000-0000-0000-000000000000';

    // If the parent_id is valid, fetch the parent task details
    const { data: parentTask, isLoading, error } = useGetTaskDetails(taskDetails?.parent_id);

    const handleBackNavigation = () => {
        if (hasParentTask) {
            // Navigate to the parent task if it exists
            navigate(`/tasks/${taskDetails.parent_id}`);
        } else {
            // Navigate to projects if no parent task
            navigate('/projects');
        }
    };

    let backText = 'Back to Projects';

    // Set the button text conditionally based on parent task data
    if (hasParentTask) {
        if (isLoading) {
            backText = 'Loading parent task...'; // Show loading state
        } else if (error) {
            backText = 'Error fetching parent task'; // Show error state
        } else if (parentTask?.task.title) {
            backText = `Back to ${parentTask.task.title}`; // Use parent task title if available
        } else {
            console.log(parentTask)
            backText = 'Back'; // Default fallback
        }
    }

    return (
        <Button
            variant="secondary"
            onClick={handleBackNavigation}
            className="my-3"
        >
            {backText}
        </Button>
    );
};

export default BackButton;