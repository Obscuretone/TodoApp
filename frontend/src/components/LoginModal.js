import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLoginUser } from '../hooks/useLoginUser';
import { useRegisterUser } from '../hooks/useRegisterUser';

const LoginModal = ({ onClose }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const { mutateAsync: login, isLoading: loginLoading } = useLoginUser();
    const { mutateAsync: register, isLoading: registerLoading } = useRegisterUser();

    const handleLoginSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        if (!email || !password) {
            setError('Please provide both email and password.');
            return;
        }

        console.log("Login");

        try {
            const response = await login({ email, password });
            console.log("Login response:", response);

            if (response.token) {
                localStorage.setItem('authToken', response.token);
                navigate('/tasks');
                onClose();
            } else {
                throw new Error('No token received');
            }
        } catch (err) {
            console.error('Login failed:', err);
            setError('Login failed. Please check your credentials and try again.');
        }
    };

    const handleRegisterSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        if (!username || !email || !password) {
            setError('All fields are required.');
            return;
        }

        try {
            await register({ username, email, password });
            navigate('/');
            onClose();
        } catch (err) {
            console.error('Registration failed:', err);
            setError('Registration failed. Please try again.');
        }
    };

    return (
        <div className="modal show d-block" tabIndex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title" id="exampleModalLabel">{isLogin ? 'Login' : 'Register'}</h5>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close" onClick={onClose}></button>
                    </div>
                    <div className="modal-body">
                        {error && <p style={{ color: 'red' }}>{error}</p>}
                        <form onSubmit={isLogin ? handleLoginSubmit : handleRegisterSubmit}>
                            {!isLogin && (
                                <div className="mb-3">
                                    <label htmlFor="username" className="form-label">Username</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="username"
                                        value={username}
                                        onChange={(e) => setUsername(e.target.value)}
                                        required
                                    />
                                </div>
                            )}
                            <div className="mb-3">
                                <label htmlFor="email" className="form-label">Email address</label>
                                <input
                                    type="email"
                                    className="form-control"
                                    id="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="mb-3">
                                <label htmlFor="password" className="form-label">Password</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    id="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                            </div>
                            <button type="submit" className="btn btn-primary" disabled={loginLoading || registerLoading}>
                                {isLogin ? (loginLoading ? 'Logging in...' : 'Login') : (registerLoading ? 'Registering...' : 'Register')}
                            </button>
                        </form>
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-secondary" onClick={onClose}>Close</button>
                        <button
                            type="button"
                            className="btn btn-link"
                            onClick={() => setIsLogin(!isLogin)}
                        >
                            {isLogin ? 'Create an account' : 'Already have an account? Login'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoginModal;