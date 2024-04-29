import React from 'react';
import LineGraph from '../Components/LineGraph';
import MarketTable from '../Components/MarketTable';
import '../styles/style.css';
import { Container } from 'react-bootstrap';

const Aave = () => (
    <div id ="page-formatting">
        <Container>
            <div className="page">
                <br />
                {/* Market-specific content */}
                <h1>Aave Overview</h1>
                <LineGraph market="AAVE" timeframe={365} />
                {/* Any additional content */}
                <MarketTable />
                <br />
                </div>
        </Container>        
    </div>
);

export default Aave;