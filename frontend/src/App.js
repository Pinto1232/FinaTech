import React, { useState, useEffect } from 'react';
import axios from 'axios';
import io from 'socket.io-client';
import UserForm from './components/UserForm';
import TransactionForm from './components/TransactionForm';
import UserList from './components/UserList';
import EventLog from './components/EventLog';
import ConnectionStatus from './components/ConnectionStatus';

const API_BASE_URL = 'http://localhost:5001/api';

function App() {
  const [users, setUsers] = useState([]);
  const [events, setEvents] = useState([]);
  const [socket, setSocket] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Initialize socket connection
    const newSocket = io('http://localhost:5001');
    setSocket(newSocket);

    // Socket event handlers
    newSocket.on('connect', () => {
      setIsConnected(true);
      console.log('Connected to server');
    });

    newSocket.on('disconnect', () => {
      setIsConnected(false);
      console.log('Disconnected from server');
    });

    newSocket.on('event', (event) => {
      setEvents(prevEvents => [event, ...prevEvents]);
    });

    newSocket.on('message', (data) => {
      console.log('Server message:', data);
    });

    // Load initial data
    loadUsers();
    loadEvents();

    return () => {
      newSocket.close();
    };
  }, []);

  const loadUsers = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/users`);
      setUsers(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load users');
      console.error('Error loading users:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadEvents = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/events`);
      setEvents(response.data);
    } catch (err) {
      console.error('Error loading events:', err);
    }
  };

  const handleUserCreated = (newUser) => {
    setUsers(prevUsers => [...prevUsers, newUser]);
  };

  const handleTransactionCreated = (transaction) => {
    console.log('Transaction created:', transaction);
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading FinaTech application...</div>
      </div>
    );
  }

  return (
    <div className="container">
      <header className="header">
        <h1>FinaTech</h1>
        <p>Event-Driven Financial Technology Platform</p>
        <ConnectionStatus isConnected={isConnected} />
      </header>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      <div className="dashboard">
        <div className="card">
          <h2>Create User</h2>
          <UserForm onUserCreated={handleUserCreated} />
        </div>

        <div className="card">
          <h2>Create Transaction</h2>
          <TransactionForm 
            users={users} 
            onTransactionCreated={handleTransactionCreated} 
          />
        </div>

        <div className="card">
          <h2>Users</h2>
          <UserList users={users} />
        </div>

        <div className="card">
          <h2>Real-time Events</h2>
          <EventLog events={events} />
        </div>
      </div>
    </div>
  );
}

export default App;