import os
from sanic import Sanic, response
from sanic.response import json
from sanic_cors import CORS
from controllers.user_controller import UserController
from controllers.task_controller import TaskController
from tortoise import Tortoise
from services.task_service import TaskService
from services.user_service import UserService
from services.llm_service import LLMService
from connections.mistral import MistralConnection  # Updated import to use Mistral
from middleware.auth import auth_middleware
from config import Config

app = Sanic("AI-TODO-API")


os.environ["SANIC_ENV"] = "development"

# CORS configuration
CORS_URL = Config.CORS_ORIGIN
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
        db_url=Config.DATABASE_URI,
        modules={"models": ["models.Task", "models.User"]},
    )
    await Tortoise.generate_schemas()  # Generate schemas in the database

    # Initialize Mistral Connection for LLM services
    mistral_connection = MistralConnection(
        api_key=Config.MISTRAL_API_KEY
    )  # Using Mistral API Key

    # Initialize LLM service
    llm_service = LLMService(mistral_connection)

    # Initialize service instances
    user_service = UserService()
    task_service = TaskService(llm_service)

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
