"""
Helper functions for API responses
"""
from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    """Generate standardized success response"""
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code

def error_response(message, status_code=400, error_code=None, details=None):
    """Generate standardized error response"""
    response = {
        'success': False,
        'message': message
    }
    if error_code:
        response['error_code'] = error_code
    if details:
        response['details'] = details
    
    return jsonify(response), status_code

def paginated_response(data, page=1, per_page=20, total=None, message="Success"):
    """Generate paginated response"""
    response = {
        'success': True,
        'message': message,
        'data': data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'has_next': total > (page * per_page) if total else False,
            'has_prev': page > 1
        }
    }
    
    return jsonify(response), 200
