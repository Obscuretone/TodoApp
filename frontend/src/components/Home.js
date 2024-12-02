import React, { useState } from 'react';
import { Button } from 'react-bootstrap'; // Import Bootstrap components
import { Link } from 'react-router-dom'; // Import Link component for navigation
import LoginModal from './LoginModal'; // Import the LoginModal component

const Home = () => {
    const [showModal, setShowModal] = useState(false); // Modal visibility state

    const authToken = localStorage.getItem('authToken'); // Get auth token

    return (
        <div>
            {/* Hero Section */}
            <section className="hero bg-primary text-white text-center py-5">
                <div className="container">
                    <h1 className="display-4 mb-4">AI Task Splitting Application</h1>
                    <p className="lead mb-4">
                        This demo application helps you organize and split your tasks with the power of AI. Effortlessly divide your projects into manageable chunks.
                    </p>

                    {/* Button or Link */}
                    {authToken ? (
                        // If user is logged in, navigate to the Tasks page
                        <Link to="/projects">
                            <Button variant="light" className="btn-lg">
                                Go to Projects
                            </Button>
                        </Link>
                    ) : (
                        // If user is not logged in, show Login/Register button
                        <Button variant="light" onClick={() => setShowModal(true)} className="btn-lg">
                            Login/Register
                        </Button>
                    )}
                </div>
            </section>

            {/* Conditionally render LoginModal */}
            {showModal && <LoginModal onClose={() => setShowModal(false)} />}

            {/* Additional Section */}
            <section className="features py-5 bg-light">
                <div className="container text-center">
                    <h2 className="mb-4">Features</h2>
                    <div className="row">
                        <div className="col-md-4 mb-4">
                            <img src="https://picsum.photos/200?random=1" alt="Feature 1" className="img-fluid rounded mb-3" />
                            <h4>AI-powered Task Splitter</h4>
                            <p>Split complex tasks into smaller, manageable chunks with AI assistance.</p>
                        </div>
                        <div className="col-md-4 mb-4">
                            <img src="https://picsum.photos/200?random=2" alt="Feature 2" className="img-fluid rounded mb-3" />
                            <h4>Smart Task Management</h4>
                            <p>Keep track of your tasks, deadlines, and priorities with ease.</p>
                        </div>
                        <div className="col-md-4 mb-4">
                            <img src="https://picsum.photos/200?random=3" alt="Feature 3" className="img-fluid rounded mb-3" />
                            <h4>Simple and Intuitive UI</h4>
                            <p>Our interface is designed to be simple, intuitive, and user-friendly.</p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Home;