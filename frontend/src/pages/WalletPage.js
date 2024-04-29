import React from 'react';
import NetworkGraph from '../Components/NetworkGraph';
// import WalletTable from '../Components/WalletTable';
import { Container } from 'react-bootstrap';
import '../styles/style.css';

const WalletPage = () => (
    <div id="page">
        <Container>
            <h1>Wallet address clustering</h1>
            <div className="subheading">
                <h5>Mouse over the nodes & edges to see the users & their actions!</h5>
            </div>
            <NetworkGraph />
            {/* <WalletTable /> */}
            <br />
        </Container>
    </div>
);

export default WalletPage;
