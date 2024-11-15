from sanic.response import json
from sanic_openapi import doc
from uuid import UUID
from services.task_service import TaskService
from services.llm_service import LLMService
from models.User import User
from sanic.exceptions import SanicException
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import List, Dict, Optional


class TaskController:

    def __init__(self, app, task_service: TaskService) -> None:
        self.app = app  # Inject the app instance into the controller
        self.task_service = task_service

        # Register routes
        self.app.add_route(self.create_task, "/tasks", methods=["POST"])
        self.app.add_route(self.delete_task, "/tasks/<task_id>", methods=["DELETE"])
        self.app.add_route(self.get_all_tasks, "/tasks", methods=["GET"])
        self.app.add_route(self.split_task, "/tasks/<task_id>/split", methods=["POST"])

    def get_user_by_uuid(self, user_uuid: UUID) -> Optional[User]:
        """
        Helper function to retrieve user by UUID.
        """
        return User.filter(uuid=user_uuid).first()

    @doc.summary("Create a task")
    @doc.description(
        "Create a new task by providing title, description, and the authenticated user."
    )
    @doc.produces({"message": str, "task": dict})
    async def create_task(self, request: Request) -> HTTPResponse:
        """
        Create a new task for the authenticated user.
        """
        data = request.json
        title = data.get("title")
        description = data.get("description")
        user_uuid = request.ctx.user_uuid  # Assuming user is authenticated

        if not title:
            return json({"error": "Title is required"}, status=400)

        user = await self.get_user_by_uuid(user_uuid)
        if not user:
            return json({"error": "User not found"}, status=404)

        task = await self.task_service.create_task(title, description, user)

        response_data = {
            "uuid": str(task.id),
            "title": task.title,
            "description": task.description,
            "user_id": str(task.user.uuid),
            "created_at": task.created_at.isoformat(),
        }

        return json({"message": "Task created", "task": response_data}, status=201)

    @doc.summary("Delete a task")
    @doc.description("Delete a task by its ID for the authenticated user.")
    async def delete_task(self, request: Request, task_id: str) -> HTTPResponse:
        """
        Delete a task for the authenticated user.
        """
        user_uuid = request.ctx.user_uuid  # Assuming user is authenticated

        try:
            task_uuid = UUID(task_id)
        except ValueError:
            return json({"error": "Invalid task ID"}, status=400)

        user = await self.get_user_by_uuid(user_uuid)
        if not user:
            return json({"error": "User not found"}, status=404)

        deleted = await self.task_service.delete_task(task_uuid, user)
        if deleted:
            return json({"message": "Task deleted"}, status=200)

        return json({"error": "Task not found"}, status=404)

    @doc.summary("Get all tasks")
    @doc.description("Fetch all tasks for the authenticated user.")
    async def get_all_tasks(self, request: Request) -> HTTPResponse:
        """
        Fetch all tasks for the authenticated user.
        """
        user_uuid = request.ctx.user_uuid  # Assuming user is authenticated

        user = await self.get_user_by_uuid(user_uuid)
        if not user:
            return json({"error": "User not found"}, status=404)

        tasks = await self.task_service.get_all_tasks(user)

        response_data: List[Dict[str, str]] = [
            {
                "uuid": str(task.uuid),
                "title": task.title,
                "description": task.description,
                "user_id": str(task.user.id),
                "created_at": task.created_at.isoformat(),
            }
            for task in tasks
        ]

        return json({"tasks": response_data}, status=200)

    @doc.summary("Split a task into two subtasks")
    @doc.description(
        "Use LLM to split a task into two subtasks for the authenticated user."
    )
    async def split_task(self, request: Request, task_id: str) -> HTTPResponse:
        """
        Split a task into two subtasks for the authenticated user.
        """
        user_uuid = request.ctx.user_uuid  # Assuming user is authenticated

        # Fetch the user by UUID
        user = await self.get_user_by_uuid(user_uuid)
        if not user:
            return json({"error": "User not found"}, status=404)

        # Fetch the task by ID for the user
        task = await self.task_service.get_task_by_id(task_id, user)
        if not task:
            return json({"error": "Task not found"}, status=404)

        try:
            # Call the TaskService to split the task into subtasks
            subtasks = await self.task_service.split_task(
                parent_task=task,  # Pass the task itself as the parent task
                num_subtasks=2,  # Default number of subtasks is 2
            )

            # Prepare the response with details of the created subtasks
            created_subtasks = []
            for subtask in subtasks:
                created_subtasks.append(
                    {
                        "uuid": str(subtask.id),  # Use the task's UUID
                        "title": subtask.title,  # Subtask title
                        "description": subtask.description,  # Subtask description
                        "user_id": str(
                            subtask.user.id
                        ),  # User ID associated with the subtask
                        "created_at": subtask.created_at.isoformat(),  # Creation time in ISO format
                    }
                )

            return json(
                {"message": "Task split successfully", "subtasks": created_subtasks},
                status=200,
            )
        except ValueError as e:
            # If there was an issue with the task splitting, handle the exception
            return json({"error": str(e)}, status=400)
