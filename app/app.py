from sanic import Sanic, response
from sanic.response import json
from sanic_cors import CORS
import os
from controllers.user_controller import UserController
from controllers.task_controller import TaskController
from tortoise import Tortoise
from services.task_service import TaskService
from services.user_service import UserService
from middleware.auth import auth_middleware

from config import Config

app = Sanic("cbc-todo-api")

# CORS configuration
CORS_URL = os.environ.get("CORS_ORIGIN", "http://localhost:3000")
CORS(app, origins=[CORS_URL], supports_credentials=True)
app.register_middleware(auth_middleware, "request")


@app.route("/", methods=["GET"])
async def hello_world(request):
    return response.json({"message": "TODO API", "version": "1.0.0"})


# Initialize services on app start and close on shutdown
@app.listener("before_server_start")
async def setup_services(app, loop):
    # Initialize the database connection using Tortoise
    await Tortoise.init(
        db_url=os.environ.get(
            "DATABASE_URL",
            "mysql://todo_user:todo_pass@127.0.0.1:3307/cbc_todo",
        ),
        modules={"models": ["models.Task", "models.User"]},
    )
    await Tortoise.generate_schemas()  # Generate schemas in the database

    # Initialize service instances
    user_service = UserService()
    task_service = TaskService()

    # Initialize controllers and pass the app and services
    user_controller = UserController(app, user_service)
    task_controller = TaskController(app, task_service)


@app.listener("after_server_stop")
async def cleanup_services(app, loop):
    # Close database connections after the server stops
    await Tortoise.close_connections()


# Run the app
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=os.environ.get("SANIC_DEBUG", "False") == "True",
    )
