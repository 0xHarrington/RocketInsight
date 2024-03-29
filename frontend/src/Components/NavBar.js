import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => (
    <nav>
        <div className="marginals">
            <div className="VTEE">RocketInsight</div>
            <ul>
                <li><Link to="/markets" className="nav-link">Markets</Link></li>
                <li><Link to="/wallets" className="nav-link">Wallets</Link></li>
            </ul>
            <div className="alternative">
                <ul>
                    <li><a href="#">FAQ</a></li>
                    <li><a href="#">Contact Us</a></li>
                </ul>
            </div>
        </div>
    </nav>
);

export default NavBar;
