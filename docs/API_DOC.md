# API DOCUMENTATION

This API lets you manage tasks and users.  
JWT Authentication is required for all main routes.

## Authentication

- **Register:**  
  `POST /api/auth/register/`  
  Create a new user.

- **Login:**  
  `POST /api/auth/login/`  
  Returns JWT tokens (`access`, `refresh`).

- **Logout:**  
  `POST /api/auth/logout/`  
  Invalidates the token.

## Users

- **List users:**  
  `GET /api/users/`  
  Admin only.

- **View/edit user:**  
  `GET /api/users/<id>/`  
  `PUT /api/users/<id>/`  
  Only the user or admin.

- **Own profile:**  
  `GET /api/users/me/`  

## Tasks

- **List tasks:**  
  `GET /api/tasks/`  
  Supports search, filtering, and pagination.

- **Create task:**  
  `POST /api/tasks/`  

- **View/edit/delete task:**  
  `GET /api/tasks/<id>/`  
  `PUT /api/tasks/<id>/`  
  `DELETE /api/tasks/<id>/`  

- **Assign task:**  
  `POST /api/tasks/<id>/assign`

---

**Quick notes:**
- All routes use and return JSON.

- To access, add the header:  
  `Authorization: Bearer <access_token>`

- You can test the API with tools like Postman or ModHeader.

- You also can test some of this API functions through basic frontend UI