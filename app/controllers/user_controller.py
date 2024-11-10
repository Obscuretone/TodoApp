# controllers/user_controller.py

from sanic.response import json
from sanic_openapi import doc
from services.user_service import UserService
from sanic.exceptions import SanicException


class UserController:

    def __init__(self, app, user_service: UserService):
        self.app = app  # Inject the app instance into the controller
        self.user_service = user_service

        # Add the routes to the app instance
        self.app.add_route(self.create_user, "/auth/register", methods=["POST"])
        self.app.add_route(self.authenticate_user, "/auth", methods=["POST"])

    async def create_user(self, request):
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return json({"error": "All fields are required"}, status=400)

        try:
            user = await self.user_service.create_user(username, email, password)
            token = self.user_service.create_access_token(user)

            return json(
                {
                    "message": "Authentication successful",
                    "user": user.to_dict(),
                    "token": token,
                },
                status=200,
            )
        except SanicException as e:
            return json({"error": str(e)}, status=e.status_code)

    async def authenticate_user(self, request):
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return json({"error": "Email and password are required"}, status=400)

        try:
            # Authenticate the user by calling the service method
            user = await self.user_service.authenticate_user(email, password)

            # Create the JWT token for the authenticated user
            token = self.user_service.create_access_token(user)

            # Return only the token
            return json(
                {
                    "message": "Authentication successful",
                    "user": user.to_dict(),
                    "token": token,
                },
                status=200,
            )

        except SanicException as e:
            return json({"error": str(e)}, status=e.status_code)
