import React, { useState } from 'react';
import { Container } from 'react-bootstrap';
import LineGraph from '../components/Graph/LineGraph';
import NavBar from '../components/Navigation/NavBar';
import './style.css'; // Assuming style.css is moved to assets/styles

const HomePage = () => {
    const [showpage, setShowpage] = useState(1);

    const handlepage = (e) => setShowpage(e);

    return (
        <div id="page-formatting">
            <NavBar showpage={showpage} handlepage={handlepage} />
            <Container>
                <div className="page">
                    {/* Page content goes here, using showpage to conditionally render components */}
                </div>
            </Container>
        </div>
    );
};

export default HomePage;
