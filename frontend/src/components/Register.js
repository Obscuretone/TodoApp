// src/components/Register.js
import React, { useState } from 'react';
import { useRegisterUser } from '../api';  // Import the custom hook for registration
import { useNavigate } from 'react-router-dom';

const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const { mutateAsync, isLoading } = useRegisterUser(); // Get mutate function from React Query

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null); // Reset error message

        if (!username || !email || !password) {
            setError('All fields are required.');
            return;
        }

        try {
            const response = await mutateAsync({ username, email, password });
            console.log('Registration successful:', response);
            // Redirect to login page after successful registration
            navigate('/login');
        } catch (err) {
            console.error('Registration error:', err);
            setError('Registration failed. Please try again.');
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Registering...' : 'Register'}
                </button>
            </form>
        </div>
    );
};

export default Register;