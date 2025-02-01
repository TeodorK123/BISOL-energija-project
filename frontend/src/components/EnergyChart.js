import React from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

const EnergyChart = ({ energyData, sipxPrices }) => {
  // Debugging: Log the raw data
  console.log('Energy Data:', energyData);
  console.log('SIPX Prices:', sipxPrices);

  const labels = energyData.map(data => new Date(data.timestamp_utc).toLocaleString());
  const consumedData = energyData.map(data => data.cons_kwh);
  const producedData = energyData.map(data => data.prod_kwh);
  const sipxPriceData = sipxPrices.map(price => price.price_eur_per_kwh);

  // Calculate profit and cost
  const profitData = energyData.map(data => {
    const price = sipxPrices.find(price => new Date(price.timestamp_utc).getTime() === new Date(data.timestamp_utc).getTime());
    return price ? data.prod_kwh * price.price_eur_per_kwh : 0;
  });

  const costData = energyData.map(data => {
    const price = sipxPrices.find(price => new Date(price.timestamp_utc).getTime() === new Date(data.timestamp_utc).getTime());
    return price ? data.cons_kwh * price.price_eur_per_kwh : 0;
  });

  // Debugging: Log the processed data
  console.log('Labels:', labels);
  console.log('Consumed Data:', consumedData);
  console.log('Produced Data:', producedData);
  console.log('SIPX Price Data:', sipxPriceData);
  console.log('Profit Data:', profitData);
  console.log('Cost Data:', costData);

  const data = {
    labels: labels,
    datasets: [
      {
        label: 'Energy Consumed (kWh)',
        data: consumedData,
        borderColor: 'rgba(75,192,192,1)',
        fill: false,
      },
      {
        label: 'Energy Produced (kWh)',
        data: producedData,
        borderColor: 'rgba(153,102,255,1)',
        fill: false,
      },
      {
        label: 'SIPX Price (EUR)',
        data: sipxPriceData,
        borderColor: 'rgba(255,99,132,1)',
        fill: false,
      },
      {
        label: 'Profit (EUR)',
        data: profitData,
        borderColor: 'rgba(54,162,235,1)',
        fill: false,
      },
      {
        label: 'Cost (EUR)',
        data: costData,
        borderColor: 'rgba(255,206,86,1)',
        fill: false,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
  };

  return (
    <div className="chart-container" style={{ position: 'relative', height: '60vh', width: '100%' }}>
      <Line data={data} options={options} />
    </div>
  );
};

export default EnergyChart;