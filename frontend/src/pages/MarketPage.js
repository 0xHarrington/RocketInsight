import React from 'react';
import LineGraph from '../Components/LineGraph';
import MarketTable from '../Components/MarketTable';

const MarketPage = () => (
    <div>
        {/* Market-specific content */}
        <h1>Market Overview</h1>
        <LineGraph />
        {/* Any additional content */}
        <MarketTable />
    </div>
);

export default MarketPage;
