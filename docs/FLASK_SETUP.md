# Flask Integration Guide

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Basic Setup](#basic-setup)
4. [Blueprints](#blueprints)
5. [Error Handling](#error-handling)
6. [Database Integration](#database-integration)

## Installation

### Step 1: Install Dependencies

```bash
pip install flask steadfast-courier python-dotenv flask-cors
```

### Step 2: Create Flask Project

```bash
mkdir courier_api
cd courier_api
mkdir app
touch app/__init__.py app/routes.py
touch config.py main.py
```

## Configuration

### .env File

```env
STEADFAST_API_KEY=your-api-key
STEADFAST_SECRET_KEY=your-secret-key
STEADFAST_BASE_URL=https://portal.packzy.com/api/v1
STEADFAST_TIMEOUT=30
FLASK_ENV=development
```

### config.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    STEADFAST_API_KEY = os.getenv('STEADFAST_API_KEY')
    STEADFAST_SECRET_KEY = os.getenv('STEADFAST_SECRET_KEY')
    STEADFAST_BASE_URL = os.getenv('STEADFAST_BASE_URL', 'https://portal.packzy.com/api/v1')
    STEADFAST_TIMEOUT = int(os.getenv('STEADFAST_TIMEOUT', 30))
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

## Basic Setup

### app/**init**.py

```python
from flask import Flask
from flask_cors import CORS
from config import config

def create_app(config_name='development'):
    """Create and configure Flask app"""

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Enable CORS
    CORS(app)

    # Register blueprints
    from app.routes import courier_bp
    app.register_blueprint(courier_bp, url_prefix='/api')

    # Error handlers
    from app.error_handlers import register_error_handlers
    register_error_handlers(app)

    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return {'status': 'healthy'}, 200

    return app
```

### main.py

```python
from app import create_app
import os

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### app/routes.py

```python
from flask import Blueprint, request, jsonify
from steadfast_courier import SteadfastCourier, SteadfastException
from config import Config
import logging

logger = logging.getLogger(__name__)

courier_bp = Blueprint('courier', __name__)

# Initialize client
def get_client():
    """Get SteadFast client instance"""
    return SteadfastCourier(
        api_key=Config.STEADFAST_API_KEY,
        secret_key=Config.STEADFAST_SECRET_KEY,
        base_url=Config.STEADFAST_BASE_URL,
        timeout=Config.STEADFAST_TIMEOUT,
    )

# Order endpoints
@courier_bp.route('/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['invoice', 'recipient_name', 'recipient_phone',
                          'recipient_address', 'cod_amount']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        # Prepare order data
        order_data = {
            'invoice': data.get('invoice'),
            'recipient_name': data.get('recipient_name'),
            'recipient_phone': data.get('recipient_phone'),
            'recipient_address': data.get('recipient_address'),
            'cod_amount': float(data.get('cod_amount')),
            'note': data.get('note', ''),
            'recipient_email': data.get('recipient_email', ''),
        }

        # Create order
        client = get_client()
        response = client.order().place_order(order_data)

        logger.info(f"Order created: {response['consignment']['consignment_id']}")

        return jsonify({
            'success': True,
            'data': response
        }), 201

    except SteadfastException as e:
        logger.error(f"SteadFast Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'code': e.code
        }), 400

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@courier_bp.route('/orders/bulk', methods=['POST'])
def create_bulk_orders():
    """Create multiple orders"""
    try:
        data = request.get_json()
        orders = data.get('orders', [])

        if not orders:
            return jsonify({'success': False, 'error': 'Orders list is empty'}), 400

        if len(orders) > 500:
            return jsonify({
                'success': False,
                'error': 'Maximum 500 orders allowed per request'
            }), 400

        client = get_client()
        response = client.order().place_bulk_orders(orders)

        logger.info(f"Bulk orders created: {len(orders)} orders")

        return jsonify({
            'success': True,
            'data': response
        }), 201

    except SteadfastException as e:
        logger.error(f"SteadFast Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Status endpoints
@courier_bp.route('/orders/status/consignment/<int:consignment_id>')
def get_status_by_cid(consignment_id):
    """Get status by consignment ID"""
    try:
        client = get_client()
        response = client.status().get_status_by_consignment_id(consignment_id)
        return jsonify({'success': True, 'data': response}), 200
    except SteadfastException as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@courier_bp.route('/orders/status/invoice/<invoice>')
def get_status_by_invoice(invoice):
    """Get status by invoice"""
    try:
        client = get_client()
        response = client.status().get_status_by_invoice(invoice)
        return jsonify({'success': True, 'data': response}), 200
    except SteadfastException as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@courier_bp.route('/orders/status/tracking/<tracking_code>')
def get_status_by_tracking(tracking_code):
    """Get status by tracking code"""
    try:
        client = get_client()
        response = client.status().get_status_by_tracking_code(tracking_code)
        return jsonify({'success': True, 'data': response}), 200
    except SteadfastException as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Account endpoints
@courier_bp.route('/account/balance')
def get_balance():
    """Get account balance"""
    try:
        client = get_client()
        response = client.balance().get_current_balance()
        return jsonify({'success': True, 'data': response}), 200
    except SteadfastException as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Payment endpoints
@courier_bp.route('/payments')
def get_payments():
    """Get all payments"""
    try:
        client = get_client()
        response = client.payment().get_payments()
        return jsonify({'success': True, 'data': response}), 200
    except SteadfastException as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@courier_bp.route('/payments/<int:payment_id>')
def get_payment(payment_id):
    """Get specific payment"""
    try:
        client = get_client()
        response = client.payment().get_payment(payment_id)
        return jsonify({'success': True, 'data': response}), 200
    except SteadfastException as e:
        return jsonify({'success': False, 'error': str(e)}), 400
```

## Blueprints

### app/services.py

```python
from steadfast_courier import SteadfastCourier, SteadfastException
from config import Config
import logging

logger = logging.getLogger(__name__)

class CourierService:
    """Service layer for courier operations"""

    def __init__(self):
        self.client = SteadfastCourier(
            api_key=Config.STEADFAST_API_KEY,
            secret_key=Config.STEADFAST_SECRET_KEY,
            base_url=Config.STEADFAST_BASE_URL,
            timeout=Config.STEADFAST_TIMEOUT,
        )

    def create_order(self, order_data):
        """Create order with logging"""
        try:
            logger.info(f"Creating order: {order_data['invoice']}")
            response = self.client.order().place_order(order_data)
            logger.info(f"Order created: {response['consignment']['consignment_id']}")
            return response
        except SteadfastException as e:
            logger.error(f"Order creation failed: {str(e)}")
            raise

    def get_order_status(self, tracking_code):
        """Get order status"""
        try:
            return self.client.status().get_status_by_tracking_code(tracking_code)
        except SteadfastException as e:
            logger.error(f"Status check failed: {str(e)}")
            raise

    def get_balance(self):
        """Get account balance"""
        try:
            return self.client.balance().get_current_balance()
        except SteadfastException as e:
            logger.error(f"Balance check failed: {str(e)}")
            raise
```

### Using Service in Routes

```python
from app.services import CourierService

@courier_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        service = CourierService()
        response = service.create_order(data)
        return jsonify({'success': True, 'data': response}), 201
    except SteadfastException as e:
        return jsonify({'success': False, 'error': str(e)}), 400
```

## Error Handling

### app/error_handlers.py

```python
from flask import jsonify
from steadfast_courier import SteadfastException
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """Register error handlers for Flask app"""

    @app.errorhandler(SteadfastException)
    def handle_steadfast_exception(e):
        logger.error(f"SteadFast Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'code': e.code,
            'details': e.get_errors()
        }), 400

    @app.errorhandler(ValueError)
    def handle_value_error(e):
        logger.error(f"Validation Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'type': 'validation_error'
        }), 400

    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({
            'success': False,
            'error': 'Bad request',
            'code': 400
        }), 400

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            'success': False,
            'error': 'Resource not found',
            'code': 404
        }), 404

    @app.errorhandler(500)
    def handle_internal_error(e):
        logger.error(f"Internal Server Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'code': 500
        }), 500
```

## Database Integration

### With SQLAlchemy

```bash
pip install flask-sqlalchemy
```

### app/models.py

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Order(db.Model):
    """Order model"""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(100), unique=True, nullable=False)
    recipient_name = db.Column(db.String(100), nullable=False)
    recipient_phone = db.Column(db.String(20), nullable=False)
    recipient_address = db.Column(db.Text, nullable=False)
    cod_amount = db.Column(db.Float, nullable=False)

    consignment_id = db.Column(db.Integer)
    tracking_code = db.Column(db.String(100))

    status = db.Column(db.String(20), default='pending')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'invoice': self.invoice,
            'recipient_name': self.recipient_name,
            'tracking_code': self.tracking_code,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
        }
```

### Updated app/**init**.py

```python
from flask import Flask
from flask_cors import CORS
from config import config
from app.models import db

def create_app(config_name='development'):
    """Create and configure Flask app"""

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize database
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Enable CORS
    CORS(app)

    # Register blueprints
    from app.routes import courier_bp
    app.register_blueprint(courier_bp, url_prefix='/api')

    # Error handlers
    from app.error_handlers import register_error_handlers
    register_error_handlers(app)

    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app
```

### Using Models in Routes

```python
from app.models import db, Order
from datetime import datetime

@courier_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        service = CourierService()
        api_response = service.create_order(data)

        # Save to database
        order = Order(
            invoice=data['invoice'],
            recipient_name=data['recipient_name'],
            recipient_phone=data['recipient_phone'],
            recipient_address=data['recipient_address'],
            cod_amount=float(data['cod_amount']),
            consignment_id=api_response['consignment']['consignment_id'],
            tracking_code=api_response['consignment']['tracking_code'],
            status='processing'
        )
        db.session.add(order)
        db.session.commit()

        return jsonify({
            'success': True,
            'order': order.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
```

## Run the Application

```bash
# Install requirements
pip install -r requirements.txt

# Create database
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()

# Run development server
python main.py

# Or use Flask CLI
flask run

# Run on specific port
flask run --port 5000
```

## requirements.txt

```
flask==3.0.0
flask-cors==4.0.0
flask-sqlalchemy==3.1.1
steadfast-courier==1.0.0
python-dotenv==1.0.0
requests==2.31.0
```

## See Also

- [Complete Usage Guide](USAGE.md)
- [Django Integration](DJANGO_SETUP.md)
- [FastAPI Integration](FASTAPI_SETUP.md)
