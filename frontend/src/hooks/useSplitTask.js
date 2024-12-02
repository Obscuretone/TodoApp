import { useMutation } from '@tanstack/react-query';
import { useAxios } from './useAxios'; // Import your custom Axios hook

// Function to handle the split task API call using the Axios instance from `useAxios`
const splitTask = async ({ taskId, splitCount }, axiosInstance) => {
    // Make the API call using the Axios instance with the appropriate body
    const response = await axiosInstance.post(
        `/tasks/${taskId}/split`, // Use the relative path without the base URL
        { count: splitCount }
    );

    return response.data; // Return API response data
};

// Hook that uses the splitTask mutation with the Axios instance
export const useSplitTask = () => {
    const axiosInstance = useAxios(); // Get the Axios instance with middleware

    return useMutation({
        mutationFn: (data) => splitTask(data, axiosInstance), // Pass the `axiosInstance` to the splitTask function
    });
};