import React from 'react';
import TaskCard from './TaskCard';

const SubtaskList = ({ subtasks }) => (
    <>
        <h3>Subtasks</h3>
        {subtasks.length > 0 ? (
            subtasks.map((subtask) => (
                <div key={subtask.uuid} className="col-md-4 mb-3">
                    <TaskCard task={subtask} />
                </div>
            ))
        ) : (
            <p>No subtasks available.</p>
        )}
    </>
);

export default SubtaskList;