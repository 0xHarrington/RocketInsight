import React from 'react';
import LineGraph from '../Components/LineGraph';
import MarketTable from '../Components/MarketTable';
import '../styles/style.css';
import { Container } from 'react-bootstrap';

const MarketPage = () => (
    <div id="page">
        <Container>
            <br />
            {/* Market-specific content */}
            <h1>Market Overview</h1>
            <LineGraph />
            {/* Any additional content */}
            <MarketTable />
            <br />
        </Container>        
    </div>
);

export default MarketPage;
