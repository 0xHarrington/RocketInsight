import React from 'react';
import WalletDetails from '../Components/WalletDetails';
import WalletTable from '../Components/WalletTable';

const WalletPage = () => (
    <div>
        <h1>Wallet address clustering</h1>
        <WalletDetails />
        <WalletTable />
    </div>
);

export default WalletPage;
