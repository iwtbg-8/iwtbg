# HTTP 405 Method Not Allowed - Fix Documentation

## Problem
Error: `HTTP 405: Method Not Allowed`

This error occurs when a client tries to access an API endpoint using an incorrect HTTP method. For example:
- Trying to use GET on an endpoint that requires POST
- Trying to use POST on an endpoint that only accepts GET
- Missing OPTIONS support for CORS preflight requests

## Root Cause

1. **Wrong HTTP Method**: Endpoints like `/api/analyze`, `/api/download`, and `/api/formats` require POST requests but might be called with GET
2. **Missing OPTIONS Support**: CORS preflight requests (OPTIONS) were not supported, causing browser CORS errors
3. **Poor Error Messages**: The default Flask 405 error didn't provide helpful information about allowed methods

## Solution Implemented

### 1. Added OPTIONS Method Support

All POST endpoints now support OPTIONS for CORS preflight:

```python
@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze_video():
    """Analyze video URL and return metadata"""
    if request.method == 'OPTIONS':
        return '', 204
    # ... rest of the code
```

This was added to:
- `/api/analyze`
- `/api/download`
- `/api/formats`

### 2. Added Custom 405 Error Handler

Created a helpful error handler that tells users:
- What method they tried to use
- What methods are allowed
- Clear error message

```python
@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors"""
    allowed_methods = error.valid_methods if hasattr(error, 'valid_methods') else []
    return jsonify({
        'error': 'Method not allowed',
        'message': f'This endpoint does not support {request.method} requests',
        'allowed_methods': list(allowed_methods) if allowed_methods else None
    }), 405
```

### 3. Enhanced API Documentation

Updated the `/api` endpoint to show detailed method information:

**Before:**
```json
{
  "endpoints": {
    "/api/analyze": "POST - Analyze video URL"
  }
}
```

**After:**
```json
{
  "endpoints": {
    "/api/analyze": {
      "methods": ["POST"],
      "description": "Analyze video URL",
      "body": {"url": "string (required)"}
    }
  }
}
```

## Endpoint Methods Reference

| Endpoint | Allowed Methods | Description |
|----------|----------------|-------------|
| `/` | GET | Serve frontend |
| `/api` | GET | API information |
| `/api/analyze` | POST, OPTIONS | Analyze video URL |
| `/api/download` | POST, OPTIONS | Download video |
| `/api/formats` | POST, OPTIONS | Get available formats |
| `/api/download-file/<filename>` | GET | Serve downloaded file |

## Testing

Created comprehensive test page: `test_405_fix.html`

Tests include:
1. ✓ Correct method usage (should succeed)
2. ✓ Wrong method usage (should fail with helpful 405 error)
3. ✓ OPTIONS preflight support (for CORS)
4. ✓ Error message clarity

## Example Error Responses

### Using GET on POST endpoint:
```json
{
  "error": "Method not allowed",
  "message": "This endpoint does not support GET requests",
  "allowed_methods": ["POST", "OPTIONS"]
}
```

### Frontend Error Handling:
```javascript
catch (error) {
    if (error.message.includes('405')) {
        console.error('Wrong HTTP method used');
        // Error message includes allowed methods
    }
}
```

## Benefits

1. ✅ **Clear Error Messages** - Users know exactly what went wrong
2. ✅ **CORS Support** - Browser preflight requests work correctly
3. ✅ **Better API Documentation** - `/api` shows allowed methods
4. ✅ **Easier Debugging** - Error includes allowed methods list
5. ✅ **Standards Compliant** - Follows HTTP/REST best practices

## Common Causes of 405 Errors

### 1. Using Wrong Method in JavaScript
```javascript
// ❌ WRONG - using default GET
fetch('/api/analyze')

// ✅ CORRECT - using POST
fetch('/api/analyze', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({url: 'https://...'})
})
```

### 2. Browser Link/Form Default
```html
<!-- ❌ WRONG - links use GET -->
<a href="/api/analyze">Analyze</a>

<!-- ✅ CORRECT - use fetch/AJAX -->
<button onclick="analyzeVideo()">Analyze</button>
```

### 3. CORS Preflight
```javascript
// Browser automatically sends OPTIONS before POST
// Server must support OPTIONS method
// Our fix handles this automatically
```

## Files Modified

- `/home/kali/Desktop/iwtbg/server.py`
  - Added OPTIONS to POST endpoints
  - Added 405 error handler
  - Enhanced API documentation

## Version
1.0.1 - Added 405 error handling and OPTIONS support

## Date
October 16, 2025

## Related Fixes
- See `JSON_ERROR_FIX.md` for JSON parsing error fixes
- Combined, these provide robust error handling for all API interactions
