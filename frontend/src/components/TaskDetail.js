import React from 'react';

const TaskDetail = ({ taskDetails, navigate }) => {
    return (
        <>
            <h1>{taskDetails.title || "No title available"}</h1>
            <p>{taskDetails.description || "No description available"}</p>
            <p>Created: {taskDetails.created_at || "No creation date available"}</p>
        </>
    );
};

export default TaskDetail;