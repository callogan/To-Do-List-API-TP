# To Do List API

## Description
To-Do List API is a RESTful API for task management built using Django 
and Django REST Framework. This project provides a complete set of CRUD 
operations for working with tasks, including creating, reading, updating, 
and deleting.

## Technologies used

### Core Stack :
  - Python 3.12
  - Django 5.2
  - Django REST Framework
  - PostgreSQL

### Authentication & Security :
  - JWT (JSON Web Tokens) using Simple JWT
  - Custom permissions for different user types
  - CSRF protection

### Additional Tools :
  - Django Filter for data filtering
  - Django CORS Headers for cross-domain requests
  - Dotenv for environment variable management

## Installation

1. Make sure you have Python 3.8 or higher installed
2. Clone the repository or unpack the project archive
3. Install the necessary dependencies:
```bash
pip install -r requirements.txt
```
4. Configure environment variables :
Create a .env file in the project root directory with the 
variables as shown in .env.sample file
5. Apply migrations:
```bash
python manage.py migrate
```
6. Create a superuser (optional): 
```bash
python manage.py createsuperuser
```
7. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Tasks :
- GET /api/tasks/ - Get list of tasks
- POST /api/tasks/ - Create a new task
- GET /api/tasks/{id}/ - Get information about a specific task
- PUT /api/tasks/{id}/ - Update a task
- DELETE /api/tasks/{id}/ - Delete a task (admin only)

### Authentication:
- POST /api/token/ - Get JWT token
- POST /api/token/refresh/ - Refresh JWT token
- POST /api/token/verify/ - Verify JWT token

### Admin interface:
- GET /admin/ - Access Django admin panel
