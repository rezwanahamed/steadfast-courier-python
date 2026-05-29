# Example: Flask Integration

```python
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from steadfast_courier import SteadfastCourier, SteadfastException

load_dotenv()

app = Flask(__name__)

# Initialize client from environment variables
client = SteadfastCourier.from_env()

# Alternative: Initialize with explicit credentials
# client = SteadfastCourier(
#     api_key=os.getenv('STEADFAST_API_KEY'),
#     secret_key=os.getenv('STEADFAST_SECRET_KEY')
# )

@app.route('/')
def home():
    return jsonify({'message': 'Courier API is running'})

@app.route('/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    try:
        data = request.get_json()
        
        order_data = {
            'invoice': data.get('invoice'),
            'recipient_name': data.get('recipient_name'),
            'recipient_phone': data.get('recipient_phone'),
            'recipient_address': data.get('recipient_address'),
            'cod_amount': float(data.get('cod_amount', 0)),
            'note': data.get('note', ''),
        }
        
        response = client.order().place_order(order_data)
        
        return jsonify({
            'success': True,
            'consignment_id': response['consignment']['consignment_id'],
            'tracking_code': response['consignment']['tracking_code']
        }), 201
    
    except SteadfastException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/orders/status/<tracking_code>')
def get_order_status(tracking_code):
    """Get order status"""
    try:
        status = client.status().get_status_by_tracking_code(tracking_code)
        
        return jsonify({
            'success': True,
            'status': status['consignment']['status']
        })
    
    except SteadfastException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/balance')
def get_balance():
    """Get account balance"""
    try:
        balance = client.balance().get_current_balance()
        
        return jsonify({
            'success': True,
            'balance': balance
        })
    
    except SteadfastException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Usage

```bash
# Install dependencies
pip install flask steadfast-courier python-dotenv

# Run server
python example_flask.py

# Create order
curl -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "invoice": "ORD-2024-00001",
    "recipient_name": "John Doe",
    "recipient_phone": "01712345678",
    "recipient_address": "House 44, Gulshan, Dhaka",
    "cod_amount": 1000.0
  }'

# Check status
curl http://localhost:5000/orders/status/SF1234567890

# Check balance
curl http://localhost:5000/balance
```
