import React from 'react';
import LineGraph from '../Components/LineGraph';
import MarketTable from '../Components/MarketTable';
import '../styles/style.css';
import { Container } from 'react-bootstrap';

const Prisma = () => (
    <div id="page-formatting">
        <Container>
            <div className="page">
                <br />
                {/* Market-specific content */}
                <h1>Prisma Overview</h1>
                <LineGraph market="PRISMA" timeframe={365} subtitle={"Historical Prisma Open Interest"} />
                {/* Any additional content */}
                <MarketTable />
                <br />
            </div>
        </Container>
    </div>
);

export default Prisma;