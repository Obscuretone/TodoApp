import { useQuery } from '@tanstack/react-query';
import { useAxios } from '../hooks/useAxios'; // Import the custom Axios hook

export const useGetTasks = () => {
    const axiosInstance = useAxios(); // Get the Axios instance with middleware

    return useQuery({
        queryKey: ['tasks'], // The query key
        queryFn: async () => {
            const { data } = await axiosInstance.get('/tasks'); // Use Axios instance to make the request
            return data.tasks || []; // Ensure it returns tasks
        },
    });
};