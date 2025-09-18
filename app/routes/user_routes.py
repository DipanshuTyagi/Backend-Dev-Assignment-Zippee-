from flask import Blueprint, request, jsonify
from app.schemas.user_schema import UserRegister
from flask_pydantic import validate

from app.services.user_service import UserService


user_bp = Blueprint("users", __name__)

@user_bp.route("/register", methods=["POST"])
@validate()
def register():
    body = UserRegister(**request.get_json())
    data = body.model_dump()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    try:
        UserService.create_user(username, password, role)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 409
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500

    return jsonify({"message": "User registered successfully"}), 201