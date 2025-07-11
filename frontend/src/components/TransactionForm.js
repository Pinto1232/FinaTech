import React, { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001/api';

function TransactionForm({ users, onTransactionCreated }) {
  const [formData, setFormData] = useState({
    user_id: '',
    amount: '',
    type: 'deposit'
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await axios.post(`${API_BASE_URL}/transactions`, {
        ...formData,
        amount: parseFloat(formData.amount)
      });
      
      setMessage('Transaction created successfully!');
      setFormData({ user_id: '', amount: '', type: 'deposit' });
      
      if (onTransactionCreated) {
        onTransactionCreated({
          id: response.data.id,
          ...formData,
          amount: parseFloat(formData.amount),
          created_at: new Date().toISOString()
        });
      }
    } catch (error) {
      setMessage(error.response?.data?.error || 'Failed to create transaction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {message && (
        <div className={message.includes('successfully') ? 'success' : 'error'}>
          {message}
        </div>
      )}
      
      <div className="form-group">
        <label htmlFor="user_id">User:</label>
        <select
          id="user_id"
          name="user_id"
          value={formData.user_id}
          onChange={handleChange}
          required
          disabled={loading}
        >
          <option value="">Select a user</option>
          {users.map(user => (
            <option key={user.id} value={user.id}>
              {user.name} ({user.email})
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="amount">Amount:</label>
        <input
          type="number"
          id="amount"
          name="amount"
          value={formData.amount}
          onChange={handleChange}
          step="0.01"
          min="0"
          required
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="type">Transaction Type:</label>
        <select
          id="type"
          name="type"
          value={formData.type}
          onChange={handleChange}
          required
          disabled={loading}
        >
          <option value="deposit">Deposit</option>
          <option value="withdrawal">Withdrawal</option>
          <option value="transfer">Transfer</option>
          <option value="payment">Payment</option>
        </select>
      </div>

      <button type="submit" className="btn" disabled={loading || !users.length}>
        {loading ? 'Creating...' : 'Create Transaction'}
      </button>
      
      {!users.length && (
        <p style={{ marginTop: '10px', color: '#6c757d', fontSize: '0.9rem' }}>
          Please create a user first to enable transactions.
        </p>
      )}
    </form>
  );
}

export default TransactionForm;