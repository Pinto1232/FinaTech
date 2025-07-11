import React from 'react';

function ConnectionStatus({ isConnected }) {
  return (
    <div style={{ marginTop: '1rem', fontSize: '0.9rem' }}>
      <span 
        className={`status-indicator ${isConnected ? 'status-connected' : 'status-disconnected'}`}
      ></span>
      WebSocket: {isConnected ? 'Connected' : 'Disconnected'}
    </div>
  );
}

export default ConnectionStatus;