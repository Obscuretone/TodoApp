# services/task_service.py

from models.Task import Task


class TaskService:
    async def create_task(self, title: str, description: str, user) -> Task:
        """
        Create a new task for the given user.
        """
        task = await Task.create(title=title, description=description, user=user)
        return task

    async def delete_task(self, task_id: str, user) -> bool:
        """
        Delete a task by its ID for the given user.
        """
        task = await Task.filter(id=task_id, user=user).first()
        if task:
            await task.delete()
            return True
        return False

    async def get_all_tasks(self, user) -> list:
        """
        Fetch all tasks for the given user.
        """
        tasks = await Task.filter(user=user).all()
        return tasks
