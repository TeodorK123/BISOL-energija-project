import React, { useState, useEffect } from 'react';
import axios from 'axios';
import IntervalSelector from './IntervalSelector';
import EnergyChart from './EnergyChart';

const CustomerDashboard = () => {
  const [customers, setCustomers] = useState([]);
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [interval, setInterval] = useState({ start: '', end: '' });
  const [energyData, setEnergyData] = useState([]);
  const [sipxPrices, setSipxPrices] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    axios.get('http://localhost:8000/customers/')
      .then(response => {
        setCustomers(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the customers!', error);
      });
  }, []);

  useEffect(() => {
    if (selectedCustomer && interval.start && interval.end) {
      setError('');
      axios.get(`http://localhost:8000/energy_data/customer/${selectedCustomer}/range`, {
        params: {
          start_timestamp: interval.start,
          end_timestamp: interval.end
        }
      })
      .then(response => {
        setEnergyData(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the energy data!', error);
        setError('No energy data found for the selected time range.');
      });

      axios.get(`http://localhost:8000/sipx_prices/range`, {
        params: {
          start_timestamp: interval.start,
          end_timestamp: interval.end
        }
      })
      .then(response => {
        setSipxPrices(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the SIPX prices!', error);
        setError('No SIPX prices found for the selected time range.');
      });
    }
  }, [selectedCustomer, interval]);

  return (
    <div className="container">
      <h2>Customer Dashboard</h2>
      <div className="form-group">
        <label htmlFor="customerSelect">Select Customer:</label>
        <select
          id="customerSelect"
          className="form-control"
          onChange={(e) => setSelectedCustomer(e.target.value)}
        >
          <option value="">Select a customer</option>
          {customers.map(customer => (
            <option key={customer.id} value={customer.id}>
              {customer.name}
            </option>
          ))}
        </select>
      </div>
      <IntervalSelector setInterval={setInterval} />
      {error && <div className="alert alert-danger mt-4">{error}</div>}
      <div className="row mt-4">
        <div className="col-12">
          <EnergyChart energyData={energyData} sipxPrices={sipxPrices} />
        </div>
      </div>
    </div>
  );
};

export default CustomerDashboard;