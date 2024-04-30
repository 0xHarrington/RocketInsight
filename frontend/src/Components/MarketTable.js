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
                    Total Supplied (rETH)
                </td>
                <td>
                    Total Borrowed (rETH)
                </td>
                <td>
                    Supply APR
                </td>
                <td>
                    Borrow APR
                </td>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><a href="https://app.aave.com/reserve-overview/?underlyingAsset=0xae78736cd615f374d3085123a210448e74fc6393&marketName=proto_mainnet_v3">AAVE</a></td>
                <td>
                    39.4k ($139.8M)
                </td>
                <td>
                    802.38 ($2.8M)
                </td>
                <td>
                    0.01%
                </td>
                <td>
                    0.32%
                </td>
            </tr>
            <tr>
                <td>
                    <a href="ipfs://bafybeidoerbumwzpj65fgxvylsttbucp2tvelplvz4kagjumsherdiip5m/markets/weth-mainnet">Compound</a>
                </td>
                <td>
                    152.3 ($542.67k)
                </td>
                <td>
                    N/A
                </td>
                <td>
                    1.08%
                </td>
                <td>
                    1.82%
                </td>
            </tr>
            <tr>
                <td>
                    <a href="https://app.prismafinance.com/vaults">Prisma</a>
                </td>
                <td>
                    2.57k ($9.3M)
                </td>
                <td>
                    N/A
                </td>
                <td>
                    6.6%
                </td>
                <td>
                    15%
                </td>
            </tr>
        </tbody>
    </Table>
);

export default MarketTable;
