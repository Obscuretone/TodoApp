from models.Task import Task
from models.User import User
from services.llm_service import LLMService
from tortoise.exceptions import DoesNotExist
import json
from typing import List


class TaskService:
    def __init__(self, llm_service: LLMService):
        """
        Initialize the TaskService with the LLMService dependency.
        """
        self.llm_service = llm_service  # Fixed the trailing dot

    async def get_task_by_id(self, task_id: str, user) -> Task:
        """
        Fetch a task by its ID for the given user.
        """
        try:
            task = await Task.get(id=task_id, user=user)
            return task
        except DoesNotExist:
            return None  # Task not found

    async def update_task(self, task: Task, updated_fields: dict) -> Task:
        """
        Update a task with the provided fields and save it to the database.
        """
        for field, value in updated_fields.items():
            setattr(task, field, value)

        await task.save()  # Save the updated task to the database
        return task

    async def create_task(
        self,
        title: str,
        description: str,
        user,
        parent_task_id: str = "00000000-0000-0000-0000-000000000000",
    ) -> Task:
        """
        Create a new task for the given user, optionally associating it with a parent task.
        """
        # Create a new task, associating it with the parent task if provided
        task = await Task.create(
            title=title,
            description=description,
            user=user,
            parent_task_id=parent_task_id,  # Associate with the parent task if provided
        )
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

    async def get_all_projects(self, user) -> list:
        """
        Fetch all projects for the given user.
        If a parent_id is provided, fetch only tasks that have the given parent_id (subtasks).
        If no parent_id is provided, fetch tasks with no parent (top-level tasks).
        """

        # TODO: That's a magic constant that should be defined.
        # Fetch top-level tasks with no parent
        tasks = await Task.filter(
            user=user, parent_task_id="00000000-0000-0000-0000-000000000000"
        ).all()

        return tasks

    async def get_subtasks(
        self, user, parent_task, page: int = 1, page_size: int = 10
    ) -> List[Task]:
        """
        Fetch all subtasks for a task, with pagination.
        """
        # Calculate the offset based on the page and page size
        offset = (page - 1) * page_size

        # Fetch the subtasks with pagination
        tasks = (
            await Task.filter(user=user, parent_task=parent_task)
            .limit(page_size)
            .offset(offset)
            .all()
        )

        return tasks

    async def split_task(
        self,
        parent_task: Task,
        num_subtasks: int = 2,
    ) -> list:
        """
        Split a task into 'num_subtasks' (default 2) and create Task objects for them,
        but only if there are no existing subtasks. Existing subtasks are sent to the LLM
        to avoid suggesting them again.
        """
        # Validate the number of subtasks (should be at least 1)
        if num_subtasks < 1:
            raise ValueError("The number of subtasks must be at least 1.")

        # Fetch existing subtasks from the database
        existing_subtasks = await Task.filter(parent_task=parent_task).all()

        # If there are existing subtasks, we need to pass them to the LLM
        existing_subtasks_data = [
            {"title": subtask.title, "description": subtask.description}
            for subtask in existing_subtasks
        ]

        # Fetch the title, description, and user from the parent task
        title = parent_task.title
        description = parent_task.description
        user = await User.filter(uuid=parent_task.user_id).first()

        # Create a prompt to send to LLM, passing the existing subtasks
        prompt = (
            f"Split the following task into a maximum of {num_subtasks} additional subtasks, "
            "while considering the existing subtasks. Do not alter or repeat existing subtasks.\n"
            f"Title: {title}\nDescription: {description}\n"
            "Existing subtasks:\n"
        )

        for subtask in existing_subtasks_data:
            prompt += f"- {subtask['title']}: {subtask['description']}\n"

        prompt += (
            "The response should be a JSON array of new subtasks, where each object has the following format:\n"
            "[\n"
            "  {\n"
            '    "title": "Subtask Title",\n'
            '    "description": "Subtask Description"\n'
            "  },\n"
            "  ...\n"
            "]\n"
            "Make sure the titles and descriptions are clear and concise."
        )

        # Ask Mistral to process the prompt and return a structured JSON response
        subtasks_response = await self.llm_service.ask_mistral(prompt)

        # Try to parse the response as JSON
        try:
            subtasks = json.loads(subtasks_response)
        except json.JSONDecodeError:
            raise ValueError("Mistral response is not a valid JSON.")

        # Validate each subtask contains both 'title' and 'description'
        for subtask in subtasks:
            if (
                not isinstance(subtask, dict)
                or "title" not in subtask
                or "description" not in subtask
            ):
                raise ValueError(
                    "Each subtask must contain both 'title' and 'description' keys."
                )

        # Create new tasks based on the generated subtasks
        created_subtasks = []
        for subtask in subtasks:
            # Extract title and description from the subtask
            subtask_title = subtask.get("title", "").strip()
            subtask_description = subtask.get("description", "").strip()

            # Ensure that only non-empty subtasks are created
            if subtask_title and subtask_description:
                new_task = await Task.create(
                    title=subtask_title,
                    description=subtask_description,
                    user=user,  # Use the user from the parent task
                    parent_task=parent_task,  # Link to the parent task
                    status="created",  # Set initial status to 'created'
                )
                created_subtasks.append(new_task)

        return created_subtasks
