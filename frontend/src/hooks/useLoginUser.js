import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const useLoginUser = () => {
    return useMutation({
        mutationFn: async ({ email, password }) => {
            console.log('Logging in with:', { email, password });
            try {
                const response = await axios.post(`${apiUrl}/auth/login`, { email, password });
                console.log('Login successful:', response.data);
                return response.data;
            } catch (error) {
                console.error('Login failed:', error);
                throw new Error('Login failed. Please check your credentials and try again.');
            }
        }
    });
};