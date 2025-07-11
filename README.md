# FinaTech - Event-Driven Financial Technology Platform

A modern financial technology application built with Event-Driven Architecture, featuring real-time event processing, WebSocket communication, and a responsive React frontend.

## 🏗️ Architecture

This project implements a comprehensive Event-Driven Architecture with:

- **Event Bus**: Central event management system
- **Real-time Communication**: WebSocket integration for live updates
- **Event Store**: Persistent event storage for audit and replay
- **Microservice-Ready**: Modular design for easy scaling

## 🚀 Technology Stack

### Backend
- **Python 3.8+** with Flask framework
- **Flask-SocketIO** for WebSocket communication
- **pyodbc** for SQL Server connectivity
- **Event-driven architecture** with custom Event Bus

### Frontend
- **React.js 18** with modern hooks
- **Socket.IO Client** for real-time communication
- **Axios** for HTTP requests
- **Responsive CSS** with modern design

### Database
- **Microsoft SQL Server** with optimized schema
- **Event sourcing** capabilities
- **Indexed tables** for performance

## 📋 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Microsoft SQL Server
- ODBC Driver 17 for SQL Server

### 1. Database Setup
```sql
-- Run the database setup script in SQL Server Management Studio
-- File: backend/database_setup.sql
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
copy .env.example .env  # Edit with your database credentials
python app.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 4. Quick Start (Windows)
```bash
# Run the development startup script
start_dev.bat
```

## 🌟 Features

### Event-Driven Architecture
- **Real-time Event Processing**: Events are processed immediately and broadcast to connected clients
- **Event Store**: All events are persisted for audit trails and potential replay
- **Scalable Design**: Easy to add new event types and handlers

### Real-time Dashboard
- **Live Event Log**: See events as they happen
- **Connection Status**: WebSocket connection monitoring
- **Responsive Design**: Works on desktop and mobile

### Financial Operations
- **User Management**: Create and manage users
- **Transaction Processing**: Handle various transaction types
- **Event Tracking**: Monitor all system activities

## 📁 Project Structure

```
FinaTech/
├── backend/                 # Python Flask backend
│   ├── app.py              # Main application with Event Bus
│   ├── config.py           # Configuration management
│   ├── requirements.txt    # Python dependencies
│   └── database_setup.sql  # Database schema
├── frontend/               # React.js frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.js         # Main application
│   │   └── index.css      # Styling
│   └── package.json       # Node.js dependencies
├── start_dev.bat          # Development startup script
└── PROJECT_SETUP.md       # Detailed setup instructions
```

## 🔄 Event Flow

1. **User Action** → API Request
2. **Backend Processing** → Database Update
3. **Event Publishing** → Event Bus
4. **Event Handling** → Background Processing
5. **Real-time Broadcast** → WebSocket to Frontend
6. **UI Update** → Live Dashboard Update

## 🛠️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/users` | Get all users |
| POST | `/api/users` | Create user |
| POST | `/api/transactions` | Create transaction |
| GET | `/api/events` | Get all events |

## 🔌 WebSocket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `connect` | Client → Server | Client connection |
| `event` | Server → Client | Real-time event broadcast |
| `message` | Server → Client | System messages |

## 🧪 Testing the Application

1. Start both servers (backend on :5000, frontend on :3000)
2. Open http://localhost:3000
3. Create a user → Watch for `user_created` event
4. Create a transaction → Watch for `transaction_processed` event
5. Observe real-time updates in the Event Log

## 📚 Documentation

For detailed setup instructions, troubleshooting, and advanced configuration, see [PROJECT_SETUP.md](PROJECT_SETUP.md).

## 🔒 Security Features

- Environment variable configuration
- CORS protection
- Input validation
- SQL injection prevention
- Secure WebSocket connections

## 🚀 Future Enhancements

- [ ] User authentication and authorization
- [ ] Event replay functionality
- [ ] Microservices architecture
- [ ] Message queue integration (Redis/RabbitMQ)
- [ ] Comprehensive testing suite
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using Event-Driven Architecture principles**
This is a financial technology I build using Python 
