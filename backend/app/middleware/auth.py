# middleware/auth.py

import jwt
from sanic.exceptions import Unauthorized
from datetime import datetime
import os
from config import Config


async def auth_middleware(request):
    exempt_path = "/auth"

    # Skip middleware for exempt paths
    if request.path.startswith(exempt_path):
        return

    # Get Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise Unauthorized("Missing Authorization header")

    # Extract the token from the Authorization header
    token_parts = auth_header.split("Bearer ")
    if len(token_parts) != 2:
        raise Unauthorized("Invalid Authorization header format")

    token = token_parts[1]
    try:
        # Decode the JWT token (verify signature)
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])

        # Add user UUID to request context
        request.ctx.user_uuid = payload["uuid"]

    except jwt.ExpiredSignatureError as e:
        raise Unauthorized(f"Token has expired {e}")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid token")
