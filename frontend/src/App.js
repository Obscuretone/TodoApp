import React from 'react';
import { Routes, Route, BrowserRouter, Navigate } from 'react-router-dom';
import Home from './components/Home';
import TasksPage from './components/TasksPage';
import TaskPage from './components/TaskPage';
import ProjectList from './components/ProjectList';
import Layout from './components/Layout'; // Import Layout component for sidebar
import Logout from './components/Logout'; // Import the Logout component

// Protected Route Wrapper
const ProtectedRoute = ({ children }) => {
  const authToken = localStorage.getItem("authToken");
  return authToken ? children : <Navigate to="/login" replace />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Home />} />

        {/* Authenticated Routes */}
        <Route
          path="/projects"
          element={
            <ProtectedRoute>
              <Layout>
                <ProjectList />
              </Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/tasks"
          element={
            <ProtectedRoute>
              <Layout>
                <TasksPage />
              </Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/tasks/:taskId"
          element={
            <ProtectedRoute>
              <Layout>
                <TaskPage />
              </Layout>
            </ProtectedRoute>
          }
        />

        {/* Logout Route */}
        <Route path="/logout" element={<Logout />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;