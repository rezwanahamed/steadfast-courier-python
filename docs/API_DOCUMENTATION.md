# SteadFast Courier API Documentation

## Overview

This document provides comprehensive API documentation for the SteadFast Courier Python package.

**Base Configuration:**

- Base URL: `https://portal.packzy.com/api/v1`
- Authentication: API Key and Secret Key (via headers)
- Content-Type: `application/json`
- Rate Limit: 60 requests per minute
- Timeout: 30 seconds

## Authentication

All API requests require the following headers:

```
Api-Key: {your-api-key}
Secret-Key: {your-secret-key}
Content-Type: application/json
Accept: application/json
```

## Table of Contents

1. [Order Management API](#1-order-management-api)
2. [Status Tracking API](#2-status-tracking-api)
3. [Balance API](#3-balance-api)
4. [Payment API](#4-payment-api)
5. [Return Management API](#5-return-management-api)
6. [Police Station API](#6-police-station-api)

---

## 1. Order Management API

### 1.1 Place Single Order

**Endpoint:** `POST /create_order`

**Method:** `client.order().place_order(order_data)`

**Description:** Creates a single order/shipment with SteadFast Courier.

**Request Parameters:**

| Parameter         | Type    | Required | Validation                         | Description                   |
| ----------------- | ------- | -------- | ---------------------------------- | ----------------------------- |
| invoice           | string  | Yes      | Alphanumeric, hyphens, underscores | Unique order identifier       |
| recipient_name    | string  | Yes      | Max 100 chars                      | Customer's full name          |
| recipient_phone   | string  | Yes      | Exactly 11 digits                  | Customer's phone number       |
| recipient_address | string  | Yes      | Max 250 chars                      | Delivery address              |
| cod_amount        | numeric | Yes      | >= 0                               | Cash on Delivery amount       |
| note              | string  | No       | -                                  | Special delivery notes        |
| recipient_email   | string  | No       | Valid email                        | Customer's email address      |
| alternative_phone | string  | No       | Exactly 11 digits                  | Alternative contact number    |
| item_description  | string  | No       | -                                  | Description of items          |
| total_lot         | int     | No       | -                                  | Number of items/lots          |
| delivery_type     | int     | No       | 0 or 1                             | 0=home delivery, 1=hub pickup |

**Response Structure:**

```json
{
  "consignment": {
    "consignment_id": 12345,
    "invoice": "ORD-123456",
    "tracking_code": "TRAC123456789",
    "status": "pending",
    "created_at": "2024-05-29T10:30:00Z"
  },
  "message": "Order created successfully"
}
```

**Response Fields:**

| Field                      | Type     | Description                        |
| -------------------------- | -------- | ---------------------------------- |
| consignment.consignment_id | int      | Unique identifier for the shipment |
| consignment.invoice        | string   | The invoice/order number provided  |
| consignment.tracking_code  | string   | Tracking code for the shipment     |
| consignment.status         | string   | Current status of the order        |
| consignment.created_at     | datetime | Order creation timestamp           |

**Example Usage:**

```python
from steadfast_courier import SteadfastCourier

client = SteadfastCourier(api_key='key', secret_key='secret')

order_data = {
    'invoice': 'ORD-123456',
    'recipient_name': 'John Doe',
    'recipient_phone': '01712345678',
    'recipient_address': 'House 44, Road 2/A, Dhanmondi, Dhaka 1209',
    'cod_amount': 1000.00,
    'note': 'Handle with care',
    'delivery_type': 0,
}

response = client.order().place_order(order_data)
```

**Error Codes:**

| Code | Message              | Cause                   |
| ---- | -------------------- | ----------------------- |
| 400  | Validation error     | Invalid input data      |
| 401  | Unauthorized         | Invalid API credentials |
| 403  | Forbidden            | Permission denied       |
| 422  | Unprocessable entity | Validation failed       |
| 429  | Too many requests    | Rate limit exceeded     |
| 500  | Server error         | SteadFast server error  |

---

### 1.2 Place Bulk Orders

**Endpoint:** `POST /create_order/bulk-order`

**Method:** `client.order().place_bulk_orders(orders_list)`

**Description:** Creates multiple orders in a single API call.

**Constraints:**

- Maximum 500 orders per request
- Each order must pass individual validation
- Same validation rules as single order apply

**Request Parameters:**

| Parameter | Type  | Required | Description                     |
| --------- | ----- | -------- | ------------------------------- |
| orders    | array | Yes      | List of order objects (max 500) |

**Response Structure:**

```json
{
  "consignments": [
    {
      "consignment_id": 12345,
      "invoice": "ORD-001",
      "tracking_code": "TRAC001",
      "status": "pending"
    },
    {
      "consignment_id": 12346,
      "invoice": "ORD-002",
      "tracking_code": "TRAC002",
      "status": "pending"
    }
  ],
  "message": "2 orders created successfully"
}
```

**Example Usage:**

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

response = client.order().place_bulk_orders(orders)
```

---

## 2. Status Tracking API

### 2.1 Get Status by Consignment ID

**Endpoint:** `GET /status_by_cid/{consignment_id}`

**Method:** `client.status().get_status_by_consignment_id(consignment_id)`

**Parameters:**

| Parameter      | Type | Required | Description              |
| -------------- | ---- | -------- | ------------------------ |
| consignment_id | int  | Yes      | SteadFast consignment ID |

**Response:**

```json
{
  "consignment": {
    "consignment_id": 12345,
    "invoice": "ORD-123456",
    "tracking_code": "TRAC123456789",
    "status": "delivered",
    "updated_at": "2024-05-29T15:45:00Z"
  }
}
```

**Example:**

```python
status = client.status().get_status_by_consignment_id(12345)
print(f"Status: {status['consignment']['status']}")
```

---

### 2.2 Get Status by Invoice

**Endpoint:** `GET /status_by_invoice/{invoice}`

**Method:** `client.status().get_status_by_invoice(invoice)`

**Parameters:**

| Parameter | Type   | Required | Description          |
| --------- | ------ | -------- | -------------------- |
| invoice   | string | Yes      | Invoice/order number |

**Example:**

```python
status = client.status().get_status_by_invoice('ORD-123456')
```

---

### 2.3 Get Status by Tracking Code

**Endpoint:** `GET /status_by_trackingcode/{tracking_code}`

**Method:** `client.status().get_status_by_tracking_code(tracking_code)`

**Parameters:**

| Parameter     | Type   | Required | Description             |
| ------------- | ------ | -------- | ----------------------- |
| tracking_code | string | Yes      | SteadFast tracking code |

**Example:**

```python
status = client.status().get_status_by_tracking_code('SF1234567890')
```

---

## 3. Balance API

### 3.1 Get Current Balance

**Endpoint:** `GET /get_balance`

**Method:** `client.balance().get_current_balance()`

**Response:**

```json
{
  "balance": 150000.0,
  "currency": "BDT"
}
```

**Example:**

```python
balance = client.balance().get_current_balance()
print(f"Available balance: {balance['balance']} {balance['currency']}")
```

---

## 4. Payment API

### 4.1 Get All Payments

**Endpoint:** `GET /payments`

**Method:** `client.payment().get_payments()`

**Response:**

```json
{
  "payments": [
    {
      "id": 1,
      "amount": 50000.0,
      "date": "2024-05-20",
      "status": "completed"
    }
  ]
}
```

**Example:**

```python
payments = client.payment().get_payments()
for payment in payments['payments']:
    print(f"Payment ID: {payment['id']}, Amount: {payment['amount']}")
```

---

### 4.2 Get Specific Payment

**Endpoint:** `GET /payments/{payment_id}`

**Method:** `client.payment().get_payment(payment_id)`

**Parameters:**

| Parameter  | Type | Required | Description |
| ---------- | ---- | -------- | ----------- |
| payment_id | int  | Yes      | Payment ID  |

**Example:**

```python
payment = client.payment().get_payment(123)
```

---

## 5. Return Management API

### 5.1 Create Return Request

**Endpoint:** `POST /create_return_request`

**Method:** `client.return_api().create_return_request(data)`

**Description:** Creates a return request for a consignment.

**Request Parameters:**

| Parameter      | Type   | Required | Description       |
| -------------- | ------ | -------- | ----------------- |
| consignment_id | int    | No\*     | Consignment ID    |
| invoice        | string | No\*     | Invoice number    |
| tracking_code  | string | No\*     | Tracking code     |
| reason         | string | No       | Reason for return |

\*At least one identifier (consignment_id, invoice, or tracking_code) is required.

**Example:**

```python
return_req = client.return_api().create_return_request({
    'invoice': 'ORD-123456',
    'reason': 'Customer requested return'
})
```

---

### 5.2 Get Return Request

**Endpoint:** `GET /get_return_request/{id}`

**Method:** `client.return_api().get_return_request(return_id)`

**Example:**

```python
return_req = client.return_api().get_return_request(123)
```

---

### 5.3 Get All Return Requests

**Endpoint:** `GET /get_return_requests`

**Method:** `client.return_api().get_return_requests()`

**Example:**

```python
returns = client.return_api().get_return_requests()
```

---

## 6. Police Station API

### 6.1 Get Police Stations

**Endpoint:** `GET /police_stations`

**Method:** `client.police_station().get_police_stations()`

**Response:**

```json
{
  "stations": [
    {
      "id": 1,
      "name": "Dhanmondi Police Station",
      "area": "Dhaka"
    }
  ]
}
```

**Example:**

```python
stations = client.police_station().get_police_stations()
for station in stations['stations']:
    print(f"Station: {station['name']}, Area: {station['area']}")
```

---

## Status Codes

| Code | Meaning                                               |
| ---- | ----------------------------------------------------- |
| 200  | OK - Request successful                               |
| 201  | Created - Resource created successfully               |
| 400  | Bad Request - Invalid input data                      |
| 401  | Unauthorized - Invalid API credentials                |
| 403  | Forbidden - Permission denied                         |
| 404  | Not Found - Resource not found                        |
| 422  | Unprocessable Entity - Validation failed              |
| 429  | Too Many Requests - Rate limit exceeded               |
| 500  | Internal Server Error - Server error                  |
| 503  | Service Unavailable - Service temporarily unavailable |

---

## Error Response Format

All error responses follow this format:

```json
{
  "success": false,
  "error": "Error message describing what went wrong",
  "code": 400,
  "details": {
    "field_name": ["Error message for this field"]
  }
}
```

---

## Rate Limiting

- **Limit:** 60 requests per minute
- **Response Header:** `X-RateLimit-Remaining`
- **When Exceeded:** Returns 429 status code

To handle rate limiting:

```python
import time
from steadfast_courier import SteadfastException

def make_request_with_retry(func, *args, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except SteadfastException as e:
            if e.code == 429 and attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

---

## Best Practices

1. **Use environment variables** for API credentials
2. **Implement retry logic** for rate limiting
3. **Validate inputs** before sending to API
4. **Log API errors** for debugging
5. **Use bulk endpoints** when creating multiple orders
6. **Cache status** when possible to reduce API calls
7. **Handle exceptions** gracefully in production

---

## Support

For issues or questions:

- GitHub Issues: https://github.com/nayemuf/steadfast-courier-python/issues
- Official API Docs: https://steadfast.com.bd/
