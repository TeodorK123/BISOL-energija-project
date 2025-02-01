import React, { useState } from 'react';
import * as yup from 'yup';

const IntervalSelector = ({ setInterval }) => {
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [error, setError] = useState('');

  const schema = yup.object().shape({
    start: yup.date().required('Start date is required'),
    end: yup.date().required('End date is required').min(yup.ref('start'), 'End date cannot be before start date'),
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await schema.validate({ start, end });
      setError('');
      setInterval({ start, end });
    } catch (validationError) {
      setError(validationError.message);
    }
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
      {error && <div className="alert alert-danger">{error}</div>}
      <button type="submit" className="btn btn-primary">Set Interval</button>
    </form>
  );
};

export default IntervalSelector;