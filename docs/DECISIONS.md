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



# DAY 3: Task Management API & Assignment Logic

### ✅ Entrypoint Script & Type Hints
- **Entrypoint.sh Update**: Updated `entrypoint.sh` and `.env` to automatically create a Django superuser inside the Docker container, making environment setup and Django admin access much easier.

- **Type Hints Addition**: Added type hints throughout the codebase to improve readability and maintainability for all contributors (good practices).


### ✅ Task API Implementation
- **Task & Tag Models**: Implemented core `Task` and `Tag` models in `apps/tasks/models.py`, following requirements.

- **Task List API**: Added `TaskListView` using DRF's `ListCreateAPIView` to support listing and creation of tasks.

- **Pagination, Searching, Filtering**: Integrated DRF pagination, search, and django-filter.

- **Default Tags**: Automated creation of default tags via data migration for immediate usability and easier testing.

### ✅ Task Detail & Assignment
- **Task Detail Endpoints**: Added `TaskDetailView` with `RetrieveUpdateDestroyAPIView` to support `GET`, `PUT`, `PATCH`, and `DELETE` for `/api/tasks/{id}/`.

- **TaskAssignment Model**: Introduced `TaskAssignment` as a through model for `assigned_to` in `Task`, enabling tracking of who assigned a task, to whom, and when, it was required by subject.

- **Assignment Endpoint (WIP)**: Started development of `/api/tasks/{id}/assign/` endpoint to manage task assignments via API, endpoints still in development.

## Key Technical Decisions

### Automate superuser creation
- **Script updated**: Entrypoint.sh and .env have been updated to automatically create a Django superuser inside the Docker container. This makes it much easier to set up the environment and access the Django admin panel.

### API Design
- **RESTful Endpoints**: Followed REST conventions for task detail and assignment endpoints.

- **User permissions related to tasks**: Implemented custom permissions to ensure that only authorized users can assign, create, or view tasks.

### Data Integrity & Usability
- **Default Data**: Automated creation of default tags for immediate usability, especially for testing purposes.

## Time Allocation Breakdown

### DAY 3 (Task API & Assignment) - ~7 hours
- Update entrypoint.sh script: ~30 minutes
- Task model and API endpoints: 2 hours
- Assignment logic and through model: 1.5 hours
- Filtering, searching, and pagination: 1 hour
- Migrations and default data: ~30 minutes
- Documentation and review: ~30 minutes
- Debugging and learning: 1.5 hours

## Technical Challenges Faced

### ForeignKey understanding
- **Challenge**: ForeignKey seemed a bit tricky because it is different from a primary key and I had never worked with it before.

- **Solution**: I spent time researching to understand how ForeignKey works in Django. In short, a ForeignKey creates a relationship between two models by storing the primary key of one model in another. This allows, for example, a user to be assigned to different tasks.

### DRF Learning Curve
- **Challenge**: Even on my third day working on this project, I still find it challenging, less than before as I continue to internalize the real structure of Django project based on the MVT or MVC architecture. I'm working to fully understand how models/views/templates and serializers interact, as well as how to use DRF features like generics to quickly build and test API endpoints.

- **Solution**: I'm continuing to research and watch tutorial videos to gradually deepen my understanding. Practice makes perfect.

### Tags Initialization
- **Challenge**: When I tried to create tasks, I encountered errors because tags could not be assigned if they did not already exist. I considered two options: either create some default tags for testing and leave further improvements for later, or implement functionality to allow users to create their own tags on the fly. The second option would have required significantly more time.

- **Solution**: To prioritize my time, I chose the first option and used a data migration to automatically create default tags for testing and initial use.



# DAY 4: Backend Optimization, Task Assignment Endpoint & Frontend Integration

### ✅ Backend Optimization & New Endpoints
- **Migrations Reset**: Reset migrations for `django_backend/apps/tasks/` to resolve migration errors and ensure a clean database state.

- **Task Assignment Endpoint**: Added `TaskAssignView` to `apps/tasks/views.py` with a custom `POST` method, enabling task assignment logic and preparing the backend for future frontend integration.

- **API Route Added**: Registered the new `POST /api/tasks/{id}/assign/` endpoint in `apps/tasks/urls.py` for assigning tasks to users.

- **Efficient Querying**: Applied `select_related` and `prefetch_related` in `apps/tasks/models.py` to optimize database queries, especially for models with multiple relationships.

- **Soft Delete Implementation**: Introduced an abstract `SoftDeleteModel` in `apps/common/models.py`. This allows multiple models (such as tasks and users) to inherit soft delete functionality, reducing code duplication and avoiding unnecessary database tables.

### ✅ Migrations & Data Integrity
- **Migrations Applied**: Ran and applied migrations from previous changes to ensure all models and database schema updates are reflected and consistent.

### ✅ Frontend Integration & UI Improvements
- **Static Files Organization**: Created `django_backend/apps/common/static` with organized `css` and `img` folders for better static file management.

- **Basic UI Implementation**: Developed a simple UI for the main page (`home.html`) to provide user-friendly navigation and a visual entry point to the application.

- **Registration Template**: Added a `register.html` template, laying the groundwork for a new view that will handle user registration through HTML forms and enable seamless HTML-to-HTML redirection.

- **Frontend-API Connection Research**: Investigated best practices for connecting Django templates with API endpoints, concluding that server-side rendered forms should submit data directly to the appropriate API endpoints for maintainability and clarity.

## Key Technical Decisions

- **Efficient Relationship Handling**: Used `select_related` and `prefetch_related` only where necessary (in the Task model) to optimize performance.

- **Reusable Soft Delete**: Implemented a reusable abstract model for soft deletion, promoting DRY principles and maintainability.

- **Frontend-Backend Separation**: Decided to keep frontend templates and API endpoints logically separated, with forms posting directly to API routes.

## Time Allocation Breakdown

### DAY 4 (Backend Optimization & Frontend Integration) - ~6-7 hours
- Migrations reset and troubleshooting: ~1 hour
- Task assignment endpoint and view logic: 2 hours
- Query optimization and soft delete implementation: 1 hour
- Static files organization and UI templates: 1 hour
- Research and connecting frontend to API: 45 minutes
- Documentation and review: ~45 minutes

## Technical Challenges Faced

### Model Reference Confusion
**Challenge**: I struggled to understand how to reference parameters between models, especially when using strings for `through` models or referencing classes declared later in the file.

**Solution**: I researched Django's model reference documentation and experimented with both direct and string-based references, which clarified when and why each approach is used.

### Lack of a Basic UI for Testing
**Challenge**: Testing endpoints was cumbersome without a basic UI, requiring manual URL navigation and making it hard to maintain session state for authenticated requests. 

**Solution**: I implemented simple HTML templates and used the ModHeader browser extension to set JWT tokens in HTTP headers, streamlining manual testing and session management.

### Framework Conventions & Learning Curve
**Challenge**: Not using Django REST Framework daily meant many conventions were unfamiliar, slowing down development as I had to frequently research best practices.  

**Solution**: I dedicated extra time to read community resources, ensuring I followed DRF conventions.



# DAY 5: Template & Static Refactor, Improved UI, and API Connection

### ✅ Template and Static Structure Refactor
- **URL Tag Usage**: Updated all template links in `home.html` and related templates to use Django's `{% url %}` tag for referencing internal routes, avoiding hardcoded URLs.

- **.gitignore Update**: Added `.vscode` to `.gitignore` to prevent workspace-specific settings from being committed. This included settings for improved Django HTML auto-suggestions in VS Code.

- **urls.py Improvements**: Refactored `django_backend/config/urls.py` for clarity and maintainability. Added `app_name` to `django_backend/apps/auth_jwt/urls.py` to enable namespaced URL referencing.

- **Base Template Creation**: Introduced a `base.html` template as the main layout to inheritance another templates.

- **Descriptive CSS Naming**: Renamed CSS files to be more descriptive and unique (e.g., `home.css` for `home.html`), resolving issues where Django's static file resolution would serve the wrong stylesheet if multiple files shared the same name.

### ✅ Basic Frontend UI
- **UI Completion**: Developed a basic frontend UI for the main pages, focusing on visual experience and usability.

### ✅ API Connection & Code Updates
- **View Updates**: Refactored views in the `auth_jwt` app to connect HTML forms with the API endpoints, enabling user registration and login via the frontend.

- **Template Syntax Improvements**: Updated HTML templates to use best practices for anchor tags (`<a>`) and form submissions.

- **Authentication State Handling**: Implemented logic to display a custom home page depending on whether the user is authenticated, providing a more dynamic user experience.

- **Requirements Update**: Added the `requests` library to `requirements.txt` to facilitate API communication from HTML forms.

## Key Technical Decisions

### Static File Handling & CSS Naming
- **Problem**: Encountered issues where extending `home.html` and adding `register.html` caused CSS conflicts—`home.css` would override styles in other templates, even with different routes.

- **Solution**: After extensive research and troubleshooting, resolved the issue by renaming CSS files to unique, descriptive names (e.g., `home.css`, `register.css`). Learned that Django's static file resolution can serve the wrong file if multiple static files share the same name, regardless of their directory.

### Template Inheritance & UI Structure
- **Block System**: Adopted the use of a `base.html` template with content blocks, enabling code reuse and easier template inheritance.

- **Font Integration**: Embedded the 'Roboto' font from Google Fonts for a clean and readable frontend appearance.

### Frontend-API Integration
- **API Connection**: Started connecting frontend forms to backend API endpoints using the `requests` library, laying the groundwork for JWT authentication.

## Time Allocation Breakdown

### DAY 5 (Template Refactor & API Connection) - ~9 hours
- Template and static structure refactor: 2 hours
- .gitignore and workspace settings: 15 minutes
- Base template and CSS renaming: 1 hour
- Frontend UI development: 3 hours
- API connection and view updates: 2 hours
- Documentation and review: ~45 minutes

## Technical Challenges Faced

### Static File Resolution
- **Challenge**: Spent significant time troubleshooting why CSS from one template would override another, even with different routes and directories.

- **Solution**: Discovered that Django's static file system can serve the wrong file if multiple static files share the same name. Renaming CSS files to unique names resolved the issue.

### Template Inheritance Learning Curve
- **Challenge**: Initially struggled with how Django's template inheritance and block system worked, especially when extending templates and managing shared content.

- **Solution**: Through research and experimentation, learned to use a `base.html` with content blocks, making the template structure more intuitive and maintainable.

### Frontend-Backend Integration
- **Challenge**: Connecting HTML forms to API endpoints and handling authentication state in the UI required updating both views and templates.

- **Solution**: Updated views to handle API requests and adjusted template logic to display different content based on authentication status.

## Personal Reflection

As a final thought for the day, I spent considerable time understanding how Django links static files through its block system. Once understood, it became intuitive, even though I haven’t worked deeply with Django before. I’m thankful for the challenge, as these kinds of obstacles always push me to improve and learn more.



# DAY 6: Task Frontend Integration & Celery Implementation

### ✅ Task Management Frontend
- **Task Templates**: Created [`django_backend/apps/tasks/templates/add_task.html`](django_backend/apps/tasks/templates/add_task.html) and [`django_backend/apps/tasks/templates/view_task.html`](django_backend/apps/tasks/templates/view_task.html) to provide a more complete frontend interface for task management.

- **URL Separation**: Split URLs in [`django_backend/apps/tasks/`](django_backend/apps/tasks/) into [`urls_api.py`](django_backend/apps/tasks/urls_api.py) and [`urls_html.py`](django_backend/apps/tasks/urls_html.py) for better organization and separation of concerns between API endpoints and HTML views.

- **Settings Update**: Updated [`django_backend/config/settings.py`](django_backend/config/settings.py) to include new template and static file paths for the tasks app, ensuring Django can properly locate and serve the new frontend components.

### ✅ Frontend-API Integration
- **Form-API Connection**: Created two main functions in [`django_backend/apps/tasks/views.py`](django_backend/apps/tasks/views.py) to connect HTML forms with API endpoints:
  - `add_task_view()` - Handles task creation through frontend forms
  - `view_tasks_view()` - Displays tasks fetched from API endpoints

- **Automatic Field Population**: Implemented automatic `created_by` field population using `request.user.id` from the active session, eliminating the need for users to manually specify task creators.

- **Code Refactoring**: Refactored view functions multiple times to improve readability and maintainability, creating helper functions like `get_task_form_data()`.

### ✅ Celery Background Tasks Implementation
- **Celery Configuration**: Created [`django_backend/config/celery.py`](django_backend/config/celery.py) with proper Django integration and autodiscovery settings.

- **Celery Dependencies**: Added `celery>=5.0` and `django-celery-beat>=2.5.0` to [`requirements.txt`](django_backend/requirements.txt) for background task processing and database scheduling.

- **Docker Services**: Updated [`docker-compose.yml`](docker-compose.yml) to include `celery` and `celery-beat` services with proper dependencies and Redis integration.

- **Celery Integration**: Updated [`django_backend/config/__init__.py`](django_backend/config/__init__.py) to automatically start Celery workers when Django starts.

- **Scheduled Tasks**: Implemented two background tasks in [`django_backend/apps/tasks/tasks.py`](django_backend/apps/tasks/tasks.py):
  - `check_overdue_tasks()` - Automatically marks tasks as overdue when they pass their due date (tested).
  - `cleanup_archived_tasks()` - Removes old archived tasks to maintain database performance (not tested).

- **Beat Schedule**: Configured [`CELERY_BEAT_SCHEDULE`](django_backend/config/settings.py) in settings to run overdue checks every minute and cleanup daily at 8:30 AM.

### ✅ Code Quality & Compatibility Improvements
- **Code Standardization**: Updated all indentation from 4 spaces to 1 tab (4 spaces) throughout the codebase for consistency.

- **Docker Compatibility**: Adjusted [`docker-compose.yml`](docker-compose.yml) commands to use `sh` for better cross-platform compatibility, especially for Windows development environments.

## Key Technical Decisions

### Celery Architecture
- **Task Design**: Implemented Celery tasks that are both useful for the application (overdue checking) and demonstrate background processing capabilities as required by test.

- **Database Scheduler**: I used `django-celery-beat` for scheduling background tasks because it’s the most common way to manage periodic jobs in Django projects. Honestly, I followed the official docs and community/AI examples to understand this part, remembered me crontab from Linux.

## Time Allocation Breakdown

### DAY 6 (Frontend Integration & Celery) - ~8-9 hours
- Task templates and frontend interface: 1.5 hours
- URL organization and settings updates: 1 hour  
- Form-API connection and view functions: 2 hours
- Celery configuration and Docker integration: 2 hours
- Code refactoring and standardization: 45 minutes
- Testing and debugging: 1 hour
- Documentation updates: 2 hour

## Technical Challenges Faced

### Form Field Mapping
- **Challenge**: Struggled to properly map form data to model fields, especially handling required fields like tags and `created_by` that shouldn't be manually entered by users.

- **Solution**: Researched Django form handling best practices and implemented automatic field population for `created_by` using session data. Used existing default tags from previous migrations to handle tag requirements.

### Celery Learning Curve  
- **Challenge**: First time implementing Celery with Django, requiring research into proper configuration, Docker integration, and task scheduling.

- **Solution**: Followed Django-Celery documentation step by step, ensuring proper Redis broker configuration and testing with simple tasks before implementing the final scheduled tasks, AI was a good support in this part.

### Docker Service Dependencies
- **Challenge**: Ensuring proper startup order for Celery services that depend on both database and Redis being healthy.

- **Solution**: Used Docker Compose health checks and service dependencies to ensure services start in the correct order, preventing connection errors during container startup.

### Code Organization & Maintenance
- **Challenge**: As the project grew, maintaining clean code organization became more important, especially with multiple view functions handling similar logic.

- **Solution**: Implemented code refactoring passes to extract common functionality into helper functions.

## Personal Reflection
Day 6 marked a significant milestone in bringing together all the pieces of the application. The integration of frontend forms with API endpoints felt like a major achievement, especially after struggling with Django's conventions in earlier days.

The automatic overdue task detection working correctly gave me confidence that the application was becoming truly functional rather than just a collection of endpoints.


# Trade-offs

For the trade-offs, I decided to skip some of the more advanced API endpoints at the end, like full task operations (assign, comments, history), so I could focus on building a basic frontend interface with a bit of styling to make it look more appealing. On the frontend side, I also left out features like deleting, editing, or assigning tasks through the UI, because I needed to spend time getting the Celery tasks working.

Overall, I tried to follow the recommended schedule and prioritized the things that felt more familiar to me, even though most of this was new! My main goal was to organize my time as best as I could. I chose to work on the frontend before Celery and other backend features because I wanted to test things in a more user-friendly way, instead of just using ModHeader for authentication tokens or jumping between API endpoints.

# Things I Would Add or Improve With More Time

If I had more time, I would focus on finishing the frontend interface to make it fully user-friendly and cover all the main features (like editing, deleting, and assigning tasks directly from the UI) including profile editing that actually is implemented in API but not in frontend interface. Once the frontend was more complete, I’d go back to the API and finish the remaining endpoints, making sure that for every new feature, there’s a clear flow from API to frontend.

I also think it would be great to let users create groups or teams, where someone can be an admin for their group and assign tasks to other members. This would allow for more real-world scenarios and flexible task management.

# Justification for Using Django Templates for the Frontend

I picked Django templates for the frontend because they’re simple to set up and work smoothly with Django views and forms. Even though I don’t have much frontend experience, I liked how you can reuse code blocks and styles, making everything feel modular almost like backend code. There’s probably a lot more you can do with them, and I’d like to explore that in the future, but for now, this approach let me focus on building and connecting features without getting stuck on extra frameworks or setup.