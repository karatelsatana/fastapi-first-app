# FastAPI First App

Backend API built with FastAPI — JWT authentication, PostgreSQL, one-to-many relationships, Docker, and tests.

## Stack

FastAPI, SQLAlchemy, PostgreSQL, JWT (python-jose), bcrypt, Docker / docker-compose, pytest

## Features

- User registration and login, passwords hashed with bcrypt
- JWT-protected endpoints
- One-to-many relationship: users and their notes
- Fully containerized — API and database each run in their own container
- Test coverage for auth and notes endpoints

## Run locally

With Docker (recommended):

\`\`\`bash
docker compose up --build
\`\`\`

API available at `http://localhost:8000/docs`

Without Docker:

\`\`\`bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

## Tests

\`\`\`bash
pytest
\`\`\`

## Live demo

https://fastapi-first-app-9cth.onrender.com/docs

Hosted on a free tier, so the service spins down after inactivity — the first request after a while may take up to a minute.

To try it out, register a new user via `POST /register`, then log in via `POST /login` to get a token.

## Endpoints

| Method | Path | Description | Auth required |
|---|---|---|---|
| POST | /register | Register a new user | No |
| POST | /login | Log in, get JWT token | No |
| GET | /users | List all users | Yes |
| GET | /user/{id} | Get user by id | No |
| PUT | /user/{id} | Update user | No |
| DELETE | /user/{id} | Delete user | No |
| POST | /notes | Create a note | Yes |
| GET | /notes | List your notes | Yes |