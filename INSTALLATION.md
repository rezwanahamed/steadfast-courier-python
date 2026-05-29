# Quick Installation & Setup Guide

## 📦 Installation

### Option 1: From PyPI (Recommended)

```bash
pip install steadfast-courier
```

### Option 2: From Source

```bash
git clone https://github.com/nayemuf/steadfast-courier-python.git
cd steadfast-courier-python
pip install -e .
```

## ⚙️ Quick Setup

### 1. Get Your API Credentials

1. Visit [SteadFast Courier Portal](https://steadfast.com.bd/)
2. Log in with your account
3. Navigate to API Settings / Developer
4. Copy your **API Key** and **Secret Key**

### 2. Configure Environment Variables

Create `.env` file:

```env
STEADFAST_API_KEY=your-api-key-here
STEADFAST_SECRET_KEY=your-secret-key-here
```

### 3. Start Using the Package

#### Basic Python

```python
from steadfast_courier import SteadfastCourier
import os
from dotenv import load_dotenv

load_dotenv()

client = SteadfastCourier(
    api_key=os.getenv('STEADFAST_API_KEY'),
    secret_key=os.getenv('STEADFAST_SECRET_KEY')
)

# Create an order
response = client.order().place_order({
    'invoice': 'ORD-001',
    'recipient_name': 'John Doe',
    'recipient_phone': '01712345678',
    'recipient_address': 'House 44, Gulshan, Dhaka',
    'cod_amount': 1000.00,
})

print(f"Order created! Tracking: {response['consignment']['tracking_code']}")
```

#### With Django

```python
# settings.py
STEADFAST_API_KEY = 'your-api-key'
STEADFAST_SECRET_KEY = 'your-secret-key'

# views.py
from steadfast_courier import SteadfastCourier
from django.conf import settings

client = SteadfastCourier(
    api_key=settings.STEADFAST_API_KEY,
    secret_key=settings.STEADFAST_SECRET_KEY
)
```

#### With FastAPI

```python
from fastapi import FastAPI
from steadfast_courier import SteadfastCourier

app = FastAPI()

client = SteadfastCourier(api_key='key', secret_key='secret')

@app.post("/orders/")
async def create_order(order_data: dict):
    response = client.order().place_order(order_data)
    return response
```

#### With Flask

```python
from flask import Flask, request, jsonify
from steadfast_courier import SteadfastCourier

app = Flask(__name__)
client = SteadfastCourier(api_key='key', secret_key='secret')

@app.route('/orders', methods=['POST'])
def create_order():
    response = client.order().place_order(request.json)
    return jsonify(response)
```

## 📚 Documentation

- **[Complete Usage Guide](docs/USAGE.md)** - Detailed examples and patterns
- **[API Documentation](docs/API_DOCUMENTATION.md)** - Full API reference
- **[Django Integration](docs/DJANGO_SETUP.md)** - Django setup and examples
- **[FastAPI Integration](docs/FASTAPI_SETUP.md)** - FastAPI setup and examples
- **[Flask Integration](docs/FLASK_SETUP.md)** - Flask setup and examples

## 🔧 Common Tasks

### Check Order Status

```python
# By tracking code
status = client.status().get_status_by_tracking_code('SF1234567890')

# By invoice
status = client.status().get_status_by_invoice('ORD-001')

# By consignment ID
status = client.status().get_status_by_consignment_id(12345)
```

### Check Account Balance

```python
balance = client.balance().get_current_balance()
print(f"Balance: {balance['balance']} Taka")
```

### Create Multiple Orders

```python
orders = [
    {'invoice': 'ORD-001', 'recipient_name': 'Customer 1', ...},
    {'invoice': 'ORD-002', 'recipient_name': 'Customer 2', ...},
]

response = client.order().place_bulk_orders(orders)
```

### Error Handling

```python
from steadfast_courier import SteadfastException

try:
    response = client.order().place_order(data)
except SteadfastException as e:
    print(f"Error: {e}")
    print(f"Code: {e.code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🆘 Troubleshooting

### "Unauthorized" Error

- Check API Key and Secret Key
- Verify they are from your SteadFast account
- Ensure they are correctly set in environment variables

### "Rate limit exceeded"

- Wait a moment before making new requests
- Implement retry logic with exponential backoff
- Maximum 60 requests per minute

### Validation Errors

- **Phone must be 11 digits**: Ensure phone is exactly 11 digits (no formatting)
- **Invoice invalid format**: Use only letters, numbers, hyphens, underscores
- **Address too long**: Keep address under 250 characters

### Connection Errors

- Check internet connection
- Verify API endpoint is accessible
- Try using a custom base URL if needed

## 📞 Support

- **GitHub Issues:** https://github.com/nayemuf/steadfast-courier-python/issues
- **Email:** nayem110899@gmail.com
- **API Docs:** https://steadfast.com.bd/

## ✅ Next Steps

1. Read the [Complete Usage Guide](docs/USAGE.md)
2. Choose your framework guide (Django/FastAPI/Flask)
3. Check the [examples/](examples/) folder
4. Review the [API Documentation](docs/API_DOCUMENTATION.md)
5. Test with your API credentials

---

Happy shipping! 🚚
