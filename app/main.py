from flask import Flask, jsonify
from pydantic import ValidationError
from app.database import db_session, init_db
from app.routes.user_routes import user_bp
from app.routes.auth_routes import auth_bp
from app.routes.task_routes import task_bp



def create_app():
    app = Flask(__name__)



    # Global error handler for Pydantic ValidationError
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        errors = []
        for error in e.errors():
            field = " -> ".join(str(loc) for loc in error["loc"])
            message = error["msg"]
            errors.append(f"{field}: {message}")
        
        return jsonify({
            "error": "Validation failed",
            "details": errors
        }), 400
        # Initialize DB
    with app.app_context():
        init_db()

    # Register blueprints (routes)
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(task_bp, url_prefix="/tasks")



    # Health check
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "message": "Flask app is healthy 🚀"}), 200

    # Close DB session after each request
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app


# Entry point for Gunicorn
app = create_app()
