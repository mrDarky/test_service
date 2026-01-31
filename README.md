# Test Service - Project Testing Web Application

A comprehensive web service for project testing management built with FastAPI, Bootstrap 5, SQLite, and async operations.

## Features

### User Management
- **Registration & Login**: JWT-based authentication
- **Two User Roles**:
  - **Project Creators**: Can create projects and tasks, assign testers
  - **Testers**: Can join projects and work on assigned tasks
- **User Profiles**: View and edit profile information

### Project Management
- Create, view, update, and delete projects
- Project status tracking (Active, Completed, Archived)
- Search and filter projects
- Join projects as a tester

### Task Management
- Create tasks within projects
- Assign tasks to testers
- Task status tracking (Open, In Progress, Completed, Closed)
- Priority levels for tasks
- Due date management

### Messaging System
- Send and receive messages
- Project-related messaging
- Mark messages as read/unread
- Filter unread messages

### Admin Panel
- **Dashboard**: Statistics overview (users, projects, tasks, messages)
- **User Management**: View all users, activate/deactivate accounts, filter by role
- **Project & Task Management**: View and manage all projects and tasks
- **IP Address Logging**: Track user activity with IP addresses
- **System Settings**: Manage application settings

### Additional Features
- Search and filtering system across projects and tasks
- Responsive design with Bootstrap 5
- IP address control and logging
- Async database operations for better performance

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Bootstrap 5, JavaScript
- **Database**: SQLite with async support (aiosqlite)
- **Authentication**: JWT tokens
- **ORM**: SQLAlchemy

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/mrDarky/test_service.git
cd test_service
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY
```

5. **Run the application**:
```bash
python main.py
```

The application will be available at `http://localhost:8000`

## Usage

### First Time Setup

1. Visit `http://localhost:8000`
2. Register as a **Project Creator** or **Tester**
3. Login with your credentials

### Creating Your First Project (as Creator)

1. Navigate to the Projects page
2. Click "Create Project"
3. Fill in project details
4. Create tasks within the project
5. Assign tasks to testers

### Joining a Project (as Tester)

1. Browse available projects
2. Click on a project to view details
3. Click "Join Project"
4. View assigned tasks

### Admin Access

To create an admin user, you'll need to manually set `is_admin=True` in the database for a user account:

```python
# Using Python shell or a script
from app.database import async_session
from app.models import User
from sqlalchemy import select, update

async def make_admin(username):
    async with async_session() as session:
        stmt = update(User).where(User.username == username).values(is_admin=True)
        await session.execute(stmt)
        await session.commit()
```

## API Documentation

Once the application is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
test_service/
├── app/
│   ├── models.py           # Database models
│   ├── schemas.py          # Pydantic schemas
│   ├── database.py         # Database configuration
│   ├── auth.py             # Authentication utilities
│   ├── routers/            # API route handlers
│   │   ├── auth.py
│   │   ├── projects.py
│   │   ├── tasks.py
│   │   ├── messages.py
│   │   ├── users.py
│   │   └── admin.py
│   ├── templates/          # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   ├── projects/
│   │   ├── profile/
│   │   ├── messages/
│   │   └── admin/
│   └── static/             # Static files (CSS, JS)
│       ├── css/
│       └── js/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Projects
- `GET /api/projects/` - List projects
- `POST /api/projects/` - Create project
- `GET /api/projects/{id}` - Get project details
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project
- `POST /api/projects/{id}/join` - Join project

### Tasks
- `GET /api/tasks/` - List tasks
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `POST /api/tasks/{id}/assign` - Assign task to user

### Messages
- `GET /api/messages/` - List messages
- `POST /api/messages/` - Send message
- `GET /api/messages/{id}` - Get message
- `PUT /api/messages/{id}/read` - Mark message as read

### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update current user profile
- `GET /api/users/{id}` - Get user profile

### Admin
- `GET /api/admin/dashboard` - Get dashboard statistics
- `GET /api/admin/users` - List all users
- `PUT /api/admin/users/{id}/activate` - Activate user
- `PUT /api/admin/users/{id}/deactivate` - Deactivate user
- `GET /api/admin/ip-logs` - Get IP address logs
- `GET /api/admin/settings` - Get system settings
- `POST /api/admin/settings` - Create setting
- `PUT /api/admin/settings/{id}` - Update setting

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- IP address logging for security monitoring
- Admin-only endpoints protection
- Role-based access control

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.