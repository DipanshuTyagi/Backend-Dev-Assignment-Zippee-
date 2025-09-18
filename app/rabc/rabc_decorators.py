from functools import wraps
from flask import request, jsonify
from app.services.auth_service import AuthService  # make sure this imports your class


def get_token_payload():
    """Extract JWT token from Authorization header and decode it using AuthService."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, "Authorization header missing or invalid"

    token = auth_header.split(" ")[1]
    payload = AuthService.decode_access_token(token)
    if payload is None:
        return None, "Invalid or expired token"

    return payload, None

def user_required(f):
    """Decorator to allow user and admin roles."""
    @wraps(f)
    def decorated(*args, **kwargs):
        payload, error = get_token_payload()
        if error:
            return jsonify({"error": error}), 401

        role = payload.get("role")
        if role not in ["user", "admin"]:
            return jsonify({"error": "Access denied"}), 403

        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator to allow only admin role."""
    @wraps(f)
    def decorated(*args, **kwargs):
        payload, error = get_token_payload()
        if error:
            return jsonify({"error": error}), 401

        role = payload.get("role")
        if role != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return f(*args, **kwargs)
    return decorated
