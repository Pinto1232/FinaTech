import React from 'react';

function EventLog({ events }) {
  if (!events || events.length === 0) {
    return (
      <div className="loading">
        No events yet. Create users or transactions to see real-time events!
      </div>
    );
  }

  const formatEventData = (data) => {
    if (typeof data === 'object') {
      return Object.entries(data).map(([key, value]) => (
        <span key={key}>
          <strong>{key}:</strong> {value.toString()}{' '}
        </span>
      ));
    }
    return data.toString();
  };

  const formatTimestamp = (timestamp) => {
    try {
      return new Date(timestamp).toLocaleString();
    } catch {
      return timestamp;
    }
  };

  return (
    <div className="event-log">
      {events.map((event, index) => (
        <div key={event.id || index} className="event-item">
          <div className="event-type">{event.type}</div>
          <div style={{ margin: '0.5rem 0', fontSize: '0.9rem' }}>
            {formatEventData(event.data)}
          </div>
          <div className="event-time">
            {formatTimestamp(event.timestamp)}
          </div>
        </div>
      ))}
    </div>
  );
}

export default EventLog;