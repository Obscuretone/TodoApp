from models.Task import Task
from models.User import User
from services.llm_service import LLMService
from tortoise.exceptions import DoesNotExist


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

    async def split_task(
        self,
        parent_task: Task,
        num_subtasks: int = 2,
    ) -> list:
        """
        Split a task into 'num_subtasks' (default 2) and create Task objects for them,
        but only if there are no existing subtasks.
        """
        # Validate the number of subtasks (should be at least 1)
        if num_subtasks < 1:
            raise ValueError("The number of subtasks must be at least 1.")

        # Check if the parent task already has subtasks
        existing_subtasks = await Task.filter(parent_task=parent_task).all()
        if existing_subtasks:
            raise ValueError(
                "This task already has subtasks and cannot be split again."
            )

        # Fetch the title, description, and user from the parent task
        title = parent_task.title
        description = parent_task.description

        # TODO: This could probably be prefetched
        user = await User.filter(uuid=parent_task.user_id).first()

        # Call LLMService to split the task into the specified number of subtasks
        subtasks = await self.llm_service.split_task(title, description, num_subtasks)

        # Create and return Task objects for the subtasks
        created_subtasks = []
        for subtask in subtasks:
            # Extract title and description from the subtask dictionary
            subtask_title = subtask.get("title", "").strip()
            subtask_description = subtask.get("description", "").strip()

            # Create a new Task for the subtask
            new_task = await Task.create(
                title=subtask_title,
                description=subtask_description,
                user=user,  # Use the user from the parent task
                parent_task=parent_task,  # Link to the parent task
                status="created",  # Set initial status to 'created'
            )
            created_subtasks.append(new_task)

        return created_subtasks
