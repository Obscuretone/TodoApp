import React from 'react';
import './Header.css'; // Import your styles for the header

const Header = () => {
    return (
        <header className="app-header">
            <img id="cbc_gem" src="https://site-cbc.radio-canada.ca/media/4616/imagesgem-menu-guide-line.png" />
            <h1>Todo App</h1>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/tasks">Tasks</a></li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;
