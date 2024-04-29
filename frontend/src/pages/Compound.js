import React from 'react';
import LineGraph from '../Components/LineGraph';
import MarketTable from '../Components/MarketTable';
import '../styles/style.css';
import { Container } from 'react-bootstrap';

const Compound = () => (
    <div id="page-formatting">
        <Container>
            <div className="page">
                <br />
                {/* Market-specific content */}
                <h1>Compound Overview</h1>
                <LineGraph market="COMPOUND" timeframe={365} subtitle={"Historical Compound Open Interest"} />
                {/* Any additional content */}
                <MarketTable />
                <br />
            </div>
        </Container>
    </div>
);

export default Compound;