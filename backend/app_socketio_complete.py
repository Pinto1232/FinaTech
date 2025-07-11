from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
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

# Initialize SocketIO with CORS support
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False)

# Event Queue for Event-Driven Architecture
event_queue = queue.Queue()

# In-memory storage (for demo without database)
users_db = []
transactions_db = []
events_db = []

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
            'timestamp': datetime.now().isoformat(),
            'id': len(events_db) + 1
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
        
        logger.info(f"📡 Event published: {event_type}")
        return event

# Initialize Event Bus
event_bus = EventBus()

def event_processor():
    """Background thread to process events"""
    while True:
        try:
            if not event_queue.empty():
                event = event_queue.get()
                # Process event (save to in-memory storage)
                save_event_to_storage(event)
                event_queue.task_done()
            time.sleep(0.1)
        except Exception as e:
            logger.error(f"Error processing event: {e}")

def save_event_to_storage(event):
    """Save event to in-memory storage"""
    try:
        events_db.append(event)
        logger.info(f"💾 Event saved: {event['type']}")
    except Exception as e:
        logger.error(f"Error saving event: {e}")

# Event handlers
def handle_user_created(event):
    """Handle user created event"""
    logger.info(f"👤 User created: {event['data']['name']}")

def handle_transaction_processed(event):
    """Handle transaction processed event"""
    logger.info(f"💳 Transaction processed: ${event['data']['amount']} ({event['data']['type']})")

# Subscribe to events
event_bus.subscribe('user_created', handle_user_created)
event_bus.subscribe('transaction_processed', handle_transaction_processed)

# Add CORS headers manually for regular HTTP requests
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'socketio': 'enabled',
        'events_count': len(events_db),
        'users_count': len(users_db),
        'transactions_count': len(transactions_db),
        'event_driven_architecture': 'active',
        'websocket_support': True
    })

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and email are required'}), 400
        
        # Create user
        user_id = len(users_db) + 1
        user = {
            'id': user_id,
            'name': data['name'],
            'email': data['email'],
            'created_at': datetime.now().isoformat()
        }
        
        users_db.append(user)
        
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
        return jsonify(users_db)
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
        
        # Create transaction
        transaction_id = len(transactions_db) + 1
        transaction = {
            'id': transaction_id,
            'user_id': int(data['user_id']),
            'amount': float(data['amount']),
            'type': data['type'],
            'created_at': datetime.now().isoformat()
        }
        
        transactions_db.append(transaction)
        
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
        # Return events in reverse chronological order
        return jsonify(sorted(events_db, key=lambda x: x['timestamp'], reverse=True))
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('🔌 Client connected via WebSocket')
    emit('message', {
        'data': 'Connected to FinaTech Event System',
        'timestamp': datetime.now().isoformat(),
        'type': 'connection'
    })
    
    # Send current stats
    emit('stats', {
        'users': len(users_db),
        'transactions': len(transactions_db),
        'events': len(events_db),
        'timestamp': datetime.now().isoformat()
    })
    
    # Send recent events
    recent_events = sorted(events_db, key=lambda x: x['timestamp'], reverse=True)[:5]
    emit('recent_events', recent_events)

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('🔌 Client disconnected from WebSocket')

@socketio.on('get_events')
def handle_get_events():
    """Handle request for events"""
    recent_events = sorted(events_db, key=lambda x: x['timestamp'], reverse=True)[:10]
    emit('events_update', recent_events)

@socketio.on('get_users')
def handle_get_users():
    """Handle request for users"""
    emit('users_update', users_db)

@socketio.on('get_stats')
def handle_get_stats():
    """Handle request for system stats"""
    emit('stats', {
        'users': len(users_db),
        'transactions': len(transactions_db),
        'events': len(events_db),
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('ping')
def handle_ping():
    """Handle ping from client"""
    emit('pong', {'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Start event processor thread
    event_thread = threading.Thread(target=event_processor, daemon=True)
    event_thread.start()
    
    # Add some sample data
    sample_user = {
        'id': 1,
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'created_at': datetime.now().isoformat()
    }
    users_db.append(sample_user)
    
    # Publish initial event
    event_bus.publish('system_started', {
        'message': 'FinaTech Event-Driven Architecture initialized',
        'version': '1.0.0',
        'features': ['Event Bus', 'WebSocket Support', 'Real-time Updates', 'Background Processing'],
        'socketio_enabled': True
    })
    
    print("🚀 FinaTech Event-Driven Backend Starting...")
    print("📊 Backend running on: http://localhost:5001")
    print("🔄 Event-Driven Architecture: ACTIVE")
    print("🌐 WebSocket Support: ENABLED ✅")
    print("⚡ Event Bus: RUNNING")
    print("🔄 Background Event Processing: ACTIVE")
    print("💾 Database: In-Memory Storage (Demo Mode)")
    print("🔗 CORS: Enabled for all origins")
    print("📋 API Endpoints:")
    print("   - GET  /api/health")
    print("   - GET  /api/users")
    print("   - POST /api/users")
    print("   - POST /api/transactions")
    print("   - GET  /api/events")
    print("🔌 WebSocket Events:")
    print("   - connect/disconnect")
    print("   - event (real-time events)")
    print("   - message (system messages)")
    print("   - stats (system statistics)")
    print("   - ping/pong (connection test)")
    print("💡 Ready for real-time Event-Driven Architecture!")
    
    # Run the application with SocketIO
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)