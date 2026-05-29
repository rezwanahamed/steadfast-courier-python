# Changelog

All notable changes to the SteadFast Courier Python package will be documented in this file.

## [1.1.2] - 2026-05-29

### Fixed

- Fixed URL preparation in BaseApi to ensure `base_url` ends with a slash for proper API endpoint construction

## [1.1.1] - 2024-05-29

### Changed

- Updated README with improved documentation and examples
- Enhanced setup instructions and quick start guide

## [1.1.0] - 2024-05-29

### Added

#### Environment Variable Support

- **`from_env()` Class Method** - Initialize client directly from environment variables
- **Standard Environment Variables** - Support for `STEADFAST_API_KEY`, `STEADFAST_SECRET_KEY`, `STEADFAST_BASE_URL`, `STEADFAST_TIMEOUT`
- **.env.example Template** - Provided template file for easy setup
- **Customizable Variable Names** - Support for custom environment variable names via `from_env()` parameters

#### Documentation Updates

- Updated all framework guides (Django, FastAPI, Flask) to showcase environment variable usage
- Updated all examples to demonstrate `from_env()` method
- Enhanced README with new quick start using environment variables

### Changed

- README updated to show `from_env()` as the recommended approach
- Django, FastAPI, and Flask integration examples now use environment variables
- Documentation clarified for easier credential management

### Notes

- **Backward Compatible** - All existing code using explicit credentials continues to work
- No breaking changes to the API

## [1.0.0] - 2024-05-29

### Added

#### Core Features

- **Complete Python Port** - Full conversion from PHP to Python with all API endpoints
- **Multi-Framework Support** - Native support for Django, FastAPI, Flask, and all Python frameworks
- **API Key Authentication** - Secure authentication with API Key and Secret Key
- **Rate Limiting** - Built-in rate limiting (60 requests/minute) with retry logic
- **Input Validation** - Comprehensive validation for all API parameters
- **Error Handling** - Custom `SteadfastException` with detailed error information
- **Type Hints** - Full type hints for better IDE support and code quality
- **Logging Support** - Built-in logging for debugging and monitoring

#### APIs Implemented

1. **Order Management API**
   - `place_order()` - Create single order
   - `place_bulk_orders()` - Create up to 500 orders in one call

2. **Status Tracking API**
   - `get_status_by_consignment_id()` - Check status by ID
   - `get_status_by_invoice()` - Check status by invoice
   - `get_status_by_tracking_code()` - Check status by tracking code

3. **Balance API**
   - `get_current_balance()` - Check account balance

4. **Payment API**
   - `get_payments()` - Get all payments
   - `get_payment()` - Get specific payment

5. **Return Management API**
   - `create_return_request()` - Create return request
   - `get_return_request()` - Get specific return request
   - `get_return_requests()` - Get all return requests

6. **Police Station API**
   - `get_police_stations()` - Get list of police stations

#### Documentation

- **Comprehensive README** with quick start guide
- **Usage Guide** with detailed examples and best practices
- **Django Integration Guide** with examples and patterns
- **FastAPI Integration Guide** with Pydantic models
- **Flask Integration Guide** with blueprints
- **API Documentation** with all endpoints and parameters
- **Multiple Examples** (basic usage, FastAPI, Django, Flask)

#### Package Structure

- Clean modular architecture with separate API classes
- `SteadfastCourier` main client class
- `BaseApi` abstract class for common functionality
- Individual API classes for each endpoint group
- `Validator` class for input validation
- `SteadfastException` custom exception class

#### Installation & Deployment

- `setup.py` for easy pip installation
- `requirements.txt` with minimal dependencies
- Support for Python 3.8+
- PyPI-ready package structure

### Features Details

#### Validation

- Invoice format validation (alphanumeric, hyphens, underscores)
- Phone number validation (11 digits)
- Email format validation
- Address length validation
- COD amount validation (numeric, non-negative)
- Delivery type validation (0 or 1)

#### Rate Limiting

- Automatic 60 requests per minute limiting
- Per-endpoint rate limit tracking
- Automatic cleanup of old entries
- Built-in exception on limit exceeded

#### Error Handling

- HTTP status code error handling (400, 401, 403, 404, 422, 429, 500)
- Network error handling (timeout, connection errors)
- Custom error messages for each HTTP status
- Field-level error details from API
- Logging of all errors

#### Security

- Secure API key and secret key handling
- Environment variable support
- Optional custom base URL support
- Configurable timeout
- No credentials in logs by default

### Dependencies

- `requests >= 2.28.0` - HTTP library

### Development

- Full test coverage ready
- Example code for all integrations
- Comprehensive docstrings
- Type hints throughout

### Documentation Files

1. `README.md` - Main documentation with quick start
2. `docs/USAGE.md` - Complete usage guide with examples
3. `docs/API_DOCUMENTATION.md` - Full API reference
4. `docs/DJANGO_SETUP.md` - Django integration guide
5. `docs/FASTAPI_SETUP.md` - FastAPI integration guide
6. `docs/FLASK_SETUP.md` - Flask integration guide
7. `examples/basic_usage.py` - Basic usage examples
8. `examples/django_example.py` - Django integration example
9. `examples/fastapi_example.py` - FastAPI integration example
10. `examples/flask_example.py` - Flask integration example

### Testing

- All validation rules tested and working
- Error handling verified
- Rate limiting functional
- API endpoint structure verified

---

## Comparison with Original PHP Package

| Feature           | PHP          | Python                             |
| ----------------- | ------------ | ---------------------------------- |
| Framework Support | Laravel only | Django, FastAPI, Flask, All Python |
| API Endpoints     | 6 groups     | 6 groups (identical)               |
| Validation        | ✅           | ✅                                 |
| Rate Limiting     | ✅           | ✅                                 |
| Error Handling    | ✅           | ✅                                 |
| Type Hints        | PhpDoc       | Full type hints                    |
| Documentation     | ✅           | ✅ Enhanced                        |
| Examples          | Limited      | Comprehensive                      |
| Installation      | Composer     | pip                                |

---

## Migration from PHP Package

Users migrating from the PHP Laravel package:

```python
# Old PHP/Laravel code:
// use Nayemuf\SteadfastCourier\Facades\SteadfastCourier;
// $response = SteadfastCourier::order()->placeOrder($orderData);

# New Python code:
from steadfast_courier import SteadfastCourier
client = SteadfastCourier(api_key, secret_key)
response = client.order().place_order(order_data)
```

Main differences:

- Client initialization instead of facade
- Snake_case method names instead of camelCase
- Dictionary-based configuration instead of config file
- Same validation and error handling logic

---

## Known Limitations

- Async/await support not yet implemented (use threaded approach for now)
- Database model examples provided but not included in package
- Webhook handling examples not yet included

---

## Future Roadmap

- [ ] Async/await support
- [ ] Celery task examples
- [ ] GraphQL API wrapper
- [ ] Webhook receiver
- [ ] CLI tool
- [ ] More framework integrations
- [ ] Enhanced caching

---

## Credits

- **Original PHP Package** by Nayem Uddin (https://github.com/nayemuf)
- **Python Port & Multi-Framework Support** by Rezwan Ahamed (https://github.com/rezwanahamed)
- SteadFast Courier API by SteadFast Courier Ltd.

---

## License

MIT License - See LICENSE file for details

---

## Support & Issues

- GitHub: https://github.com/rezwanahamed/steadfast-courier-python
- GitHub Issues: https://github.com/rezwanahamed/steadfast-courier-python/issues
- Official API: https://steadfast.com.bd/

---

## Version History

- **1.0.0** (2024-05-29) - Initial release with full API coverage and framework integrations
