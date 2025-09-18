from flask import Blueprint, request, jsonify
from app.schemas.auth_schema import UserLogin, TokenResponse
from app.services.auth_service import AuthService
from flask_pydantic import validate

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
@validate()
def login():
    body = UserLogin(**request.get_json())
    username = body.username
    password = body.password

    user = AuthService.authenticate_user(username, password)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    token = AuthService.create_access_token(user.id,user.role)
    response = TokenResponse(access_token=token)
    return jsonify(response.model_dump()), 200
