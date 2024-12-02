import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import jwtDecode from 'jwt-decode';

const isTokenExpired = (token) => {
    try {
        const { exp } = jwtDecode(token);
        return Date.now() >= exp * 1000;
    } catch {
        return true;
    }
};

const AuthGuard = ({ children }) => {
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('authToken');
        if (!token || isTokenExpired(token)) {
            localStorage.removeItem('authToken');
            navigate('/login');
        }
    }, [navigate]);

    return <>{children}</>;
};

export default AuthGuard;