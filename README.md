# Task Management System

A Django-based task management system with Docker orchestration, Celery background tasks, and PostgreSQL database.

## Features
- JWT Authentication
- Task CRUD operations with assignment
- Background task processing (Celery)
- Responsive web interface
- REST API with pagination, search, and filtering

## Quick Start
```bash
git clone <repo>
cd sherpa
cp .env.sample .env
docker-compose up
```

Access the application at http://localhost:8000

## Default Credentials

You can update your admin credentials from .env

- Username: admin
- Password: adminpass