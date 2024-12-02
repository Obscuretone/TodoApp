import { useNavigate } from 'react-router-dom';
import { createAxiosInstance } from '../api/axiosInstance';

export const useAxios = () => {
    const navigate = useNavigate();
    return createAxiosInstance(navigate);
};