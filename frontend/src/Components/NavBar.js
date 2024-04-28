import React from 'react';
import { Link } from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

function Navigation() {
    return (
  
            <Navbar expand="lg" className="bg-body-tertiary" data-bs-theme="dark">
                <Container fluid>
                    <Navbar.Brand as={Link} to="/" >RocketInsight</Navbar.Brand>
                    <Navbar.Toggle aria-controls="navbarScroll" />
                    <Navbar.Collapse id="navbarScroll">
                        <Nav
                            className="me-auto my-2 my-lg-0"
                            style={{ maxHeight: '100px' }}
                            navbarScroll
                        >

                            <NavDropdown title="Markets" id="marketDropdown">
                                <NavDropdown.Item as={Link} to="/markets/aave" >Aave</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to="/markets/compound" >
                                    Compound
                                </NavDropdown.Item>
                                <NavDropdown.Item as={Link} to="/markets/prisma">
                                    Prisma
                                </NavDropdown.Item>
                            </NavDropdown>
                            <Nav.Link as={Link} to="/wallets">Wallets</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>

    );        
}


export default Navigation;