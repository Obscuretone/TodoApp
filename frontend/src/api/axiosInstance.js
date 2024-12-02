import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Helper to check token expiration
const isTokenExpired = (token) => {
    try {
        const { exp } = jwtDecode(token);
        return Date.now() >= exp * 1000; // Check if current time is after expiration
    } catch (e) {
        return true; // Assume invalid or expired if decode fails
    }
};

export const createAxiosInstance = (navigate) => {
    const axiosInstance = axios.create({
        baseURL: apiUrl,
    });

    // Add request interceptor to inject token
    axiosInstance.interceptors.request.use(
        (config) => {
            const token = localStorage.getItem('authToken');
            if (token) {
                if (isTokenExpired(token)) {
                    localStorage.removeItem('authToken');
                    navigate('/'); // Redirect to login if expired
                    return Promise.reject(new Error('Token expired'));
                }
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        },
        (error) => Promise.reject(error)
    );

    return axiosInstance;
};