# Complete Usage Guide for SteadFast Courier Python Package

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Basic Usage](#basic-usage)
3. [API Reference](#api-reference)
4. [Framework Integration](#framework-integration)
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)

## Installation & Setup

### Step 1: Install the Package

```bash
pip install steadfast-courier
```

### Step 2: Get Your Credentials

1. Visit [SteadFast Courier Portal](https://steadfast.com.bd/)
2. Log in to your account
3. Navigate to API Settings
4. Copy your API Key and Secret Key

### Step 3: Configure Environment Variables

Create a `.env` file in your project:

```env
STEADFAST_API_KEY=your-api-key
STEADFAST_SECRET_KEY=your-secret-key
STEADFAST_BASE_URL=https://portal.packzy.com/api/v1
STEADFAST_TIMEOUT=30
```

Alternatively, copy the provided `.env.example`:

```bash
cp .env.example .env
```

Then edit the `.env` file with your credentials.

## Basic Usage

### Option 1: Initialize from Environment Variables (Recommended)

```python
from steadfast_courier import SteadfastCourier
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize client from environment variables
client = SteadfastCourier.from_env()
```

### Option 2: Initialize with Explicit Credentials

```python
from steadfast_courier import SteadfastCourier

client = SteadfastCourier(
    api_key='your-api-key',
    secret_key='your-secret-key',
    base_url='https://portal.packzy.com/api/v1',  # Optional
    timeout=30  # Optional
)
```

### Simple Order Creation

```python
try:
    response = client.order().place_order({
        'invoice': 'ORD-12345',
        'recipient_name': 'Ahmed Hassan',
        'recipient_phone': '01712345678',
        'recipient_address': 'House 12, Gulshan, Dhaka 1212',
        'cod_amount': 2500.00,
    })

    print(f"Success! Consignment ID: {response['consignment']['consignment_id']}")
    print(f"Tracking Code: {response['consignment']['tracking_code']}")
except Exception as e:
    print(f"Error: {e}")
```

## API Reference

### Order Management API

#### Create Single Order

**Endpoint:** `POST /create_order`

**Method:** `client.order().place_order(order_data)`

**Parameters:**

| Parameter         | Type   | Required | Description                                                       |
| ----------------- | ------ | -------- | ----------------------------------------------------------------- |
| invoice           | string | Yes      | Unique order identifier (alphanumeric, hyphens, underscores only) |
| recipient_name    | string | Yes      | Customer's full name (max 100 chars)                              |
| recipient_phone   | string | Yes      | Customer's phone (11 digits)                                      |
| recipient_address | string | Yes      | Delivery address (max 250 chars)                                  |
| cod_amount        | float  | Yes      | Cash on delivery amount (>= 0)                                    |
| note              | string | No       | Special delivery instructions                                     |
| recipient_email   | string | No       | Customer's email (valid format)                                   |
| alternative_phone | string | No       | Alternative phone (11 digits)                                     |
| item_description  | string | No       | Description of items                                              |
| total_lot         | int    | No       | Number of items/lots                                              |
| delivery_type     | int    | No       | 0 = home delivery, 1 = hub pickup                                 |

**Example:**

```python
order_data = {
    'invoice': 'ORD-2024-00123',
    'recipient_name': 'Sara Rahman',
    'recipient_phone': '01987654321',
    'recipient_address': 'Apartment 5B, Block C, Banasree, Dhaka 1219',
    'cod_amount': 3500.50,
    'note': 'Leave with security guard if not home',
    'recipient_email': 'sara.rahman@example.com',
    'delivery_type': 0,  # Home delivery
}

response = client.order().place_order(order_data)
```

**Response:**

```json
{
  "consignment": {
    "consignment_id": 98765,
    "invoice": "ORD-2024-00123",
    "tracking_code": "SF1234567890",
    "status": "pending",
    "created_at": "2024-05-29T10:30:00Z"
  },
  "message": "Order created successfully"
}
```

#### Create Bulk Orders

**Method:** `client.order().place_bulk_orders(orders_list)`

**Constraints:** Maximum 500 orders per request

**Example:**

```python
orders = [
    {
        'invoice': 'ORD-2024-00101',
        'recipient_name': 'Customer 1',
        'recipient_phone': '01712345678',
        'recipient_address': 'Address 1',
        'cod_amount': 1000.00,
    },
    {
        'invoice': 'ORD-2024-00102',
        'recipient_name': 'Customer 2',
        'recipient_phone': '01812345678',
        'recipient_address': 'Address 2',
        'cod_amount': 2000.00,
    },
    # ... up to 500 orders
]

response = client.order().place_bulk_orders(orders)
```

### Status Tracking API

#### Get Status by Consignment ID

**Method:** `client.status().get_status_by_consignment_id(consignment_id)`

```python
status = client.status().get_status_by_consignment_id(98765)
print(f"Status: {status['consignment']['status']}")
```

#### Get Status by Invoice

**Method:** `client.status().get_status_by_invoice(invoice)`

```python
status = client.status().get_status_by_invoice('ORD-2024-00123')
print(f"Tracking Code: {status['consignment']['tracking_code']}")
```

#### Get Status by Tracking Code

**Method:** `client.status().get_status_by_tracking_code(tracking_code)`

```python
status = client.status().get_status_by_tracking_code('SF1234567890')
print(f"Current Status: {status['consignment']['status']}")
```

### Balance API

#### Check Account Balance

**Method:** `client.balance().get_current_balance()`

```python
balance_info = client.balance().get_current_balance()
print(f"Available Balance: {balance_info['balance']} Taka")
```

### Payment API

#### Get All Payments

**Method:** `client.payment().get_payments()`

```python
payments = client.payment().get_payments()
for payment in payments['payments']:
    print(f"Payment ID: {payment['id']}, Amount: {payment['amount']}")
```

#### Get Specific Payment

**Method:** `client.payment().get_payment(payment_id)`

```python
payment = client.payment().get_payment(123)
print(f"Payment amount: {payment['amount']}")
```

### Return Management API

#### Create Return Request

**Method:** `client.return_api().create_return_request(data)`

**Required:** At least one of: `consignment_id`, `invoice`, or `tracking_code`

```python
return_request = client.return_api().create_return_request({
    'invoice': 'ORD-2024-00123',
    'reason': 'Customer requested return'
})
```

#### Get Return Requests

**Method:** `client.return_api().get_return_requests()`

```python
returns = client.return_api().get_return_requests()
```

#### Get Specific Return Request

**Method:** `client.return_api().get_return_request(return_id)`

```python
return_request = client.return_api().get_return_request(123)
```

### Police Station API

#### Get Police Stations

**Method:** `client.police_station().get_police_stations()`

```python
stations = client.police_station().get_police_stations()
for station in stations['stations']:
    print(f"Station: {station['name']}, Area: {station['area']}")
```

## Framework Integration

### Django Integration

See [DJANGO_SETUP.md](DJANGO_SETUP.md) for detailed setup.

### FastAPI Integration

See [FASTAPI_SETUP.md](FASTAPI_SETUP.md) for detailed setup.

### Flask Integration

See [FLASK_SETUP.md](FLASK_SETUP.md) for detailed setup.

## Error Handling

### Exception Types

```python
from steadfast_courier import SteadfastException

try:
    response = client.order().place_order(data)
except SteadfastException as e:
    # Handle SteadFast API errors
    print(f"API Error: {e}")
    print(f"Status Code: {e.code}")
    print(f"Detailed Errors: {e.get_errors()}")
except Exception as e:
    # Handle other errors
    print(f"Unexpected error: {e}")
```

### Common Errors

| Error                               | Cause                  | Solution                                        |
| ----------------------------------- | ---------------------- | ----------------------------------------------- |
| "Unauthorized"                      | Wrong API credentials  | Check your API Key and Secret Key               |
| "Rate limit exceeded"               | Too many requests      | Wait before making new requests                 |
| "Validation error"                  | Invalid input data     | Check all required fields and formats           |
| "Recipient phone must be 11 digits" | Invalid phone format   | Ensure phone is exactly 11 digits               |
| "Invoice must be alphanumeric"      | Invalid invoice format | Use only letters, numbers, hyphens, underscores |

## Best Practices

### 1. Environment Configuration

```python
# Don't do this
client = SteadfastCourier(
    api_key='actual-key-here',
    secret_key='actual-secret-here'
)

# Do this instead
import os
from dotenv import load_dotenv

load_dotenv()
client = SteadfastCourier(
    api_key=os.getenv('STEADFAST_API_KEY'),
    secret_key=os.getenv('STEADFAST_SECRET_KEY')
)
```

### 2. Error Handling

```python
from steadfast_courier import SteadfastException

def create_order_safe(order_data):
    try:
        client = SteadfastCourier(api_key, secret_key)
        response = client.order().place_order(order_data)
        return {'success': True, 'data': response}
    except SteadfastException as e:
        # Log the error
        print(f"API Error: {e}")
        return {'success': False, 'error': str(e), 'code': e.code}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {'success': False, 'error': 'An unexpected error occurred'}
```

### 3. Input Validation

```python
def validate_order_data(data):
    """Validate before sending to API"""
    required = ['invoice', 'recipient_name', 'recipient_phone', 'recipient_address', 'cod_amount']

    for field in required:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    if len(data['recipient_phone']) != 11:
        raise ValueError("Phone must be 11 digits")

    if not data['invoice']:
        raise ValueError("Invoice cannot be empty")

    return True
```

### 4. Retry Logic

```python
import time

def create_order_with_retry(order_data, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.order().place_order(order_data)
            return response
        except SteadfastException as e:
            if e.code == 429:  # Rate limit
                wait_time = 2 ** attempt
                print(f"Rate limited. Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                raise

    raise Exception("Max retries exceeded")
```

### 5. Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def create_order_with_logging(order_data):
    try:
        logger.info(f"Creating order: {order_data['invoice']}")
        response = client.order().place_order(order_data)
        logger.info(f"Order created successfully: {response['consignment']['consignment_id']}")
        return response
    except Exception as e:
        logger.error(f"Order creation failed: {str(e)}")
        raise
```

## See Also

- [Django Integration](DJANGO_SETUP.md)
- [FastAPI Integration](FASTAPI_SETUP.md)
- [Flask Integration](FLASK_SETUP.md)
- [API Documentation](API_DOCUMENTATION.md)
