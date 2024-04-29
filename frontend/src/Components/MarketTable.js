import React from 'react';
import Table from 'react-bootstrap/Table';

const MarketTable = () => (
    // Render the market table as in Pages.js
    <Table striped bordered variant="dark">
        <thead>
            <tr>
                <td>
                    Protocol
                </td>
                <td>
                    Total Supplied
                </td>
                <td>
                    Total Borrowed
                </td>
                <td>
                    Supply APY
                </td>
                <td>
                    Borrow APY
                </td>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><a href="https://app.aave.com/reserve-overview/?underlyingAsset=0xae78736cd615f374d3085123a210448e74fc6393&marketName=proto_mainnet_v3">AAVE</a></td>
                <td>
                    47.68K
                </td>
                <td>
                    74.86K
                </td>
                <td>
                    0.01%
                </td>
                <td>
                    0.01%
                </td>
            </tr>
            <tr>
                <td>
                    <   a href="https://app.compound.finance/markets/weth-mainnet">Compound</a>
                </td>
                <td>
                    47.68K
                </td>
                <td>
                    74.86K
                </td>
                <td>
                    0.01%
                </td>
                <td>
                    0.01%
                </td>
            </tr>
            <tr>
                <td>
                    <a href="https://app.uniswap.org/explore/tokens/ethereum/0xae78736cd615f374d3085123a210448e74fc6393">Prisma</a>
                </td>
                <td>
                    47.68K
                </td>
                <td>
                    74.86K
                </td>
                <td>
                    0.01%
                </td>
                <td>
                    0.01%
                </td>
            </tr>
        </tbody>
    </Table>
);

export default MarketTable;
