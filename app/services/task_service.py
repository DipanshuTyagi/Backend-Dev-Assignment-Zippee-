from app.models.task import Task
from app.database import db_session
from typing import List, Optional, Tuple

class TaskService:
    @staticmethod
    def get_all_tasks(
        page: int = 1,
        limit: int = 10,
        completed: Optional[bool] = None
    ) -> Tuple[List[Task], int]:
        """
        Returns a paginated list of tasks with optional filtering by completed status.
        """
        query = db_session.query(Task)

        # Apply filter if completed status is provided
        if completed is not None:
            query = query.filter(Task.completed == completed)

        total = query.count()
        tasks = query.offset((page - 1) * limit).limit(limit).all()
        return tasks, total

    @staticmethod
    def get_task_by_id(task_id: int):
        return db_session.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def create_task(title: str, description: str = "", completed: bool = False) -> Task:
        new_task = Task(title=title, description=description, completed=completed)
        db_session.add(new_task)
        db_session.commit()
        db_session.refresh(new_task)
        return new_task

    @staticmethod
    def update_task(task_id: int, title: str = None, description: str = None, completed: bool = None):
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return None
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        db_session.commit()
        db_session.refresh(task)
        return task

    @staticmethod
    def delete_task(task_id: int) -> bool:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return False
        db_session.delete(task)
        db_session.commit()
        return True
