import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const useRegisterUser = () => {
    return useMutation({
        mutationFn: async ({ username, email, password }) => {
            console.log('Registering user with:', { username, email, password });
            try {
                const response = await axios.post(`${apiUrl}/auth/register`, { username, email, password });
                console.log('Registration successful:', response.data);
                return response.data;
            } catch (error) {
                console.error('Registration failed:', error);
                throw new Error('Registration failed. Please try again.');
            }
        }
    });
};