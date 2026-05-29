# Project Structure Documentation

## 📁 Directory Layout

```
steadfast-courier-python/
│
├── steadfast_courier/                    # Main package directory
│   ├── __init__.py                       # Package initialization
│   ├── client.py                         # Main SteadfastCourier client
│   ├── exceptions.py                     # Custom exception classes
│   ├── validators.py                     # Input validation utilities
│   │
│   └── apis/                             # API implementations
│       ├── __init__.py                   # APIs module init
│       ├── base_api.py                   # Base class for all APIs
│       ├── balance_api.py                # Balance API
│       ├── order_api.py                  # Order management API
│       ├── payment_api.py                # Payment API
│       ├── police_station_api.py         # Police station API
│       ├── return_api.py                 # Return management API
│       └── status_api.py                 # Status tracking API
│
├── docs/                                 # Documentation directory
│   ├── USAGE.md                          # Complete usage guide
│   ├── API_DOCUMENTATION.md              # Full API reference
│   ├── DJANGO_SETUP.md                   # Django integration guide
│   ├── FASTAPI_SETUP.md                  # FastAPI integration guide
│   └── FLASK_SETUP.md                    # Flask integration guide
│
├── examples/                             # Example code directory
│   ├── basic_usage.py                    # Basic Python usage examples
│   ├── django_example.py                 # Django integration example
│   ├── fastapi_example.py                # FastAPI integration example
│   └── flask_example.py                  # Flask integration example
│
├── README.md                             # Main project README
├── INSTALLATION.md                       # Installation & quick setup guide
├── CHANGELOG.md                          # Version history and changes
├── LICENSE                               # MIT License
├── setup.py                              # Package setup configuration
├── requirements.txt                      # Python dependencies
├── .gitignore                            # Git ignore rules
└── tests.py                              # Unit tests and examples

```

## 📄 File Descriptions

### Core Package Files

#### `steadfast_courier/__init__.py`

- Package initialization file
- Exports main classes: `SteadfastCourier`, `SteadfastException`
- Version and author information

#### `steadfast_courier/client.py`

- **Main client class**: `SteadfastCourier`
- Initializes with API Key and Secret Key
- Provides methods to access all API instances
- Lazy initialization of API instances for efficiency
- Features:
  - Error validation on initialization
  - Custom base URL support
  - Custom timeout support
  - Singleton pattern for API instances

#### `steadfast_courier/exceptions.py`

- **Custom exception class**: `SteadfastException`
- Extends Python's built-in Exception
- Stores error code, message, and detailed errors
- Methods:
  - `__str__()`: String representation
  - `get_errors()`: Retrieve error details

#### `steadfast_courier/validators.py`

- **Validation utilities class**: `Validator`
- Static methods for validating input data
- Validates:
  - Invoice format (alphanumeric, hyphens, underscores)
  - Phone numbers (11 digits)
  - Email format
  - Address length (max 250 chars)
  - COD amount (numeric, non-negative)
  - Delivery type (0 or 1)
  - Names (max 100 chars)

### API Implementation Files

#### `steadfast_courier/apis/__init__.py`

- Exports all API classes
- Makes API imports convenient

#### `steadfast_courier/apis/base_api.py`

- **Base class for all APIs**: `BaseApi`
- Implements common functionality:
  - HTTP request handling (GET, POST, PUT, DELETE)
  - Rate limiting (60 requests/minute)
  - Error handling and logging
  - Request/response formatting
- Constants:
  - `RATE_LIMIT_PER_MINUTE = 60`
  - `DEFAULT_BASE_URL` (SteadFast API URL)
- Methods:
  - `_make_request()`: Main request method
  - `_check_rate_limit()`: Rate limiting logic

#### `steadfast_courier/apis/order_api.py`

- **Order Management API**: `OrderApi`
- Methods:
  - `place_order()`: Create single order
  - `place_bulk_orders()`: Create up to 500 orders
  - `_validate_order_data()`: Validate order data

#### `steadfast_courier/apis/status_api.py`

- **Status Tracking API**: `StatusApi`
- Methods:
  - `get_status_by_consignment_id()`: Get status by ID
  - `get_status_by_invoice()`: Get status by invoice
  - `get_status_by_tracking_code()`: Get status by tracking code

#### `steadfast_courier/apis/balance_api.py`

- **Balance API**: `BalanceApi`
- Methods:
  - `get_current_balance()`: Check account balance

#### `steadfast_courier/apis/payment_api.py`

- **Payment Management API**: `PaymentApi`
- Methods:
  - `get_payments()`: Get all payments
  - `get_payment()`: Get specific payment

#### `steadfast_courier/apis/return_api.py`

- **Return Management API**: `ReturnApi`
- Methods:
  - `create_return_request()`: Create return request
  - `get_return_request()`: Get specific return request
  - `get_return_requests()`: Get all return requests

#### `steadfast_courier/apis/police_station_api.py`

- **Police Station API**: `PoliceStationApi`
- Methods:
  - `get_police_stations()`: Get list of police stations

### Documentation Files

#### `README.md`

- Main project documentation
- Features overview
- Requirements and installation
- Quick start examples
- Framework integration previews
- API reference overview
- Error handling examples
- Security best practices
- Contributing information

#### `INSTALLATION.md`

- Quick installation guide
- Setup instructions
- Environment configuration
- Basic usage for each framework
- Troubleshooting guide
- Common tasks reference

#### `docs/USAGE.md`

- Comprehensive usage guide
- Detailed API reference
- Complete parameter documentation
- Error handling patterns
- Best practices
- Logging setup
- Testing examples

#### `docs/API_DOCUMENTATION.md`

- Full API reference document
- All endpoints with details
- Request/response structures
- Status codes and error handling
- Rate limiting information
- Security best practices

#### `docs/DJANGO_SETUP.md`

- Django framework integration guide
- Settings configuration
- View examples
- Service layer pattern
- Celery async task integration
- Database model examples
- Error handling middleware
- Logging configuration

#### `docs/FASTAPI_SETUP.md`

- FastAPI framework integration guide
- Configuration setup
- API endpoint examples
- Pydantic models
- Dependency injection
- Error handlers
- Complete working example

#### `docs/FLASK_SETUP.md`

- Flask framework integration guide
- Configuration setup
- Blueprint organization
- View examples
- Service layer pattern
- Database integration with SQLAlchemy
- Error handling
- Complete working example

#### `CHANGELOG.md`

- Version history
- Feature changes for each version
- Migration guide from PHP package
- Known limitations
- Future roadmap
- Credits

### Example Files

#### `examples/basic_usage.py`

- Basic Python usage examples
- Order creation examples
- Status checking examples
- Balance checking examples
- Bulk operations
- Error handling with retry logic
- Complete working examples

#### `examples/django_example.py`

- Django integration example
- Views implementation
- URL configuration
- Settings setup
- Model example

#### `examples/fastapi_example.py`

- FastAPI integration example
- Routes/endpoints
- Pydantic models
- Error handling
- Complete working application

#### `examples/flask_example.py`

- Flask integration example
- Routes implementation
- Error handling
- Service layer pattern
- Complete working application

### Configuration Files

#### `setup.py`

- Package configuration for PyPI
- Metadata (author, description, version)
- Dependencies specification
- Entry points
- Classifiers for PyPI

#### `requirements.txt`

- Python package dependencies
- Currently only: `requests>=2.28.0`

#### `.gitignore`

- Git ignore patterns
- Python cache files
- Virtual environments
- IDE configurations
- Build artifacts
- Logs

#### `LICENSE`

- MIT License text
- Copyright information

### Test Files

#### `tests.py`

- Comprehensive unit tests
- Validator tests
- Exception handling tests
- Order validation tests
- API initialization tests
- Mocking examples for integration tests
- Test coverage information

## 🔄 Data Flow

### Request Flow

```
User Code
    ↓
SteadfastCourier (client.py)
    ↓
API Instance (e.g., OrderApi)
    ↓
BaseApi._make_request()
    ↓
Validator (if needed)
    ↓
HTTP Request (requests library)
    ↓
SteadFast API
    ↓
Response Processing
    ↓
Return to User
```

### Error Handling Flow

```
API Request
    ↓
Error Occurs?
    ├─ No → Return JSON response
    └─ Yes → Check status code
              ├─ 4xx → Validation/Client error
              ├─ 5xx → Server error
              ├─ Network error → Connection issue
              └─ All → Raise SteadfastException
                        ↓
                    User Catches Exception
```

## 📊 Class Hierarchy

```
BaseApi
├── OrderApi
├── StatusApi
├── BalanceApi
├── PaymentApi
├── ReturnApi
└── PoliceStationApi

SteadfastCourier
└── (Initializes and manages API instances)

SteadfastException (extends Exception)

Validator
└── (Static validation methods)
```

## 🎯 Usage Patterns

### Pattern 1: Direct Usage

```python
from steadfast_courier import SteadfastCourier

client = SteadfastCourier(api_key, secret_key)
response = client.order().place_order(data)
```

### Pattern 2: Service Layer

```python
class CourierService:
    def __init__(self):
        self.client = SteadfastCourier(api_key, secret_key)

    def create_order(self, data):
        return self.client.order().place_order(data)
```

### Pattern 3: Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()
client = SteadfastCourier(
    api_key=os.getenv('STEADFAST_API_KEY'),
    secret_key=os.getenv('STEADFAST_SECRET_KEY')
)
```

## 🔐 Configuration Options

### Required

- `api_key` (str): SteadFast API Key
- `secret_key` (str): SteadFast Secret Key

### Optional

- `base_url` (str): Custom API base URL
- `timeout` (int): Request timeout in seconds (default: 30)

## 📈 Performance Considerations

1. **API Instances**: Lazily initialized and reused
2. **Rate Limiting**: Automatic enforcement of 60 requests/minute
3. **Caching**: Rate limit tracking using in-memory dict
4. **Logging**: Debug and error logging available
5. **Validation**: Pre-request validation reduces API errors

## 🔗 Dependencies

- **requests**: HTTP library for making API calls
- **No external framework requirements**: Framework-agnostic core

## 📝 Documentation Coverage

- ✅ Installation guide
- ✅ Quick start guide
- ✅ Complete API documentation
- ✅ Framework integration guides (Django, FastAPI, Flask)
- ✅ Code examples for each use case
- ✅ Testing examples
- ✅ Error handling guide
- ✅ Best practices guide

## 🚀 Getting Started

1. Start with [README.md](README.md) for overview
2. Follow [INSTALLATION.md](INSTALLATION.md) for setup
3. Use [examples/basic_usage.py](examples/basic_usage.py) for basic understanding
4. Read [docs/USAGE.md](docs/USAGE.md) for complete reference
5. Choose framework guide: [Django](docs/DJANGO_SETUP.md), [FastAPI](docs/FASTAPI_SETUP.md), or [Flask](docs/FLASK_SETUP.md)
6. Run [tests.py](tests.py) to understand testing patterns

---

**Package is production-ready and fully documented!** 🎉
