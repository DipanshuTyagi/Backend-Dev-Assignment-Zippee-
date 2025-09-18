from flask import Blueprint, request, jsonify
from app.rabc.rabc_decorators import admin_required, user_required
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService
from flask_pydantic import validate

task_bp = Blueprint("tasks", __name__)

@task_bp.route("", methods=["GET"])
@user_required
def get_tasks():
    try:
        # Pagination parameters
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))

        # Filtering by completed status (optional)
        completed_param = request.args.get("completed")
        if completed_param is not None:
            # Convert string to boolean
            if completed_param.lower() in ["true", "1"]:
                completed = True
            elif completed_param.lower() in ["false", "0"]:
                completed = False
            else:
                return jsonify({"error": "Invalid value for 'completed'. Use true or false."}), 400
        else:
            completed = None

        tasks, total = TaskService.get_all_tasks(page=page, limit=limit, completed=completed)
        response = [TaskResponse.model_validate(task).model_dump() for task in tasks]

        return jsonify({
            "total": total,
            "page": page,
            "limit": limit,
            "tasks": response
        }), 200

    except Exception as e:
        return jsonify({"error": "Failed to retrieve tasks", "details": str(e)}), 500

@task_bp.route("/<int:task_id>", methods=["GET"])
@user_required
def get_task(task_id):
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(TaskResponse.model_validate(task).model_dump()), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve task", "details": str(e)}), 500

@task_bp.route("", methods=["POST"])
@validate()
@user_required
def create_task():
    try:
        data = TaskCreate(**request.get_json())
        task = TaskService.create_task(title=data.title, description=data.description, completed=data.completed)
        return jsonify(TaskResponse.model_validate(task).model_dump()), 201
    except Exception as e:
        return jsonify({"error": "Failed to create task", "details": str(e)}), 500

@task_bp.route("/<int:task_id>", methods=["PUT"])
@validate()
@user_required
def update_task(task_id):
    try:
        data = TaskUpdate(**request.get_json())
        task = TaskService.update_task(
            task_id,
            title=data.title,
            description=data.description,
            completed=data.completed
        )
        if not task:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(TaskResponse.model_validate(task).model_dump()), 200
    except Exception as e:
        return jsonify({"error": "Failed to update task", "details": str(e)}), 500

@task_bp.route("/<int:task_id>", methods=["DELETE"])
@admin_required
def delete_task(task_id):
    try:
        success = TaskService.delete_task(task_id)
        if not success:
            return jsonify({"error": "Task not found"}), 404
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete task", "details": str(e)}), 500
