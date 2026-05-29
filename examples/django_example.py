# Example: Django Integration

```python
# settings.py
# Add to your Django settings
import os

from dotenv import load_dotenv

load_dotenv()

# Your other settings...
STEADFAST_API_KEY = os.getenv('STEADFAST_API_KEY')
STEADFAST_SECRET_KEY = os.getenv('STEADFAST_SECRET_KEY')
STEADFAST_BASE_URL = os.getenv('STEADFAST_BASE_URL')
STEADFAST_TIMEOUT = int(os.getenv('STEADFAST_TIMEOUT', 30))

# views.py
import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from steadfast_courier import SteadfastCourier, SteadfastException


def get_steadfast_client():
    """Initialize SteadFast client from environment variables"""
    return SteadfastCourier.from_env()

@require_http_methods(["POST"])
@csrf_exempt
def create_order(request):
    """Create a new order"""
    try:
        data = json.loads(request.body)
        
        order_data = {
            'invoice': data.get('invoice'),
            'recipient_name': data.get('recipient_name'),
            'recipient_phone': data.get('recipient_phone'),
            'recipient_address': data.get('recipient_address'),
            'cod_amount': float(data.get('cod_amount', 0)),
            'note': data.get('note', ''),
        }
        
        client = get_steadfast_client()
        response = client.order().place_order(order_data)
        
        return JsonResponse({
            'success': True,
            'consignment_id': response['consignment']['consignment_id'],
            'tracking_code': response['consignment']['tracking_code']
        })
    
    except SteadfastException as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@require_http_methods(["GET"])
def get_order_status(request, tracking_code):
    """Get order status"""
    try:
        client = get_steadfast_client()
        status = client.status().get_status_by_tracking_code(tracking_code)
        
        return JsonResponse({
            'success': True,
            'status': status['consignment']['status']
        })
    
    except SteadfastException as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/status/<str:tracking_code>/', views.get_order_status, name='get_order_status'),
]

# settings.py
import os

STEADFAST_API_KEY = os.getenv('STEADFAST_API_KEY', '')
STEADFAST_SECRET_KEY = os.getenv('STEADFAST_SECRET_KEY', '')
```

## Usage

```bash
# Start Django development server
python manage.py runserver

# Create order
curl -X POST http://localhost:8000/api/orders/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "invoice": "ORD-2024-00001",
    "recipient_name": "John Doe",
    "recipient_phone": "01712345678",
    "recipient_address": "House 44, Gulshan, Dhaka",
    "cod_amount": 1000.0
  }'

# Check status
curl http://localhost:8000/api/orders/status/SF1234567890/
```
