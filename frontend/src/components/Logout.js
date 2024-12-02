import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // For redirecting the user after logout

const Logout = () => {
    const navigate = useNavigate();

    useEffect(() => {
        // Clear authentication token or session data
        localStorage.removeItem('authToken'); // Adjust based on where you store the token

        // Optionally, clear other related data
        // localStorage.removeItem('userDetails');
        // sessionStorage.removeItem('userDetails');

        // Call backend API if you need to invalidate the session
        // Example: logoutUserFromBackend();

        // Redirect user to the login page after logout
        navigate('/'); // Or wherever you want to redirect
    }, [navigate]);

    return (
        <div>
            <p>Logging you out...</p>
        </div>
    );
};

export default Logout;