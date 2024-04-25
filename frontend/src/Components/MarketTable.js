import React from 'react';

const MarketTable = () => (
    // Render the market table as in Pages.js
    <table>
        <tr>
            <td>
                <div className="thead">
                    Protocol
                </div>
            </td>
            <td>
                <div className="thead">
                    URL
                </div>
            </td>
            <td>
                <div className="thead">
                    Total Supplied
                </div>
            </td>
            <td>
                <div className="thead">
                    Total Borrowed
                </div>
            </td>
            <td>
                <div className="thead">
                    Supply APY
                </div>
            </td>
        </tr>
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
                <a href="https://app.compound.finance/markets/weth-mainnet">Compound</a>
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
                <a href="https://app.uniswap.org/explore/tokens/ethereum/0xae78736cd615f374d3085123a210448e74fc6393">Uniswap</a>
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
    </table>
);

export default MarketTable;
