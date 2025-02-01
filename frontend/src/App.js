import React from 'react';
import './App.css';
import CustomerDashboard from './components/CustomerDashboard';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to the Customer Management System</h1>
      </header>
      <main>
        <CustomerDashboard />
      </main>
    </div>
  );
}

export default App;