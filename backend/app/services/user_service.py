# services/user_service.py

import jwt
import datetime
import bcrypt
from sanic.exceptions import SanicException
from models.User import User
from config import Config


class UserService:
    async def create_user(self, display_name: str, email: str, password: str) -> User:
        """
        Create a new user with a hashed password.
        """
        # Check if the email is already taken
        existing_user = await User.filter(email=email).first()
        if existing_user:
            raise SanicException("User already exists", status_code=400)

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Create the user and save to database
        user = await User.create(
            display_name=display_name, email=email, password=hashed_password
        )
        return user

    async def authenticate_user(self, email: str, password: str) -> User:
        """
        Authenticate a user by verifying email and password.
        """
        # Find the user by email
        user = await User.filter(email=email).first()
        if not user:
            raise SanicException("Invalid credentials", status_code=401)

        # Verify password
        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            raise SanicException("Invalid credentials", status_code=401)

        return user

    def create_access_token(self, user: User) -> str:
        """
        Generate a JWT access token for an authenticated user.
        """
        # Token expiration time (1 hour from now)
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=2)

        # Payload for the JWT token
        payload = {
            "sub": user.email,  # User's email as subject
            "uuid": str(user.uuid),  # User's unique identifier
            "exp": expiration,  # Expiration time
        }

        # Create the JWT token
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

        return token
