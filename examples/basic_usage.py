# Example: Basic Python Usage

```python
import os

from dotenv import load_dotenv
from steadfast_courier import SteadfastCourier, SteadfastException

# Load environment variables
load_dotenv()

# Initialize client
client = SteadfastCourier(
    api_key=os.getenv('STEADFAST_API_KEY'),
    secret_key=os.getenv('STEADFAST_SECRET_KEY')
)

# Example 1: Create a single order
print("=== Example 1: Create Single Order ===")
try:
    response = client.order().place_order({
        'invoice': 'ORD-2024-00001',
        'recipient_name': 'Ahmed Hassan',
        'recipient_phone': '01712345678',
        'recipient_address': 'House 12, Gulshan, Dhaka 1212',
        'cod_amount': 2500.00,
        'note': 'Handle with care',
        'recipient_email': 'ahmed@example.com',
    })
    
    print(f"✓ Order created successfully!")
    print(f"  Consignment ID: {response['consignment']['consignment_id']}")
    print(f"  Tracking Code: {response['consignment']['tracking_code']}")
    print(f"  Status: {response['consignment']['status']}")

except SteadfastException as e:
    print(f"✗ Error: {e}")
    print(f"  Code: {e.code}")

# Example 2: Create bulk orders
print("\n=== Example 2: Create Bulk Orders ===")
try:
    orders = [
        {
            'invoice': 'ORD-2024-00101',
            'recipient_name': 'Customer 1',
            'recipient_phone': '01712345678',
            'recipient_address': 'Address 1, Dhaka',
            'cod_amount': 1000.00,
        },
        {
            'invoice': 'ORD-2024-00102',
            'recipient_name': 'Customer 2',
            'recipient_phone': '01812345678',
            'recipient_address': 'Address 2, Dhaka',
            'cod_amount': 2000.00,
        },
        {
            'invoice': 'ORD-2024-00103',
            'recipient_name': 'Customer 3',
            'recipient_phone': '01912345678',
            'recipient_address': 'Address 3, Dhaka',
            'cod_amount': 1500.00,
        }
    ]
    
    response = client.order().place_bulk_orders(orders)
    print(f"✓ {len(orders)} orders created successfully!")
    for i, consignment in enumerate(response['consignments'], 1):
        print(f"  {i}. {consignment['invoice']} -> {consignment['tracking_code']}")

except SteadfastException as e:
    print(f"✗ Error: {e}")

# Example 3: Check order status
print("\n=== Example 3: Check Order Status ===")
try:
    # By tracking code
    status = client.status().get_status_by_tracking_code('SF1234567890')
    print(f"✓ Status by tracking code: {status['consignment']['status']}")
    
    # By invoice
    status = client.status().get_status_by_invoice('ORD-2024-00001')
    print(f"✓ Status by invoice: {status['consignment']['status']}")
    
except SteadfastException as e:
    print(f"✗ Error: {e}")

# Example 4: Check balance
print("\n=== Example 4: Check Account Balance ===")
try:
    balance = client.balance().get_current_balance()
    print(f"✓ Current balance: {balance['balance']} Taka")

except SteadfastException as e:
    print(f"✗ Error: {e}")

# Example 5: Get payments
print("\n=== Example 5: Get Payments ===")
try:
    payments = client.payment().get_payments()
    print(f"✓ Total payments: {len(payments['payments'])}")
    for payment in payments['payments'][:3]:  # Show first 3
        print(f"  - Payment ID: {payment['id']}, Amount: {payment['amount']}")

except SteadfastException as e:
    print(f"✗ Error: {e}")

# Example 6: Error handling with retry
print("\n=== Example 6: Error Handling with Retry ===")
import time


def create_order_with_retry(order_data, max_retries=3):
    """Create order with retry logic"""
    for attempt in range(max_retries):
        try:
            print(f"  Attempt {attempt + 1}...")
            response = client.order().place_order(order_data)
            print(f"  ✓ Success!")
            return response
        
        except SteadfastException as e:
            if e.code == 429:  # Rate limited
                wait_time = 2 ** attempt
                print(f"  Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"  ✗ Error: {e}")
                raise
    
    raise Exception("Max retries exceeded")

try:
    response = create_order_with_retry({
        'invoice': 'ORD-2024-00999',
        'recipient_name': 'Retry Test',
        'recipient_phone': '01712345678',
        'recipient_address': 'Test Address',
        'cod_amount': 500.00,
    })
except Exception as e:
    print(f"  ✗ Failed: {e}")
```

## Output

```
=== Example 1: Create Single Order ===
✓ Order created successfully!
  Consignment ID: 98765
  Tracking Code: SF1234567890
  Status: pending

=== Example 2: Create Bulk Orders ===
✓ 3 orders created successfully!
  1. ORD-2024-00101 -> SF1000001
  2. ORD-2024-00102 -> SF1000002
  3. ORD-2024-00103 -> SF1000003

=== Example 3: Check Order Status ===
✓ Status by tracking code: in_transit
✓ Status by invoice: pending

=== Example 4: Check Account Balance ===
✓ Current balance: 150000 Taka

=== Example 5: Get Payments ===
✓ Total payments: 5
  - Payment ID: 1, Amount: 50000
  - Payment ID: 2, Amount: 75000
  - Payment ID: 3, Amount: 100000

=== Example 6: Error Handling with Retry ===
  Attempt 1...
  ✓ Success!
```
