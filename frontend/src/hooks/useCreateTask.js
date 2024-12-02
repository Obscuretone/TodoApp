import { useMutation } from '@tanstack/react-query';
import { useAxios } from '../hooks/useAxios'; // Import the custom Axios hook

export const useCreateTask = () => {
    const axiosInstance = useAxios(); // Get the Axios instance with middleware

    // Mutation function using the axiosInstance
    const createTask = async (taskData) => {
        const { data } = await axiosInstance.post('/tasks', taskData, {
            headers: { 'Content-Type': 'application/json' }, // Content-Type header
        });
        return data.task; // Ensure backend returns data in this format
    };

    // Return the mutation with React Query's useMutation
    return useMutation({ mutationFn: createTask });
};