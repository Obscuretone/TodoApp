import React from 'react';
import { Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Sidebar = () => {
    return (
        <div className="d-flex flex-column vh-100 bg-light border-end" style={{ width: '250px' }}>
            <h4 className="p-3">Task Manager</h4>
            <Nav className="flex-column">
                <Nav.Link as={Link} to="/projects">Projects</Nav.Link>
            </Nav>
            <Nav className="flex-column">
                <Nav.Link as={Link} to="/logout">Logout</Nav.Link>
            </Nav>
        </div>
    );
};

export default Sidebar;