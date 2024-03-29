import React from 'react';

const NavBar = ({ showpage, handlepage }) => (
    <nav>
        <div className="marginals">
            <div className="VTEE">RocketInsight</div>
            <ul>
                <li>
                    <button className={showpage === 1 ? "nav-link active" : "nav-link"} onClick={() => handlepage(1)}>Markets</button>
                </li>
                <li>
                    <button className={showpage === 2 ? "nav-link active" : "nav-link"} onClick={() => handlepage(2)}>Wallets</button>
                </li>
            </ul>
            <div className="login">
                <ul>
                    <li><a href="#">FAQ</a></li>
                    <li><a href="#">Contact Us</a></li>
                </ul>
            </div>
        </div>
    </nav>
);

export default NavBar;
