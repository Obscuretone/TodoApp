from sanic.response import json
from sanic_openapi import doc
from uuid import UUID
from services.task_service import TaskService
from services.llm_service import LLMService
from models.User import User
from models.Task import Task
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

        self.app.add_route(self.get_all_projects, "/projects", methods=["GET"])
        self.app.add_route(self.get_task, "/tasks/<task_id>", methods=["GET"])

        self.app.add_route(self.split_task, "/tasks/<task_id>/split", methods=["POST"])
        self.app.add_route(self.edit_task, "/tasks/<task_id>", methods=["PATCH"])

    # TODO: Get rid of this helper function
    def get_user_by_uuid(self, user_uuid: UUID) -> Optional[User]:
        """
        Helper function to retrieve user by UUID.
        """
        return User.filter(uuid=user_uuid).first()

    @doc.summary("Get task with subtasks")
    @doc.description(
        "Fetch a task by its ID and return all its subtasks with pagination support."
    )
    async def get_task(self, request: Request, task_id: str) -> HTTPResponse:
        """
        Fetch a task and its subtasks by task ID with pagination.
        """
        user_uuid = request.ctx.user_uuid  # Assuming user is authenticated

        if task_id == "00000000-0000-0000-0000-000000000000":
            return json(
                {"error": "Invalid task ID: Project parent task cannot be accessed."},
                status=400,
            )

        try:
            task_uuid = UUID(task_id)
        except ValueError:
            return json({"error": "Invalid task ID"}, status=400)

        # Get user by UUID
        user = await self.get_user_by_uuid(user_uuid)
        if not user:
            return json({"error": "User not found"}, status=404)

        # Fetch the task by UUID
        task = await self.task_service.get_task_by_id(task_uuid, user)
        if not task:
            return json({"error": "Task not found"}, status=404)

        # Get pagination parameters from the query string
        page = int(request.args.get("page", 1))  # Default to page 1 if not provided
        page_size = int(
            request.args.get("page_size", 10)
        )  # Default to 10 tasks per page

        # Fetch subtasks of the task with pagination
        subtasks = await self.task_service.get_subtasks(user, task, page, page_size)

        # Prepare the response data with task and subtasks
        subtasks_data = [
            {
                "uuid": str(subtask.id),
                "title": subtask.title,
                "description": subtask.description,
                "user_id": str(subtask.user_id),
                "created_at": subtask.created_at.isoformat(),
            }
            for subtask in subtasks
        ]

        task_data = {
            "uuid": str(task.id),
            "title": task.title,
            "description": task.description,
            "user_id": str(task.user_id),
            "created_at": task.created_at.isoformat(),
            "parent_id": str(task.parent_task_id),
        }

        return json({"task": task_data, "subtasks": subtasks_data}, status=200)

    @doc.summary("Edit a task")
    @doc.description("Edit the details of an existing task.")
    @doc.produces({"message": str, "task": dict})
    async def edit_task(self, request: Request, task_id: str) -> HTTPResponse:
        """
        Edit an existing task's details like title, description, and parent task.
        """
        data = request.json
        title = data.get("title")
        description = data.get("description")
        parent_uuid = data.get("parent_uuid")  # Optional field

        user_uuid = request.ctx.user_uuid  # Assuming user is authenticated

        try:
            task_uuid = UUID(task_id)  # Ensure the task ID is valid
        except ValueError:
            return json({"error": "Invalid task ID"}, status=400)

        # Get the user by UUID
        user = await self.get_user_by_uuid(user_uuid)
        if not user:
            return json({"error": "User not found"}, status=404)

        # Fetch the task from the service layer (should be authorized by user context)
        task = await self.task_service.get_task_by_id(task_uuid, user)
        if not task:
            return json({"error": "Task not found"}, status=404)

        # Check for parent_uuid and validate it (ensure it's valid or default it)
        if parent_uuid:
            parent_task = await Task.filter(id=parent_uuid).first()
            if not parent_task:
                return json({"error": "Parent task not found"}, status=404)

        # Update task details
        updated_fields = {}
        if title:
            updated_fields["title"] = title
        if description:
            updated_fields["description"] = description
        if parent_uuid:
            updated_fields["parent_task"] = parent_task

        # Update the task via the service
        updated_task = await self.task_service.update_task(task, updated_fields)

        # Prepare response data for the updated task
        response_data = {
            "uuid": str(updated_task.id),
            "title": updated_task.title,
            "description": updated_task.description,
            "user_id": str(updated_task.user.uuid),
            "created_at": updated_task.created_at.isoformat(),
        }

        return json({"message": "Task updated", "task": response_data}, status=200)

    @doc.summary("Create a task")
    @doc.description(
        "Create a new task by providing title, description, and the authenticated user."
    )
    @doc.produces({"message": str, "task": dict})
    async def create_task(self, request: Request) -> HTTPResponse:
        """
        Create a new task for the authenticated user, optionally as a subtask.
        """
        data = request.json
        title = data.get("title")
        description = data.get("description")
        parent_uuid = data.get("parent_uuid")  # Optional parent UUID
        user_uuid = request.ctx.user_uuid  # Assuming user is authenticated

        # Validate title
        if not title:
            return json({"error": "Title is required"}, status=400)

        # Get user
        user = await self.get_user_by_uuid(user_uuid)
        if not user:
            return json({"error": "User not found"}, status=404)

        # If parent_uuid is provided, validate that the parent task exists
        if parent_uuid:
            parent_task = await Task.filter(id=parent_uuid).first()
            if not parent_task:
                return json({"error": "Parent task not found"}, status=404)
        else:
            parent_uuid = "00000000-0000-0000-0000-000000000000"

        # Create the new task
        task = await self.task_service.create_task(
            title, description, user, parent_uuid
        )

        # Prepare the response data
        response_data = {
            "uuid": str(task.id),
            "title": task.title,
            "description": task.description,
            "user_id": str(task.user.uuid),
            "created_at": task.created_at.isoformat(),
        }

        # Return the response with the created task
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

    @doc.summary("Get all projects")
    @doc.description("Fetch all projects for the authenticated user.")
    async def get_all_projects(self, request: Request) -> HTTPResponse:
        """
        Fetch all tasks for the authenticated user, including subtask count.
        """
        user_uuid = request.ctx.user_uuid  # Assuming user is authenticated

        user = await self.get_user_by_uuid(user_uuid)
        if not user:
            return json({"error": "User not found"}, status=404)

        tasks = await self.task_service.get_all_projects(user)

        # Assuming tasks is a list of task objects, and each task has a user attribute that needs to be fetched asynchronously
        response_data: List[Dict[str, str]] = []

        # Use an async for loop to handle the asynchronous task.user call
        for task in tasks:
            # Count the subtasks for the current task
            subtask_count = await Task.filter(parent_task=task).count()

            # Append the task data to the response_data list
            response_data.append(
                {
                    "uuid": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "user_id": str(task.user_id),  # Ensure user_id is a string
                    "created_at": task.created_at.isoformat(),
                    "subtask_count": subtask_count,  # Add the subtask count
                }
            )

        return json(response_data, status=200)

    @doc.summary("Get task with subtasks")
    @doc.description("Fetch a task by its ID and return all its subtasks.")
    async def get_task(self, request: Request, task_id: str) -> HTTPResponse:
        """
        Fetch a task and its subtasks by task ID.
        """
        user_uuid = request.ctx.user_uuid  # Assuming user is authenticated

        if task_id == "00000000-0000-0000-0000-000000000000":
            return json(
                {"error": "Invalid task ID: Project parent task cannot be accessed."},
                status=400,
            )

        try:
            task_uuid = UUID(task_id)
        except ValueError:
            return json({"error": "Invalid task ID"}, status=400)

        # Get user by UUID
        user = await self.get_user_by_uuid(user_uuid)
        if not user:
            return json({"error": "User not found"}, status=404)

        # Fetch the task by UUID
        task = await self.task_service.get_task_by_id(task_uuid, user)
        if not task:
            return json({"error": "Task not found"}, status=404)

        # Fetch subtasks of the task
        subtasks = await Task.filter(parent_task=task).all()

        # Prepare the response data with task and subtasks
        subtasks_data = [
            {
                "uuid": str(subtask.id),
                "title": subtask.title,
                "description": subtask.description,
                "user_id": str(subtask.user_id),
                "created_at": subtask.created_at.isoformat(),
            }
            for subtask in subtasks
        ]

        task_data = {
            "uuid": str(task.id),
            "title": task.title,
            "description": task.description,
            "user_id": str(task.user_id),
            "created_at": task.created_at.isoformat(),
            "parent_id": str(task.parent_task_id),
        }

        return json({"task": task_data, "subtasks": subtasks_data}, status=200)

    @doc.summary("Split a task into two subtasks")
    @doc.description(
        "Use LLM to split a task into two subtasks for the authenticated user."
    )
    async def split_task(self, request: Request, task_id: str) -> HTTPResponse:
        """
        Split a task into multiple subtasks based on the provided count.
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
            # Get the number of subtasks from the request body
            data = request.json  # Read the JSON body from the request
            num_subtasks = data.get("count", 2)  # Default to 2 if no count is provided

            # Validate that the number of subtasks is within the allowed range
            if num_subtasks < 1 or num_subtasks > 5:
                return json(
                    {"error": "You can only split the task into 1 to 5 subtasks."},
                    status=400,
                )

            # Call the TaskService to split the task into subtasks
            subtasks = await self.task_service.split_task(
                parent_task=task,  # Pass the task itself as the parent task
                num_subtasks=num_subtasks,  # Use the provided number of subtasks
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
                            subtask.user.uuid
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
        except Exception as e:
            # Catch any other errors and return an appropriate response
            return json({"error": f"Unexpected error: {str(e)}"}, status=500)
