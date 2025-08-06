from flask import jsonify
from typing import Any, Dict, Optional, Union

def success_response(
    data: Any = None, 
    message: str = "Success",
    status_code: int = 200,
    meta: Optional[Dict] = None
) -> tuple:
    """
    Create a standardized success response
    
    Args:
        data: The response data
        message: Success message
        status_code: HTTP status code
        meta: Additional metadata (pagination, etc.)
    
    Returns:
        Tuple of (response, status_code)
    """
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    
    if meta:
        response["meta"] = meta
    
    return jsonify(response), status_code

def error_response(
    message: str = "An error occurred",
    status_code: int = 500,
    error_code: Optional[str] = None,
    details: Optional[Dict] = None
) -> tuple:
    """
    Create a standardized error response
    
    Args:
        message: Error message
        status_code: HTTP status code
        error_code: Custom error code for client handling
        details: Additional error details
    
    Returns:
        Tuple of (response, status_code)
    """
    response = {
        "success": False,
        "message": message
    }
    
    if error_code:
        response["error_code"] = error_code
    
    if details:
        response["details"] = details
    
    return jsonify(response), status_code

def paginated_response(
    data: Any,
    total: int,
    page: int = 1,
    per_page: int = 20,
    message: str = "Success"
) -> tuple:
    """
    Create a standardized paginated response
    
    Args:
        data: The response data
        total: Total number of items
        page: Current page number
        per_page: Items per page
        message: Success message
    
    Returns:
        Tuple of (response, status_code)
    """
    meta = {
        "pagination": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        }
    }
    
    return success_response(data=data, message=message, meta=meta)