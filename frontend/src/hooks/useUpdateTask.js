import { useMutation } from '@tanstack/react-query';
import { useAxios } from './useAxios'; // Import your custom Axios hook

// Function to handle the update task API call using the Axios instance from `useAxios`
const updateTask = async ({ taskId, taskData }, axiosInstance) => {
    const response = await axiosInstance.patch(`/tasks/${taskId}`, taskData); // Use relative path
    return response.data; // Return updated task data
};

// Hook that uses the updateTask mutation with the Axios instance
export const useUpdateTask = () => {
    const axiosInstance = useAxios(); // Get the Axios instance with middleware

    return useMutation({
        mutationFn: (data) => updateTask(data, axiosInstance), // Pass the `axiosInstance` to the updateTask function
    });
};