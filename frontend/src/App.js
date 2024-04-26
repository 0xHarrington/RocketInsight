import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MarketPage from './pages/MarketPage';
import WalletPage from './pages/WalletPage';
import HomePage from './pages/HomePage';
import Navigation from './Components/NavBar';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div>
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/markets" element={<MarketPage />} />
          <Route path="/wallets" element={<WalletPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
