import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Aave from './pages/Aave';
import Prisma from './pages/Prisma';
import Compound from './pages/Compound';
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
          <Route path="/markets/aave" element={<Aave />} />
          <Route path="/markets/compound" element={<Compound />} />
          <Route path="/markets/prisma" element={<Prisma />} />
          <Route path="/wallets" element={<WalletPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
