import { useQuery } from '@tanstack/react-query';
import { useAxios } from '../hooks/useAxios'; // Import the custom Axios hook

export const useGetTaskDetails = (taskId) => {
    const axiosInstance = useAxios(); // Get the Axios instance with middleware

    return useQuery({
        queryKey: ['taskDetails', taskId], // queryKey as an array
        queryFn: async () => {
            const { data } = await axiosInstance.get(`/tasks/${taskId}`); // Use axiosInstance to fetch task details
            return data; // Return task details
        },
    });
};