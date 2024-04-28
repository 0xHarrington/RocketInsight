import React from 'react';
import WalletClustering from '../Components/WalletClustering';
import NetworkGraph from '../Components/network';
import WalletTable from '../Components/WalletTable';
import { Container } from 'react-bootstrap';
import '../styles/style.css';

const WalletPage = () => (
    <div id="page">
        <Container>
            <h1>Wallet address clustering</h1>
            <NetworkGraph />
            <WalletTable />
            <br />
        </Container>
    </div>
);

export default WalletPage;
