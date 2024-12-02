import React from 'react';
import Sidebar from './Sidebar';
import { Container, Row, Col } from 'react-bootstrap';

const Layout = ({ children }) => {
    return (
        <Container fluid>
            <Row>
                {/* Sidebar Column */}
                <Col xs={3} md={2} className="bg-light p-0">
                    <Sidebar />
                </Col>

                {/* Main Content Column */}
                <Col xs={9} md={10} className="p-4">
                    {children}
                </Col>
            </Row>
        </Container>
    );
};

export default Layout;