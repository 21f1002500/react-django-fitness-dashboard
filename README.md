# Fitness Dashboard (Backend + Frontend)

This repository contains a Django REST backend and a React frontend for a role-based Fitness Dashboard.

## Tech stack

- Backend: Django, Django REST Framework, Simple JWT, SQLite
- Frontend: React, MUI, Axios, React Router

## Features

- JWT authentication
- Role-based access for `SUPER_ADMIN`, `COACH`, and `CLIENT`
- Module-level access control for coaches
- CRUD APIs for users, coaches, clients, subscriptions, diet plans, fitness plans, trackers, analytics, and app configuration
- React dashboard UI with protected routes

## Deliverables

- GitHub repository containing both frontend and backend code
- README with setup and run instructions
- Sample login credentials for Super Admin and Coach
- API documentation via Postman collection (no Swagger)

## Evaluation Criteria

- Implementation of business requirements
- Code quality and folder structure
- Role and module permission handling
- UI/UX and usability
- Documentation quality

## Project structure

- `fitness_dashboard/` Django project and apps
- `frontend/` React app
- `env/` Python virtual environment (already present in this workspace)

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm

## Quick start (run full project)

Open two terminals from the repository root.

### 1. Start backend

```powershell
& .\env\Scripts\Activate.ps1
python .\fitness_dashboard\manage.py migrate
python .\fitness_dashboard\manage.py seed_demo
python .\fitness_dashboard\manage.py runserver
```

Backend runs at `http://localhost:8000`.

### 2. Start frontend

```powershell
cd .\frontend
npm install
npm start
```

Frontend runs at `http://localhost:3000`.

## Backend setup details

If you do not already have the `env` virtual environment, create one and install packages:

```powershell
python -m venv env
& .\env\Scripts\Activate.ps1
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
```

Then run:

```powershell
python .\fitness_dashboard\manage.py migrate
python .\fitness_dashboard\manage.py seed_demo
python .\fitness_dashboard\manage.py runserver
```

## Frontend setup details

```powershell
cd .\frontend
npm install
npm start
```

The frontend uses `http://localhost:8000/api` as the API base URL.

## Demo credentials

Credentials created by `seed_demo` command:

- Super Admin
   - username: `superadmin`
   - password: `SuperAdmin123!`
- Coach
   - username: `coachuser`
   - password: `Coach123!`

## API authentication

- `POST /api/token` obtain access and refresh tokens
- `POST /api/token/refresh` refresh access token

Example request:

```json
{
   "username": "coachuser",
   "password": "Coach123!"
}
```

Use access token in header:

```text
Authorization: Bearer <access_token>
```

## Main API endpoints

- `GET /api/users/` users (Super Admin only)
- `GET /api/users/me/` current logged-in user
- `GET /api/coaches/` coaches (Super Admin only)
- `GET /api/clients/` clients
- `GET /api/modules/` modules (coaches only see enabled modules)
- `GET /api/coach-module-access/` coach module access (Super Admin only)
- `GET /api/app-configurations/` app configuration
- `GET /api/analytics/` analytics
- `GET /api/diet-plans/` diet plans
- `GET /api/fitness-plans/` fitness plans
- `GET /api/subscriptions/` subscriptions
- `GET /api/tracker-records/` tracker records

## Notes on role behavior

- `SUPER_ADMIN` can manage all entities.
- `COACH` can only access data and modules allowed through `CoachModuleAccess`.
- Creating a diet plan requires a valid `client` id in payload.

## Postman

Import `FitnessDashboard.postman_collection.json` in Postman and set the base URL to your backend.

## Common issues and fixes

- 401 unauthorized:
   - Login again and ensure `Authorization: Bearer <token>` is sent.
- 403 forbidden:
   - Logged-in role does not have permission for that endpoint/module.
- 400 while creating diet/fitness plan:
   - Ensure all required fields are sent (for diet, include `client`).
- CORS/network error from frontend:
   - Ensure backend is running on port 8000 and frontend on 3000.

## Useful commands

Run backend tests:

```powershell
python .\fitness_dashboard\manage.py test
```

Run frontend tests:

```powershell
cd .\frontend
npm test
```
