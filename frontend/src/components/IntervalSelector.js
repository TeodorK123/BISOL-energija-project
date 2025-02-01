import React, { useState } from 'react';

const IntervalSelector = ({ setInterval }) => {
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setInterval({ start, end });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="start">Start Date:</label>
        <input
          type="datetime-local"
          id="start"
          className="form-control"
          value={start}
          onChange={(e) => setStart(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label htmlFor="end">End Date:</label>
        <input
          type="datetime-local"
          id="end"
          className="form-control"
          value={end}
          onChange={(e) => setEnd(e.target.value)}
        />
      </div>
      <button type="submit" className="btn btn-primary">Set Interval</button>
    </form>
  );
};

export default IntervalSelector;