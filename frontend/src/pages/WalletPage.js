import React from 'react';
import WalletClustering from '../Components/WalletClustering';
import WalletTable from '../Components/WalletTable';
import { Container } from 'react-bootstrap';

const WalletPage = () => (
    <div>
        <Container>
            <h1>Wallet address clustering</h1>
            <WalletClustering />
            <WalletTable />
        </Container>
    </div>
);

export default WalletPage;
