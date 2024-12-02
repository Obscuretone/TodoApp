import React from 'react';
import { Button, Form } from 'react-bootstrap';

const SplitTaskForm = ({ taskId, splitCount, setSplitCount, isSplitting, splitTask }) => {
    const handleSplitTask = () => {
        if (splitCount < 1 || splitCount > 5) {
            alert('You can only split the task into 1 to 5 subtasks.');
            return;
        }

        splitTask({
            taskId: taskId,
            splitCount: splitCount,
        }, {
            onSuccess: (data) => {
                alert(`${splitCount} subtasks created successfully.`);
            },
            onError: (error) => {
                console.error('Error splitting task:', error);
                alert('Failed to split the task. Please try again.');
            },
        });
    };

    return (
        <Form>
            <Form.Group controlId="splitCount" className="mb-3">
                <Form.Label>Max of Subtasks to Generate</Form.Label>
                <Form.Control
                    type="number"
                    value={splitCount}
                    onChange={(e) => setSplitCount(Number(e.target.value))}
                    min="1"
                    max="5"
                />
            </Form.Group>
            <Button variant="primary" onClick={handleSplitTask} disabled={isSplitting}>
                {isSplitting ? 'Splitting...' : `Split Task into ${splitCount} Subtask${splitCount > 1 ? 's' : ''}`}
            </Button>
        </Form>
    );
};

export default SplitTaskForm;