# Task Management API

A simple Task Management backend API with role-based access control (RBAC) using Flask, SQLAlchemy, and SQLite.

## Pre-requisites

- **Windows**: Docker Desktop
- **Linux**: Docker

## Setup & Run

1. **Clone the repository**:

   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```

2. **Run the application using Docker Compose**:
   ```bash
   docker-compose up --build
   ```

## Access URLs

After running, you will have two URLs:

### Backend API

```
http://localhost:5000
```

Check if the backend is running using the health endpoint:

```
http://localhost:5000/health
```

### SQLite Web Interface

```
http://localhost:8080
```

You can use this to inspect and manage the SQLite database.

### Access Summary

**Users can access:**

- `GET /tasks` - View all tasks
- `POST /tasks` - Create new tasks
- `PUT /tasks/{id}` - Update existing tasks

**Admins can access:**

- All user endpoints ✅
- `DELETE /tasks/{id}` - Delete tasks (Admin only)

## API Usage

Use the backend URL to access all endpoints (`/tasks`, `/login`, `/register`, etc.).

All requests require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Available Endpoints

| Method | Endpoint      | Description         | Required Role |
| ------ | ------------- | ------------------- | ------------- |
| POST   | `/register`   | Register new user   | Public        |
| POST   | `/login`      | User authentication | Public        |
| GET    | `/tasks`      | Get all tasks       | User/Admin    |
| POST   | `/tasks`      | Create new task     | User/Admin    |
| PUT    | `/tasks/{id}` | Update task         | User/Admin    |
| DELETE | `/tasks/{id}` | Delete task         | Admin Only    |
| GET    | `/health`     | Health check        | Public        |

## Postman Collection

A Postman collection is included in the repository to test all available endpoints with example requests and JWT authorization setup.

## Environment Variables

| Variable     | Description    | Default        |
| ------------ | -------------- | -------------- |
| `SECRET_KEY` | JWT secret key | Auto-generated |
