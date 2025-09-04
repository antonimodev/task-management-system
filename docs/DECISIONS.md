# DAY 1: Docker & Foundation

### ✅ Docker Infrastructure
- **Docker Compose Setup**: The foundational step, establishing the core services for future use, starting with PostgreSQL 15 and Redis 7 for testing and development.

- **Health Checks**: Implemented health checks for all services to ensure proper startup order and reliability.

- **Environment Variable Management**: Created [.env.sample](.env.sample) as a template for environment variables, promoting secure and configurable deployments.

- **Volume Persistence**: Added a named volume `postgres_data` to persist database data across container restarts.

### ✅ Django Foundation
- **Django Project Initialization**: Set up a Django 4.2 LTS project with core structure, configured for PostgreSQL integration.

- **Database Configuration**: Switched from default SQLite to PostgreSQL using environment variables for credentials and connection details.

- **Entry Point Script**: Automated database migrations and server startup in [django_backend/scripts/entrypoint.sh](django_backend/scripts/entrypoint.sh).

- **Settings Adjustments**: Modified [django_backend/core/settings.py](django_backend/core/settings.py) to allow all hosts for development testing and integrate environment variables via `os.environ.get()`.

### ✅ Dockerfile & Requirements Optimization
- **Custom Dockerfile**: Created [`django_backend/Dockerfile`](django_backend/Dockerfile) to define the build process for the Django backend. Focused on using a slim Python base image and only installing essential system dependencies (`postgresql-client`, `redis-tools`) to keep the image lightweight.

- **Requirements Management**: Maintained [`django_backend/requirements.txt`](django_backend/requirements.txt) with only the necessary Python packages for the project (Django, psycopg). I'm going to avoid unnecessary bloat during initial development.

- **Iterative Testing**: Continuously rebuilt and tested the Docker image, removing unused dependencies and system packages to minimize image size and speed up build times. Verified that the application ran correctly with the minimal set of dependencies.

### ✅ Django First Endpoints
- **Health Check Endpoint**: Implemented `/health/` route in [`apps/common/views.py`](django_backend/apps/common/views.py) for service monitoring and Docker health checks.

- **Home Page (Landing)**: Added a basic `home.html` template in [`apps/common/templates/home.html`](django_backend/apps/common/templates/home.html) and corresponding view in [`apps/common/views.py`](django_backend/apps/common/views.py). Configured root URL (`/`) in [`config/urls.py`](django_backend/config/urls.py) to render this template as the landing page. At this point, is a preliminary version intended to verify core setup.

## Key Technical Decisions

### Python & Django Version Choice
- **Python 3.12**: Selected for its stability after the bugfix phase and long-term support until 2028, ensuring reliability for a production task management system.

- **Django 4.2 LTS**: Chose over 5.2 for stability and proven compatibility, prioritizing production readiness over minor performance gains. Official documentation confirms support for PostgreSQL 14+ with psycopg 3.1.8+.

### Docker Configuration
- **Base Images**: Used `postgres:15` and `redis:7` for consistency and compatibility.

- **Ports**: Exposed standard ports (5432 for PostgreSQL, 6379 for Redis, 8000 for Django) for easy access during development.

- **Dependencies and Health Checks**: Ensured services start in order (e.g., `web` waits for `db` and `redis` to be healthy) to prevent connection errors.

## Time Allocation Breakdown

### DAY 1 (Docker & Foundation) - ~6-9 hours
- Environment setup and Docker configuration: 3 hours
- Django project initialization and settings: ~2 hours
- Database integration, debugging, and testing: 1 hour
- Documentation: ~1.5 hours

## Technical Challenges Faced

### Learning Curve & Optimization
- **Challenge**: Adapting to new technologies and best practices, especially optimizing Docker and Django integration with PostgreSQL.

- **Solution**: Applied a "less is more" approach—researched and tested which dependencies were truly necessary, iteratively refined the Dockerfile and requirements to achieve a lightweight, maintainable setup.

### PostgreSQL Integration
- **Challenge**: Module import errors with psycopg

- **Solution**: Added proper system dependencies in Dockerfile and correct psycopg version in [requirements.txt](django_backend/requirements.txt)
