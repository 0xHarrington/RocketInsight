import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import MarketAnalysis from './components/MarketAnalysis';
import UserInsights from './components/UserInsights';

function App() {
  return (
    <Router>
      <div>
        {/* Navigation Links can be added here */}
        <Switch>
          <Route path="/" exact component={Dashboard} />
          <Route path="/market-analysis" component={MarketAnalysis} />
          <Route path="/user-insights" component={UserInsights} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
