import { useQuery } from '@tanstack/react-query';
import { useAxios } from './useAxios'; // Import the custom Axios hook

export const useGetProjects = () => {
    const axiosInstance = useAxios(); // Get the Axios instance with middleware

    return useQuery({
        queryKey: ['projects'], // The query key
        queryFn: async () => {
            const { data } = await axiosInstance.get('/projects'); // Use Axios instance to make the request
            console.log(data)
            return data || []; // Ensure it returns projects
        },
    });
};