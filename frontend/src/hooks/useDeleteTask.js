import { useMutation } from '@tanstack/react-query';
import { useAxios } from '../hooks/useAxios'; // Import the custom Axios hook

export const useDeleteTask = () => {
    const axiosInstance = useAxios(); // Get the Axios instance with middleware

    // Mutation function for deleting the task
    const deleteTask = async (taskId) => {
        const { data } = await axiosInstance.delete(`/tasks/${taskId}`); // Make DELETE request
        return data; // Return the response from the API
    };

    // Use React Query's useMutation to handle the delete operation
    return useMutation({
        mutationFn: deleteTask, // Pass the deleteTask function here
    });
};