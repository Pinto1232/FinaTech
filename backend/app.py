from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import pyodbc
import json
import threading
import queue
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
CORS(app, origins=["http://localhost:3000"])
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

# Event Queue for Event-Driven Architecture
event_queue = queue.Queue()

# Database configuration
DB_CONFIG = {
    'server': 'localhost',
    'database': 'FinaTechDB',
    'username': 'sa',
    'password': 'your_password',
    'driver': '{ODBC Driver 17 for SQL Server}'
}

def get_db_connection():
    """Get database connection"""
    try:
        conn_str = f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']}"
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

class EventBus:
    """Event Bus for handling events in the system"""
    
    def __init__(self):
        self.subscribers = {}
    
    def subscribe(self, event_type, callback):
        """Subscribe to an event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    def publish(self, event_type, data):
        """Publish an event"""
        event = {
            'type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add to queue for processing
        event_queue.put(event)
        
        # Notify subscribers
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"Error in event callback: {e}")
        
        # Emit to frontend via WebSocket
        socketio.emit('event', event)
        
        logger.info(f"Event published: {event_type}")

# Initialize Event Bus
event_bus = EventBus()

def event_processor():
    """Background thread to process events"""
    while True:
        try:
            if not event_queue.empty():
                event = event_queue.get()
                # Process event (save to database, trigger other actions, etc.)
                save_event_to_db(event)
                event_queue.task_done()
            time.sleep(0.1)
        except Exception as e:
            logger.error(f"Error processing event: {e}")

def save_event_to_db(event):
    """Save event to database"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Events (event_type, event_data, timestamp)
                VALUES (?, ?, ?)
            """, (event['type'], json.dumps(event['data']), event['timestamp']))
            conn.commit()
            conn.close()
    except Exception as e:
        logger.error(f"Error saving event to database: {e}")

# Event handlers
def handle_user_created(event):
    """Handle user created event"""
    logger.info(f"User created: {event['data']}")

def handle_transaction_processed(event):
    """Handle transaction processed event"""
    logger.info(f"Transaction processed: {event['data']}")

# Subscribe to events
event_bus.subscribe('user_created', handle_user_created)
event_bus.subscribe('transaction_processed', handle_transaction_processed)

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and email are required'}), 400
        
        # Save to database
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Users (name, email, created_at)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?)
        """, (data['name'], data['email'], datetime.now()))
        
        user_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        # Publish event
        event_bus.publish('user_created', {
            'user_id': user_id,
            'name': data['name'],
            'email': data['email']
        })
        
        return jsonify({'id': user_id, 'message': 'User created successfully'}), 201
        
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, created_at FROM Users")
        users = []
        for row in cursor.fetchall():
            users.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'created_at': row[3].isoformat() if row[3] else None
            })
        
        conn.close()
        return jsonify(users)
        
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction"""
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['user_id', 'amount', 'type']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'user_id, amount, and type are required'}), 400
        
        # Save to database
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Transactions (user_id, amount, transaction_type, created_at)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?)
        """, (data['user_id'], data['amount'], data['type'], datetime.now()))
        
        transaction_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        # Publish event
        event_bus.publish('transaction_processed', {
            'transaction_id': transaction_id,
            'user_id': data['user_id'],
            'amount': data['amount'],
            'type': data['type']
        })
        
        return jsonify({'id': transaction_id, 'message': 'Transaction created successfully'}), 201
        
    except Exception as e:
        logger.error(f"Error creating transaction: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("SELECT id, event_type, event_data, timestamp FROM Events ORDER BY timestamp DESC")
        events = []
        for row in cursor.fetchall():
            events.append({
                'id': row[0],
                'type': row[1],
                'data': json.loads(row[2]) if row[2] else {},
                'timestamp': row[3].isoformat() if row[3] else None
            })
        
        conn.close()
        return jsonify(events)
        
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('Client connected')
    emit('message', {'data': 'Connected to FinaTech Event System'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected')

if __name__ == '__main__':
    # Start event processor thread
    event_thread = threading.Thread(target=event_processor, daemon=True)
    event_thread.start()
    
    # Run the application
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)