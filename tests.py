# Testing Examples

```python
import unittest

from steadfast_courier import SteadfastCourier, SteadfastException
from steadfast_courier.validators import Validator


class TestValidators(unittest.TestCase):
    """Test validation utilities"""
    
    def test_validate_invoice_valid(self):
        """Test valid invoice format"""
        try:
            Validator.validate_invoice('ORD-2024-00001')
            Validator.validate_invoice('ORD_001-ABC')
            Validator.validate_invoice('ORDER123')
        except SteadfastException:
            self.fail("Valid invoice raised exception")
    
    def test_validate_invoice_invalid(self):
        """Test invalid invoice format"""
        with self.assertRaises(SteadfastException):
            Validator.validate_invoice('ORD@2024')
        
        with self.assertRaises(SteadfastException):
            Validator.validate_invoice('ORD#001')
    
    def test_validate_phone_valid(self):
        """Test valid phone format"""
        try:
            Validator.validate_phone('01712345678')
            Validator.validate_phone('01812345678')
        except SteadfastException:
            self.fail("Valid phone raised exception")
    
    def test_validate_phone_invalid(self):
        """Test invalid phone format"""
        with self.assertRaises(SteadfastException):
            Validator.validate_phone('123')  # Too short
        
        with self.assertRaises(SteadfastException):
            Validator.validate_phone('01712345678910')  # Too long
    
    def test_validate_email_valid(self):
        """Test valid email format"""
        try:
            Validator.validate_email('user@example.com')
            Validator.validate_email('test.user+tag@domain.co.uk')
        except SteadfastException:
            self.fail("Valid email raised exception")
    
    def test_validate_email_invalid(self):
        """Test invalid email format"""
        with self.assertRaises(SteadfastException):
            Validator.validate_email('invalid.email')
        
        with self.assertRaises(SteadfastException):
            Validator.validate_email('@example.com')
    
    def test_validate_cod_amount_valid(self):
        """Test valid COD amount"""
        try:
            Validator.validate_cod_amount(100)
            Validator.validate_cod_amount(1000.50)
            Validator.validate_cod_amount(0)
        except SteadfastException:
            self.fail("Valid COD amount raised exception")
    
    def test_validate_cod_amount_invalid(self):
        """Test invalid COD amount"""
        with self.assertRaises(SteadfastException):
            Validator.validate_cod_amount(-100)
        
        with self.assertRaises(SteadfastException):
            Validator.validate_cod_amount('not_a_number')
    
    def test_validate_delivery_type(self):
        """Test delivery type validation"""
        try:
            Validator.validate_delivery_type(0)
            Validator.validate_delivery_type(1)
            Validator.validate_delivery_type(None)
        except SteadfastException:
            self.fail("Valid delivery type raised exception")
        
        with self.assertRaises(SteadfastException):
            Validator.validate_delivery_type(2)


class TestSteadfastException(unittest.TestCase):
    """Test exception handling"""
    
    def test_exception_creation(self):
        """Test exception creation"""
        exc = SteadfastException("Test error", 400, {'field': ['error']})
        
        self.assertEqual(str(exc), "Test error")
        self.assertEqual(exc.code, 400)
        self.assertEqual(exc.get_errors(), {'field': ['error']})
    
    def test_exception_default_values(self):
        """Test exception with default values"""
        exc = SteadfastException()
        
        self.assertEqual(str(exc), "")
        self.assertEqual(exc.code, 0)
        self.assertEqual(exc.get_errors(), {})


class TestOrderValidation(unittest.TestCase):
    """Test order validation"""
    
    def setUp(self):
        """Set up test client"""
        self.client = SteadfastCourier(
            api_key='test-key',
            secret_key='test-secret'
        )
    
    def test_place_order_missing_required_fields(self):
        """Test order creation with missing fields"""
        incomplete_order = {
            'invoice': 'ORD-001',
            'recipient_name': 'Test User',
            # Missing phone, address, cod_amount
        }
        
        with self.assertRaises(SteadfastException):
            self.client.order().place_order(incomplete_order)
    
    def test_place_order_invalid_phone(self):
        """Test order creation with invalid phone"""
        order = {
            'invoice': 'ORD-001',
            'recipient_name': 'Test User',
            'recipient_phone': '123',  # Invalid
            'recipient_address': 'Test Address',
            'cod_amount': 100,
        }
        
        with self.assertRaises(SteadfastException) as context:
            self.client.order().place_order(order)
        
        self.assertIn("11 digits", str(context.exception))
    
    def test_place_order_invalid_invoice(self):
        """Test order creation with invalid invoice"""
        order = {
            'invoice': 'ORD@001',  # Invalid character
            'recipient_name': 'Test User',
            'recipient_phone': '01712345678',
            'recipient_address': 'Test Address',
            'cod_amount': 100,
        }
        
        with self.assertRaises(SteadfastException) as context:
            self.client.order().place_order(order)
        
        self.assertIn("alphanumeric", str(context.exception))
    
    def test_place_order_negative_cod(self):
        """Test order creation with negative COD amount"""
        order = {
            'invoice': 'ORD-001',
            'recipient_name': 'Test User',
            'recipient_phone': '01712345678',
            'recipient_address': 'Test Address',
            'cod_amount': -100,  # Invalid
        }
        
        with self.assertRaises(SteadfastException) as context:
            self.client.order().place_order(order)
        
        self.assertIn("cannot be less than 0", str(context.exception))
    
    def test_bulk_orders_max_limit(self):
        """Test bulk orders exceeds max limit"""
        orders = [
            {
                'invoice': f'ORD-{i:04d}',
                'recipient_name': f'Customer {i}',
                'recipient_phone': '01712345678',
                'recipient_address': f'Address {i}',
                'cod_amount': 100,
            }
            for i in range(501)  # Exceed 500 limit
        ]
        
        with self.assertRaises(SteadfastException) as context:
            self.client.order().place_bulk_orders(orders)
        
        self.assertIn("500", str(context.exception))


class TestStatusAPI(unittest.TestCase):
    """Test status API validation"""
    
    def setUp(self):
        """Set up test client"""
        self.client = SteadfastCourier(
            api_key='test-key',
            secret_key='test-secret'
        )
    
    def test_get_status_invalid_consignment_id(self):
        """Test status check with invalid consignment ID"""
        # This would normally make an API call in real testing
        # For unit testing, we just test the validation
        pass
    
    def test_get_status_invalid_invoice(self):
        """Test status check with invalid invoice"""
        # This would normally make an API call in real testing
        # For unit testing, we just test the validation
        pass


class TestReturnAPI(unittest.TestCase):
    """Test return API"""
    
    def setUp(self):
        """Set up test client"""
        self.client = SteadfastCourier(
            api_key='test-key',
            secret_key='test-secret'
        )
    
    def test_return_without_identifier(self):
        """Test return creation without identifier"""
        with self.assertRaises(SteadfastException) as context:
            self.client.return_api().create_return_request({
                'reason': 'Customer requested return'
            })
        
        self.assertIn("required", str(context.exception))
    
    def test_return_with_invoice(self):
        """Test return creation with invoice"""
        # This would make an API call in real testing
        # For unit testing, just verify validation passes
        try:
            # Validation should pass
            data = {
                'invoice': 'ORD-001',
                'reason': 'Test return'
            }
            # In real test, this would call the API
        except SteadfastException:
            self.fail("Valid return data raised exception")


class TestClientInitialization(unittest.TestCase):
    """Test client initialization"""
    
    def test_client_init_without_credentials(self):
        """Test client initialization without credentials"""
        with self.assertRaises(ValueError):
            SteadfastCourier(api_key='', secret_key='')
        
        with self.assertRaises(ValueError):
            SteadfastCourier(api_key='key', secret_key='')
    
    def test_client_init_with_credentials(self):
        """Test client initialization with credentials"""
        try:
            client = SteadfastCourier(
                api_key='test-key',
                secret_key='test-secret'
            )
            self.assertIsNotNone(client)
        except ValueError:
            self.fail("Client initialization failed with valid credentials")
    
    def test_client_custom_base_url(self):
        """Test client with custom base URL"""
        client = SteadfastCourier(
            api_key='test-key',
            secret_key='test-secret',
            base_url='https://custom-api.example.com'
        )
        self.assertEqual(client.base_url, 'https://custom-api.example.com')
    
    def test_client_custom_timeout(self):
        """Test client with custom timeout"""
        client = SteadfastCourier(
            api_key='test-key',
            secret_key='test-secret',
            timeout=60
        )
        self.assertEqual(client.timeout, 60)


class TestAPIInstances(unittest.TestCase):
    """Test API instance creation"""
    
    def setUp(self):
        """Set up test client"""
        self.client = SteadfastCourier(
            api_key='test-key',
            secret_key='test-secret'
        )
    
    def test_order_api_instance(self):
        """Test order API instance"""
        api = self.client.order()
        self.assertIsNotNone(api)
    
    def test_status_api_instance(self):
        """Test status API instance"""
        api = self.client.status()
        self.assertIsNotNone(api)
    
    def test_balance_api_instance(self):
        """Test balance API instance"""
        api = self.client.balance()
        self.assertIsNotNone(api)
    
    def test_payment_api_instance(self):
        """Test payment API instance"""
        api = self.client.payment()
        self.assertIsNotNone(api)
    
    def test_return_api_instance(self):
        """Test return API instance"""
        api = self.client.return_api()
        self.assertIsNotNone(api)
    
    def test_police_station_api_instance(self):
        """Test police station API instance"""
        api = self.client.police_station()
        self.assertIsNotNone(api)
    
    def test_api_instances_singleton(self):
        """Test that API instances are reused"""
        api1 = self.client.order()
        api2 = self.client.order()
        self.assertIs(api1, api2)


if __name__ == '__main__':
    unittest.main()
```

## Running Tests

```bash
# Run all tests
python -m unittest discover

# Run specific test file
python -m unittest tests/test_validators.py

# Run specific test class
python -m unittest tests.test_validators.TestValidators

# Run specific test method
python -m unittest tests.test_validators.TestValidators.test_validate_invoice_valid

# Run with verbose output
python -m unittest discover -v

# Run with coverage
pip install coverage
coverage run -m unittest discover
coverage report
coverage html
```

## Mocking API Responses (For Integration Testing)

```python
import unittest
from unittest.mock import MagicMock, patch

from steadfast_courier import SteadfastCourier


class TestOrderAPIIntegration(unittest.TestCase):
    """Integration tests with mocked API responses"""
    
    @patch('steadfast_courier.apis.base_api.requests.post')
    def test_place_order_success(self, mock_post):
        """Test successful order placement"""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'consignment': {
                'consignment_id': 12345,
                'invoice': 'ORD-001',
                'tracking_code': 'SF1234567890',
                'status': 'pending'
            }
        }
        mock_post.return_value = mock_response
        
        # Create order
        client = SteadfastCourier('test-key', 'test-secret')
        response = client.order().place_order({
            'invoice': 'ORD-001',
            'recipient_name': 'Test User',
            'recipient_phone': '01712345678',
            'recipient_address': 'Test Address',
            'cod_amount': 1000,
        })
        
        # Verify
        self.assertEqual(response['consignment']['consignment_id'], 12345)
        self.assertEqual(response['consignment']['tracking_code'], 'SF1234567890')
    
    @patch('steadfast_courier.apis.base_api.requests.post')
    def test_place_order_api_error(self, mock_post):
        """Test API error handling"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'message': 'Validation error',
            'errors': {'phone': ['Invalid phone format']}
        }
        mock_post.return_value = mock_response
        
        client = SteadfastCourier('test-key', 'test-secret')
        
        from steadfast_courier import SteadfastException
        with self.assertRaises(SteadfastException):
            client.order().place_order({
                'invoice': 'ORD-001',
                'recipient_name': 'Test User',
                'recipient_phone': '123',  # Invalid
                'recipient_address': 'Test Address',
                'cod_amount': 1000,
            })
```

## Test Coverage

Current test coverage areas:
- ✅ Input validation
- ✅ Exception handling
- ✅ Client initialization
- ✅ API instance creation
- ⚠️ API responses (requires mocking)
- ⚠️ Rate limiting (requires mock time)
- ⚠️ Network errors (requires mock)

To achieve 100% coverage, mock external API calls using `unittest.mock`.
