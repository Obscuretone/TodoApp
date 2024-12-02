// ConfirmationModal.js
import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const ConfirmationModal = ({ showModal, onConfirm, onCancel, message }) => {
    return (
        <Modal show={showModal} onHide={onCancel}>
            <Modal.Header closeButton>
                <Modal.Title>Confirm Action</Modal.Title>
            </Modal.Header>
            <Modal.Body>{message}</Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={onCancel}>
                    Cancel
                </Button>
                <Button variant="danger" onClick={onConfirm}>
                    Confirm
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default ConfirmationModal;