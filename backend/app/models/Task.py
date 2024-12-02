from tortoise import fields, models
import uuid


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("created", "Created"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    status = fields.CharField(max_length=20, choices=STATUS_CHOICES, default="created")
    created_at = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="tasks"
    )  # Link to the User model
    parent_task = fields.ForeignKeyField(
        "models.Task", related_name="subtasks", null=True, on_delete=fields.SET_NULL
    )  # Self-referencing field to link parent task

    class Meta:
        table = "tasks"
