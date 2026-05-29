# SteadFast Courier Python Package

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://github.com/rezwanahamed/steadfast-courier-python)
[![Author](https://img.shields.io/badge/Author-Rezwan%20Ahamed-blue.svg)](https://github.com/rezwanahamed)

A professional Python package for integrating with **SteadFast Courier API**. This package provides a clean, well-structured interface for all SteadFast API endpoints with built-in validation, rate limiting, and comprehensive error handling. Works seamlessly with **Django**, **FastAPI**, **Flask**, and all Python frameworks.

## ✨ Features

- ✅ **Complete API Coverage** - All SteadFast Courier API endpoints implemented
- ✅ **Multi-Framework Support** - Django, FastAPI, Flask, and any Python framework
- ✅ **API Key Authentication** - Secure authentication with API Key and Secret Key
- ✅ **Rate Limiting** - Built-in protection against API abuse (configurable)
- ✅ **Input Validation** - Comprehensive validation before API calls
- ✅ **Error Handling** - Detailed exception messages with field-level errors
- ✅ **Type Hints** - Full type hints for better IDE support
- ✅ **Zero Configuration** - Works out of the box with sensible defaults
- ✅ **Production Ready** - Battle-tested in production environments
- ✅ **Logging Support** - Built-in logging for debugging and monitoring

## 📋 Requirements

- Python >= 3.8
- requests >= 2.28.0

## 📦 Installation

Install the package via pip:

```bash
pip install steadfast-courier
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in your project root:

```env
STEADFAST_API_KEY=your-api-key
STEADFAST_SECRET_KEY=your-secret-key
STEADFAST_BASE_URL=https://portal.packzy.com/api/v1  # Optional
STEADFAST_TIMEOUT=30  # Optional
```

**Note:** You can obtain your API credentials from the [SteadFast Courier Portal](https://steadfast.com.bd/).

## 🚀 Quick Start

### Basic Usage

```python
from steadfast_courier import SteadfastCourier

# Initialize the client
client = SteadfastCourier(
    api_key='your-api-key',
    secret_key='your-secret-key'
)

# Place an order
order_data = {
    'invoice': 'ORD-123456',
    'recipient_name': 'John Doe',
    'recipient_phone': '01712345678',
    'recipient_address': 'House 44, Road 2/A, Dhanmondi, Dhaka 1209',
    'cod_amount': 1000.00,
    'note': 'Handle with care',
}

try:
    response = client.order().place_order(order_data)
    print(f"Order created! Consignment ID: {response['consignment']['consignment_id']}")
except Exception as e:
    print(f"Error: {e}")
```

### Django Integration

See [Django Integration Guide](docs/DJANGO_SETUP.md)

```python
# settings.py
STEADFAST_API_KEY = 'your-api-key'
STEADFAST_SECRET_KEY = 'your-secret-key'

# views.py
from steadfast_courier import SteadfastCourier
from django.conf import settings

def create_order(request):
    client = SteadfastCourier(
        api_key=settings.STEADFAST_API_KEY,
        secret_key=settings.STEADFAST_SECRET_KEY
    )

    order_data = {
        'invoice': f'ORD-{request.POST.get("invoice")}',
        'recipient_name': request.POST.get('name'),
        'recipient_phone': request.POST.get('phone'),
        'recipient_address': request.POST.get('address'),
        'cod_amount': float(request.POST.get('cod_amount')),
    }

    try:
        response = client.order().place_order(order_data)
        return {'success': True, 'data': response}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

### FastAPI Integration

See [FastAPI Integration Guide](docs/FASTAPI_SETUP.md)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from steadfast_courier import SteadfastCourier

app = FastAPI()

STEADFAST_CLIENT = SteadfastCourier(
    api_key='your-api-key',
    secret_key='your-secret-key'
)

class OrderRequest(BaseModel):
    invoice: str
    recipient_name: str
    recipient_phone: str
    recipient_address: str
    cod_amount: float

@app.post("/orders/")
async def create_order(order: OrderRequest):
    try:
        response = STEADFAST_CLIENT.order().place_order(order.dict())
        return {"success": True, "data": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Flask Integration

See [Flask Integration Guide](docs/FLASK_SETUP.md)

```python
from flask import Flask, request, jsonify
from steadfast_courier import SteadfastCourier

app = Flask(__name__)

client = SteadfastCourier(
    api_key='your-api-key',
    secret_key='your-secret-key'
)

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order_data = {
        'invoice': data.get('invoice'),
        'recipient_name': data.get('recipient_name'),
        'recipient_phone': data.get('recipient_phone'),
        'recipient_address': data.get('recipient_address'),
        'cod_amount': float(data.get('cod_amount')),
    }

    try:
        response = client.order().place_order(order_data)
        return jsonify({"success": True, "data": response})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

## 📚 API Documentation

### Order Management

#### Place Single Order

```python
client.order().place_order({
    'invoice': 'ORD-123456',
    'recipient_name': 'John Doe',
    'recipient_phone': '01712345678',
    'recipient_address': 'House 44, Road 2/A, Dhanmondi, Dhaka 1209',
    'cod_amount': 1000.00,
    'note': 'Handle with care',  # Optional
    'recipient_email': 'john@example.com',  # Optional
    'alternative_phone': '01812345678',  # Optional
    'item_description': 'Product description',  # Optional
    'total_lot': 1,  # Optional
    'delivery_type': 0,  # Optional: 0=home, 1=hub
})
```

#### Place Bulk Orders

```python
orders = [
    {
        'invoice': 'ORD-001',
        'recipient_name': 'Customer 1',
        'recipient_phone': '01712345678',
        'recipient_address': 'Address 1',
        'cod_amount': 500.00,
    },
    {
        'invoice': 'ORD-002',
        'recipient_name': 'Customer 2',
        'recipient_phone': '01812345678',
        'recipient_address': 'Address 2',
        'cod_amount': 1000.00,
    }
]

client.order().place_bulk_orders(orders)
```

### Status Tracking

```python
# Check status by consignment ID
client.status().get_status_by_consignment_id(12345)

# Check status by invoice
client.status().get_status_by_invoice('ORD-123456')

# Check status by tracking code
client.status().get_status_by_tracking_code('TRAC123456789')
```

### Account Balance

```python
balance = client.balance().get_current_balance()
print(f"Current balance: {balance['balance']}")
```

### Payment Management

```python
# Get all payments
client.payment().get_payments()

# Get specific payment
client.payment().get_payment(123)
```

### Return Management

```python
# Create return request
client.return_api().create_return_request({
    'invoice': 'ORD-123456',
    'reason': 'Customer requested return'
})

# Get return requests
client.return_api().get_return_requests()

# Get specific return request
client.return_api().get_return_request(123)
```

### Police Stations

```python
# Get list of police stations
stations = client.police_station().get_police_stations()
```

## 🔧 Error Handling

```python
from steadfast_courier import SteadfastCourier, SteadfastException

client = SteadfastCourier(api_key='key', secret_key='secret')

try:
    response = client.order().place_order(order_data)
except SteadfastException as e:
    print(f"API Error: {e}")
    print(f"Status Code: {e.code}")
    print(f"Errors: {e.get_errors()}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🔐 Security Best Practices

1. **Never hardcode API keys** - Use environment variables
2. **Use .env files** - Keep credentials out of version control
3. **Validate inputs** - The package validates automatically, but check user inputs
4. **Use HTTPS** - Always use secure connections
5. **Rate limiting** - Be aware of rate limits to avoid blocking

## 📝 Logging

Enable logging to monitor API calls:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('steadfast_courier')
```

## 🧪 Testing

```python
import unittest
from steadfast_courier import SteadfastCourier, SteadfastException

class TestSteadfastCourier(unittest.TestCase):
    def setUp(self):
        self.client = SteadfastCourier(
            api_key='test-key',
            secret_key='test-secret'
        )

    def test_invalid_phone(self):
        with self.assertRaises(SteadfastException):
            self.client.order().place_order({
                'invoice': 'ORD-001',
                'recipient_name': 'Test User',
                'recipient_phone': '123',  # Invalid
                'recipient_address': 'Test Address',
                'cod_amount': 100,
            })

if __name__ == '__main__':
    unittest.main()
```

## 📞 Support

- Documentation: [See USAGE.md](docs/USAGE.md)
- Issue Tracking: [GitHub Issues](https://github.com/rezwanahamed/steadfast-courier-python/issues)
- Developer: [Rezwan Ahamed](https://github.com/rezwanahamed)
- Official API Docs: [SteadFast API Documentation](https://steadfast.com.bd/)

## 📄 License

This package is open-sourced software licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **Original PHP Package** by Nayem Uddin (https://github.com/nayemuf)
- **Python Port with Multi-Framework Support** by Rezwan Ahamed (https://github.com/rezwanahamed)
- SteadFast Courier API by SteadFast Courier Ltd.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📦 Version History

- **1.0.0** (2024-05-29) - Initial Python port with full API coverage and framework integrations
