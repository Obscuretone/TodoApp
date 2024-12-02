import { useMutation } from '@tanstack/react-query';
import { useAxios } from '../hooks/useAxios'; // Import the custom Axios hook

export const useCreateProject = () => {
    const axiosInstance = useAxios(); // Get the Axios instance with middleware

    // Mutation function using the axiosInstance
    const createProject = async (projectData) => {
        const { data } = await axiosInstance.post('/tasks', projectData, {
            headers: { 'Content-Type': 'application/json' }, // Content-Type header
        });
        return data.task; // Return the created task
    };

    // Return the mutation using React Query's useMutation
    return useMutation(createProject);
};