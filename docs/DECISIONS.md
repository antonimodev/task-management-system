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



# DAY 2: Auth/User Endpoints & Restructured URLs

### ✅ JWT Authentication Implementation
- **JWT Integration**: Added `djangorestframework-simplejwt` to [requirements.txt](django_backend/requirements.txt) for secure token-based authentication.

- **Security by Default**: Configured `DEFAULT_PERMISSION_CLASSES` in [config/settings.py](django_backend/config/settings.py) to require authentication on all endpoints by default. This was a security choice to follow good practices.

- **Token Blacklist**: Integrated `rest_framework_simplejwt.token_blacklist` in `INSTALLED_APPS` to enable secure logout functionality that invalidates tokens on the server side.

### ✅ Custom User Model & Extensibility
- **AbstractUser**: Implemented custom [`User`](django_backend/apps/users/models.py) model extending Django's `AbstractUser` with additional `nickname` field, following Django documentation recommendations for future scalability.

- **Admin Integration**: Registered custom User model in [apps/users/admin.py](django_backend/apps/users/admin.py) using Django's built-in `UserAdmin` to allow management through admin panel.

- **Database Migration**: Applied `makemigrations users` to properly connect the custom User model with PostgreSQL, ensuring data integrity and proper field constraints.

### ✅ API Architecture & URL Organization
- **Modular URL Structure**: Restructured URLs by creating dedicated `urls.py` files in [apps/users/](django_backend/apps/users/urls.py) and [apps/common/](django_backend/apps/common/urls.py), promoting separation of concerns and maintainability.

- **RESTful Endpoint Design**: Implemented user management endpoints with proper HTTP methods:
  - `POST /api/auth/register/` - User registration (public)
  - `POST /api/auth/login/` - JWT token generation
  - `POST /api/auth/logout/` - Token invalidation
  - `GET /api/auth/users/` - User list (admin only)
  - `GET /api/auth/users/<int:pk>/` - User detail by ID
  - `PUT /api/auth/users/<int:pk>/update/` - User update by ID
  - `GET /api/auth/users/me/` - Current user profile

- **URL Parameter Handling**: Instead of manually writing URL with user ID (not viable), I've used Django standard format, `<int:pk>`. This tells the API to expect a number in that part of the address and use it to find the corresponding user in database.

### ✅ Security & Permission Management
- **Role-Based Access Control**: Implemented differentiated permissions where admin users can access all user data, while regular users can only access their own profiles through `get_queryset()` method overrides.

- **Password Security**: Applied Django's `create_user()` method in [UserSerializer](django_backend/apps/users/serializers.py) to ensure automatic password hashing and `write_only=True` for password fields to prevent exposure in API responses.

- **Authentication Endpoints**: Separated public endpoints (register, login) from protected endpoints using Django REST Framework's permission classes (`AllowAny`, `IsAuthenticated`, `IsAdminUser`).

## Key Technical Decisions

### Authentication Strategy
- **JWT over Sessions**: Selected JWT tokens over Django's default session-based authentication for API scalability and security.

- **Token Blacklisting**: Chose server-side token invalidation over client-side only logout for enhanced security, preventing token reuse after logout.

### User Model Design
- **Early Customization**: Implemented custom User model from the beginning to avoid complex migrations later, as recommended by Django documentation for production applications.

- **Minimal Extensions**: Added only essential fields (`nickname`) while maintaining compatibility with Django's built-in authentication system.

## Time Allocation Breakdown

### DAY 2 (Authentication & User Management) - ~8 hours
- JWT setup and security configuration: 2 hours
- Custom User model implementation and migrations: 1 hour
- API endpoints development and testing: 3 hours
- URL restructuring and organization: 1 hour
- Documentation: ~45 minutes

Each step in any process involves a considerable amount of research.

## Technical Challenges Faced

### URL Organization & Scalability
- **Challenge**: While adding content to the `urls.py` file, I realized that grouping all routes in a single file was not scalable or maintainable. After researching best practices in the Django documentation, I discovered that a modular URL structure is the recommended approach for better organization and scalability.

- **Solution**: I restructured the URLs by creating dedicated `urls.py` files for each app, such as `apps/users/urls.py` and `apps/common/urls.py`. This separation allows each app to manage its own routes independently, making the project easier to maintain and extend. Additionally, I used Django's `include()` function in the main `urls.py` file to integrate modular routes, ensuring a clean and scalable structure.

### Learning Curve & Complexity
- **Challenge**: The second day proved significantly more complex than the first. My limited exposure to Django REST Framework and JWT authentication made it difficult to quickly understand the structure of serializers, views, and endpoints. Adjusting to how Django automates processes behind the scenes has been confusing at times, and the learning curve feels steep, more like driving a race car without much prior experience.

- **Solution**: To address this, I focused on carefully reading official documentation, breaking each step into smaller parts, and testing endpoints directly to confirm understanding. I also ensured migrations were properly created and versioned to keep the project reproducible with docker-compose up. While the process has been frustrating at times, I’m applying everything I know, making steady progress, and gaining confidence.


