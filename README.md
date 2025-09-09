# Task Management System

A Django-based task management system with Docker orchestration, Celery background tasks, and PostgreSQL database.

## What I Built

This is a junior-level technical test project. I focused on getting the core functionality working rather than making everything perfect.

### API Features
The API endpoints let you do full CRUD operations on tasks:
- Create, edit, delete, and list tasks
- Search and filter tasks by different criteria
- Pagination for large task lists
- JWT authentication for secure access
- User registration, login, and logout

During development, I tested most of these by manually changing URLs and using the ModHeader Chrome extension to set JWT tokens in the headers.

### Frontend Features
The basic UI allows users to:
- Register new accounts
- Log in and log out
- View all tasks
- Add new tasks

It's not fancy, but it works and connects to the API properly.

### Technical Setup
- **Database**: PostgreSQL with persistent data storage
- **Background Tasks**: Celery for automated task processing
- **Caching**: Redis for session management and Celery broker
- **Docker**: Everything runs with a single `docker-compose up` command

## Quick Start
```bash
git clone <repo>
cd task-management-system
cp .env.sample .env
docker-compose up
```

Access the application at http://localhost:8000

## Default parameters
You can customize names of your database, ports, passwords and credentials inside `.env` file.
Admin credentials by default:
- Username: admin
- Password: adminpass


## Development Notes
This project has been a real challenge and a great learning experience. I’ve pushed my limits and got to know much more about the Django stack and what it takes to build a full stack application from scratch. I constantly had to look up resources and learn on the go, but practice is what makes you improve, and I know the real learning will come from repeating this process again and again.
Main focus was on getting the mandatory requirements, so time managament was crucial in this project.

For API documentation and technical decisions, check out:
- [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) - Basic API reference
- [DECISIONS.md](docs/DECISIONS.md) - My development process and challenges