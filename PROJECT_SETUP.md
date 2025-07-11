# FinaTech - Event-Driven Architecture Setup

This project implements an Event-Driven Architecture using Python (Flask) for the backend, React.js for the frontend, and Microsoft SQL Server as the database.

## Architecture Overview

### Event-Driven Architecture Components

1. **Event Bus**: Central component that handles event publishing and subscription
2. **Event Queue**: Manages event processing in the background
3. **Event Handlers**: Process specific types of events
4. **WebSocket Integration**: Real-time event broadcasting to frontend
5. **Database Event Store**: Persists all events for audit and replay

### Technology Stack

- **Backend**: Python 3.8+, Flask, Flask-SocketIO, pyodbc
- **Frontend**: React.js 18, Socket.IO Client, Axios
- **Database**: Microsoft SQL Server
- **Real-time Communication**: WebSockets via Socket.IO

## Prerequisites

### 1. Python Environment
- Python 3.8 or higher
- pip package manager

### 2. Node.js Environment
- Node.js 16 or higher
- npm package manager

### 3. Microsoft SQL Server
- SQL Server 2017 or higher (Express edition is sufficient)
- SQL Server Management Studio (SSMS) or Azure Data Studio
- ODBC Driver 17 for SQL Server

## Setup Instructions

### 1. Database Setup

1. **Install SQL Server** (if not already installed)
   - Download SQL Server Express from Microsoft
   - Install with default settings
   - Note the server name (usually `localhost` or `.\SQLEXPRESS`)

2. **Create Database**
   ```sql
   -- Run this in SQL Server Management Studio
   -- File: backend/database_setup.sql
   ```

3. **Configure Database Connection**
   - Copy `backend/.env.example` to `backend/.env`
   - Update database credentials in `.env` file

### 2. Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   # Copy and edit the environment file
   copy .env.example .env
   # Edit .env with your database credentials
   ```

6. **Run the backend server**
   ```bash
   python app.py
   ```

   The backend will start on `http://localhost:5000`

### 3. Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

   The frontend will start on `http://localhost:3000`

## Project Structure

```
FinaTech/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration management
│   ├── requirements.txt       # Python dependencies
│   ├── database_setup.sql     # Database schema
│   └── .env.example          # Environment variables template
├── frontend/
│   ├── public/
│   │   └── index.html        # HTML template
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── UserForm.js
│   │   │   ├── TransactionForm.js
│   │   │   ├── UserList.js
│   │   │   ├── EventLog.js
│   │   │   └── ConnectionStatus.js
│   │   ├── App.js           # Main React component
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Global styles
│   └── package.json         # Node.js dependencies
└── PROJECT_SETUP.md         # This file
```

## Event-Driven Architecture Features

### 1. Event Types
- `user_created`: Triggered when a new user is created
- `transaction_processed`: Triggered when a transaction is processed

### 2. Event Flow
1. User action triggers an API call
2. Backend processes the request
3. Event is published to the Event Bus
4. Event handlers process the event
5. Event is stored in the database
6. Real-time notification sent to frontend via WebSocket

### 3. Real-time Features
- Live event log in the frontend
- WebSocket connection status indicator
- Automatic UI updates when events occur

## API Endpoints

### Health Check
- `GET /api/health` - Check API status

### Users
- `GET /api/users` - Get all users
- `POST /api/users` - Create a new user

### Transactions
- `POST /api/transactions` - Create a new transaction

### Events
- `GET /api/events` - Get all events

## WebSocket Events

### Client to Server
- `connect` - Client connection
- `disconnect` - Client disconnection

### Server to Client
- `event` - Real-time event broadcast
- `message` - Server messages

## Testing the Application

1. **Start both backend and frontend servers**
2. **Open browser to `http://localhost:3000`**
3. **Test the event-driven flow:**
   - Create a user → Watch for `user_created` event
   - Create a transaction → Watch for `transaction_processed` event
   - Observe real-time updates in the Event Log

## Troubleshooting

### Database Connection Issues
- Verify SQL Server is running
- Check connection string in `.env` file
- Ensure ODBC Driver 17 is installed
- Test connection with SQL Server Management Studio

### Backend Issues
- Check Python version (3.8+)
- Verify all dependencies are installed
- Check console for error messages
- Ensure port 5000 is not in use

### Frontend Issues
- Check Node.js version (16+)
- Verify npm dependencies are installed
- Check browser console for errors
- Ensure port 3000 is not in use

### WebSocket Connection Issues
- Verify backend is running on port 5000
- Check browser network tab for WebSocket connection
- Ensure CORS is properly configured

## Next Steps

1. **Add Authentication**: Implement user authentication and authorization
2. **Event Replay**: Add functionality to replay events from the event store
3. **Event Sourcing**: Implement full event sourcing pattern
4. **Microservices**: Split into multiple microservices
5. **Message Queue**: Add Redis or RabbitMQ for better event handling
6. **Monitoring**: Add logging, metrics, and health checks
7. **Testing**: Add unit tests and integration tests

## Security Considerations

1. **Environment Variables**: Never commit `.env` files to version control
2. **Database Security**: Use strong passwords and proper user permissions
3. **API Security**: Add rate limiting and input validation
4. **CORS**: Configure CORS properly for production
5. **HTTPS**: Use HTTPS in production environments