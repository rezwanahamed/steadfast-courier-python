# Django Integration Guide

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Basic Usage](#basic-usage)
4. [Service Layer Pattern](#service-layer-pattern)
5. [Celery Integration](#celery-integration)
6. [Error Handling](#error-handling)

## Installation

### Step 1: Install Dependencies

```bash
pip install django steadfast-courier python-decouple
```

### Step 2: Install in Django Project

Add to your Django app:

```bash
python manage.py startapp courier  # Create a new app if needed
```

## Configuration

### .env File

Create a `.env` file in your project root:

```env
STEADFAST_API_KEY=your-api-key
STEADFAST_SECRET_KEY=your-secret-key
STEADFAST_BASE_URL=https://portal.packzy.com/api/v1
STEADFAST_TIMEOUT=30
```

Or copy the provided template:

```bash
cp .env.example .env
```

### settings.py (Option 1: Using from_env() - Recommended)

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Your other Django settings...
```

Then in your views/services, use:

```python
from steadfast_courier import SteadfastCourier

client = SteadfastCourier.from_env()
```

### settings.py (Option 2: Using decouple)

````python
import os
from decouple import config

# Load SteadFast API Credentials
STEADFAST_API_KEY = config('STEADFAST_API_KEY', default='')
STEADFAST_SECRET_KEY = config('STEADFAST_SECRET_KEY', default='')
STEADFAST_BASE_URL = config('STEADFAST_BASE_URL', default='https://portal.packzy.com/api/v1')
STEADFAST_TIMEOUT = config('STEADFAST_TIMEOUT', default=30, cast=int)

## Basic Usage

### views.py

```python
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from steadfast_courier import SteadfastCourier, SteadfastException

def get_steadfast_client():
    """Initialize SteadFast client"""
    return SteadfastCourier(
        api_key=settings.STEADFAST_API_KEY,
        secret_key=settings.STEADFAST_SECRET_KEY,
        base_url=settings.STEADFAST_BASE_URL,
        timeout=settings.STEADFAST_TIMEOUT,
    )

@require_http_methods(["POST"])
@csrf_exempt
def create_order(request):
    """Create a new order"""
    import json

    try:
        data = json.loads(request.body)

        # Prepare order data
        order_data = {
            'invoice': data.get('invoice'),
            'recipient_name': data.get('recipient_name'),
            'recipient_phone': data.get('recipient_phone'),
            'recipient_address': data.get('recipient_address'),
            'cod_amount': float(data.get('cod_amount', 0)),
            'note': data.get('note', ''),
            'recipient_email': data.get('recipient_email', ''),
        }

        # Create order
        client = get_steadfast_client()
        response = client.order().place_order(order_data)

        return JsonResponse({
            'success': True,
            'data': response
        })

    except SteadfastException as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'code': e.code
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_order_status(request, tracking_code):
    """Get order status"""
    try:
        client = get_steadfast_client()
        status = client.status().get_status_by_tracking_code(tracking_code)

        return JsonResponse({
            'success': True,
            'data': status
        })

    except SteadfastException as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@require_http_methods(["GET"])
def get_balance(request):
    """Get account balance"""
    try:
        client = get_steadfast_client()
        balance = client.balance().get_current_balance()

        return JsonResponse({
            'success': True,
            'balance': balance
        })

    except SteadfastException as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
````

### urls.py

```python
from django.urls import path
from . import views

urlpatterns = [
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/status/<str:tracking_code>/', views.get_order_status, name='get_order_status'),
    path('account/balance/', views.get_balance, name='get_balance'),
]
```

## Service Layer Pattern

### services.py (Recommended)

```python
from django.conf import settings
from steadfast_courier import SteadfastCourier, SteadfastException
import logging

logger = logging.getLogger(__name__)

class SteadfastService:
    """Service layer for SteadFast API"""

    def __init__(self):
        self.client = SteadfastCourier(
            api_key=settings.STEADFAST_API_KEY,
            secret_key=settings.STEADFAST_SECRET_KEY,
            base_url=settings.STEADFAST_BASE_URL,
            timeout=settings.STEADFAST_TIMEOUT,
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

    def get_status(self, tracking_code):
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

    def create_bulk_orders(self, orders):
        """Create multiple orders"""
        try:
            logger.info(f"Creating {len(orders)} orders")
            response = self.client.order().place_bulk_orders(orders)
            logger.info(f"Bulk orders created successfully")
            return response
        except SteadfastException as e:
            logger.error(f"Bulk order creation failed: {str(e)}")
            raise

# Usage in views
from .services import SteadfastService

def create_order(request):
    try:
        data = json.loads(request.body)
        service = SteadfastService()
        response = service.create_order(data)
        return JsonResponse({'success': True, 'data': response})
    except SteadfastException as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
```

## Celery Integration

### tasks.py

```python
from celery import shared_task
from .services import SteadfastService
from steadfast_courier import SteadfastException
import logging

logger = logging.getLogger(__name__)

@shared_task
def create_order_async(order_data):
    """Create order asynchronously"""
    try:
        service = SteadfastService()
        response = service.create_order(order_data)
        logger.info(f"Async order created: {response['consignment']['consignment_id']}")
        return response
    except Exception as e:
        logger.error(f"Async order creation failed: {str(e)}")
        raise

@shared_task
def create_bulk_orders_async(orders):
    """Create bulk orders asynchronously"""
    try:
        service = SteadfastService()
        response = service.create_bulk_orders(orders)
        logger.info(f"Async bulk orders created successfully")
        return response
    except Exception as e:
        logger.error(f"Async bulk order creation failed: {str(e)}")
        raise
```

### Using in Views

```python
from .tasks import create_order_async
from django.http import JsonResponse

def create_order_async_view(request):
    """Create order asynchronously using Celery"""
    try:
        data = json.loads(request.body)

        # Queue the task
        task = create_order_async.delay(data)

        return JsonResponse({
            'success': True,
            'task_id': task.id,
            'message': 'Order is being processed'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

def get_task_status(request, task_id):
    """Get status of async task"""
    from celery.result import AsyncResult

    task = AsyncResult(task_id)

    return JsonResponse({
        'task_id': task_id,
        'status': task.status,
        'result': task.result if task.ready() else None
    })
```

## Error Handling

### middleware.py (Custom Error Handler)

```python
from django.http import JsonResponse
from steadfast_courier import SteadfastException
import logging

logger = logging.getLogger(__name__)

class SteadfastErrorMiddleware:
    """Middleware to handle SteadFast exceptions"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, SteadfastException):
            logger.error(f"SteadFast API Error: {str(exception)}")
            return JsonResponse({
                'success': False,
                'error': str(exception),
                'code': exception.code
            }, status=400)

        return None
```

### Add to MIDDLEWARE in settings.py

```python
MIDDLEWARE = [
    # ... other middleware
    'courier.middleware.SteadfastErrorMiddleware',
]
```

## Complete Example

### models.py

```python
from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]

    invoice = models.CharField(max_length=100, unique=True)
    recipient_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=20)
    recipient_address = models.TextField()
    cod_amount = models.DecimalField(max_digits=10, decimal_places=2)

    consignment_id = models.IntegerField(null=True, blank=True)
    tracking_code = models.CharField(max_length=100, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.invoice} - {self.recipient_name}"
```

### Complete View

```python
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from steadfast_courier import SteadfastException
from .models import Order
from .services import SteadfastService

@require_http_methods(["POST"])
@csrf_exempt
def create_order(request):
    """Create order and save to database"""
    try:
        data = json.loads(request.body)

        # Prepare order data
        order_data = {
            'invoice': data.get('invoice'),
            'recipient_name': data.get('recipient_name'),
            'recipient_phone': data.get('recipient_phone'),
            'recipient_address': data.get('recipient_address'),
            'cod_amount': float(data.get('cod_amount', 0)),
        }

        # Create order via API
        service = SteadfastService()
        api_response = service.create_order(order_data)

        # Save to database
        order = Order.objects.create(
            invoice=order_data['invoice'],
            recipient_name=order_data['recipient_name'],
            recipient_phone=order_data['recipient_phone'],
            recipient_address=order_data['recipient_address'],
            cod_amount=order_data['cod_amount'],
            consignment_id=api_response['consignment']['consignment_id'],
            tracking_code=api_response['consignment']['tracking_code'],
            status='processing'
        )

        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'consignment_id': api_response['consignment']['consignment_id'],
            'tracking_code': api_response['consignment']['tracking_code']
        })

    except SteadfastException as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
```

## Logging Configuration

### logging_config.py

```python
import logging
import logging.config
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['require_debug_true'],
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'steadfast.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'errors.log',
            'maxBytes': 1024 * 1024 * 15,
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'steadfast_courier': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
```

## See Also

- [Complete Usage Guide](USAGE.md)
- [FastAPI Integration](FASTAPI_SETUP.md)
- [Flask Integration](FLASK_SETUP.md)
