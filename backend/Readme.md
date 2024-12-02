# Task Management API

This is a RESTful API for managing tasks and user authentication. The API is built with the Sanic web framework, providing asynchronous operations for scalability. This project demonstrates the use of modern Python practices and technologies, including type hinting, clean code principles, and a separation of concerns between controllers, services, and models.

## Features

- **User Authentication**: Users can register and authenticate via email and password.
- **Task Management**: Users can create, retrieve, and delete tasks.
- **JWT Authentication**: The API uses JSON Web Tokens (JWT) for authenticating users.
- **Asynchronous Operations**: Built to handle high-concurrency using Sanic's asynchronous capabilities.

## API Endpoints

### Authentication Endpoints

- **POST /auth/register**: Registers a new user.
- **POST /auth**: Authenticates an existing user and returns a JWT token.

### Task Management Endpoints

- **POST /tasks**: Creates a new task for an authenticated user.
- **DELETE /tasks/<task_id>**: Deletes a task by its ID.
- **GET /tasks**: Fetches all tasks for the authenticated user.

## Technology Stack

- **Sanic**: Asynchronous web framework for Python.
- **Sanic OpenAPI**: For generating API documentation.
- **Tortoise ORM**: For database interactions.
- **JWT**: For user authentication and token generation.

## Installation and Setup

### Prerequisites

- Python 3.12+
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/task-management-api.git
cd task-management-api
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # For Linux/macOS
.venv\Scripts\activate  # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```


### 4. Install Dependencies

Make sure you have a database configured for Tortoise ORM. Update the DATABASES settings in the config.py file with your database connection details.

### 4. Run the Server

```bash
python app.py
```
The API will be accessible at http://localhost:8000.


# API 

```yaml
openapi: 3.0.0
info:
  title: Backend API Showcase
  description: A simple backend for user authentication and task management built with Sanic and Tortoise ORM.
  version: 1.0.0
paths:
  /auth/register:
    post:
      summary: Register a new user
      description: Allows users to register by providing a username, email, and password.
      operationId: registerUser
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: exampleuser
                email:
                  type: string
                  example: exampleuser@example.com
                password:
                  type: string
                  example: securepassword
      responses:
        '200':
          description: User registered successfully.
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Authentication successful
                  user:
                    type: object
                    properties:
                      id:
                        type: string
                        example: uuid-of-user
                      username:
                        type: string
                        example: exampleuser
                      email:
                        type: string
                        example: exampleuser@example.com
                  token:
                    type: string
                    example: jwt-token
        '400':
          description: Missing required fields or invalid data.
        '500':
          description: Internal server error.

  /auth:
    post:
      summary: Authenticate a user
      description: Authenticates a user using their email and password.
      operationId: authenticateUser
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  example: exampleuser@example.com
                password:
                  type: string
                  example: securepassword
      responses:
        '200':
          description: Authentication successful.
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Authentication successful
                  user:
                    type: object
                    properties:
                      id:
                        type: string
                        example: uuid-of-user
                      username:
                        type: string
                        example: exampleuser
                      email:
                        type: string
                        example: exampleuser@example.com
                  token:
                    type: string
                    example: jwt-token
        '400':
          description: Email or password is missing.
        '401':
          description: Invalid credentials.
        '500':
          description: Internal server error.

  /tasks:
    post:
      summary: Create a new task
      description: Allows users to create a new task by providing a title and description.
      operationId: createTask
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                  example: Sample Task
                description:
                  type: string
                  example: This is a sample task description.
      responses:
        '201':
          description: Task created successfully.
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Task created
                  task:
                    type: object
                    properties:
                      uuid:
                        type: string
                        example: uuid-of-task
                      title:
                        type: string
                        example: Sample Task
                      description:
                        type: string
                        example: This is a sample task description.
                      user_id:
                        type: string
                        example: uuid-of-user
                      created_at:
                        type: string
                        format: date-time
                        example: '2024-11-10T12:00:00Z'
        '400':
          description: Missing required fields or invalid data.
        '404':
          description: User not found or invalid user.
        '500':
          description: Internal server error.

    get:
      summary: Get all tasks
      description: Fetch all tasks created by the authenticated user.
      operationId: getAllTasks
      responses:
        '200':
          description: List of tasks.
          content:
            application/json:
              schema:
                type: object
                properties:
                  tasks:
                    type: array
                    items:
                      type: object
                      properties:
                        uuid:
                          type: string
                          example: uuid-of-task
                        title:
                          type: string
                          example: Sample Task
                        description:
                          type: string
                          example: This is a sample task description.
                        user_id:
                          type: string
                          example: uuid-of-user
                        created_at:
                          type: string
                          format: date-time
                          example: '2024-11-10T12:00:00Z'
        '404':
          description: User not found.
        '500':
          description: Internal server error.

  /tasks/{task_id}:
    delete:
      summary: Delete a task
      description: Delete a task by its ID for the authenticated user.
      operationId: deleteTask
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
            example: uuid-of-task
      responses:
        '200':
          description: Task deleted successfully.
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Task deleted
        '400':
          description: Invalid task ID.
        '404':
          description: Task not found.
        '500':
          description: Internal server error.
          
```