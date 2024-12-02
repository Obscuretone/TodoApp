# TodoApp API

This repository contains the API for a task management application built with **Sanic**, **Sanic OpenAPI**, and **SQLite** (or other database backends as per the configuration). The API allows users to manage tasks and projects, including creating, editing, deleting tasks, as well as working with subtasks and authenticating users.

## Features

- **User Authentication**: Users can register and log in with their email and password.
- **Task Management**: Create, edit, delete, and fetch tasks and subtasks.
- **Project Management**: Group tasks under projects.
- **Task Splitting**: Split tasks into multiple subtasks using a language model.
- **Pagination**: Fetch tasks and subtasks with pagination support.

## Authentication

Users can authenticate by registering via the `/auth/register` endpoint and logging in via the `/auth/login` endpoint. Upon successful login, the user will receive a **JWT token** to be used for accessing protected routes.

### Task Management

The API supports several actions for task management, including:

- **Create Task**: Users can create new tasks with a title, description, and optional parent task.
- **Edit Task**: Users can edit task details such as title, description, and parent task.
- **Delete Task**: Users can delete tasks.
- **Fetch Task**: Users can retrieve specific tasks and their subtasks.
- **Split Task**: Tasks can be split into subtasks.

### Project Management

The API also supports managing tasks under projects. Projects are essentially tasks that group multiple tasks and can have subtasks. The `/projects` endpoint fetches all projects for the authenticated user.

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests. Common errors include:

- **400 Bad Request**: When required data is missing or invalid.
- **404 Not Found**: When the requested resource (e.g., user or task) is not found.
- **500 Internal Server Error**: For unexpected errors during processing.

## Example Responses

- **Success Response**: After creating a task, the API will return the details of the newly created task.
- **Error Response**: In case of invalid input or missing data, the API will return an error message with the corresponding HTTP status code.

## Setup and Installation

To run this API locally, follow the steps below:

1. Clone the repository:
    ```
    git clone https://github.com/Obscuretone/TodoApp
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Run the app:
    ```
    docker-compose up
    ```

The app will be accessible at `http://localhost:8000` by default.
