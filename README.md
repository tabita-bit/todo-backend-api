# Todo Backend API (JWT-Protected)

A backend API built with FastAPI where authenticated users can create and view their own todos. Extends a JWT authentication system with user-scoped CRUD endpoints.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Known Limitations](#known-limitations)
- [Author](#author)

## Overview
This project builds on a JWT authentication backend to add a todo list feature scoped to each logged-in user. Users register and log in to receive a JWT access token, then pass that token in the `Authorization` header to create and fetch their own todos, other users' todos are never visible. Database schema (users and todos tables, with a foreign key relationship) is versioned with Alembic. It was built as part of coursework to practice authenticated APIs, relational models, and protecting routes with tokens.

## Features
- User registration and login (JWT access tokens)
- Passwords hashed with bcrypt
- Create a todo (linked to the authenticated user)
- List todos belonging only to the authenticated user
- Token-based route protection via the `Authorization: Bearer <token>` header
- One-to-many `User` → `Todo` relationship via SQLAlchemy
- Alembic migration defining both tables

## Tech Stack
| Category         | Technology              |
|-------------------|--------------------------|
| Framework         | FastAPI                 |
| ORM               | SQLAlchemy               |
| Database          | SQLite                  |
| Migrations        | Alembic                 |
| Auth              | JWT (python-jose)        |
| Password Hashing  | passlib (bcrypt)         |
| Language          | Python                  |

## Project Structure
```
todo-backend-api/
├── alembic/
│   ├── versions/
│   │   └── c0913e65e55e_create_users_and_todos_table.py  # Creates users & todos tables
│   ├── env.py
│   ├── script.py.mako
│   └── README
├── .gitignore
├── README.md         
├── alembic.ini        # Alembic configuration
├── auth.py            # Password hashing, JWT creation/verification, auth logic
├── database.py        # SQLAlchemy engine & session setup
├── main.py            # FastAPI app — auth & todo routes
├── models.py          # SQLAlchemy User and Todo models (with relationship)
├── requirements.txt   # Python dependencies
└── schemas.py         # Pydantic request/response schemas
```

## API Endpoints
| Method | Endpoint         | Auth Required | Description                              |
|--------|-------------------|:--------------:|--------------------------------------------|
| POST   | `/auth/register`  | No             | Register a new user (email + password)    |
| POST   | `/auth/login`     | No             | Log in and receive a JWT access token     |
| POST   | `/todos`          | Yes            | Create a new todo for the logged-in user  |
| GET    | `/todos`          | Yes            | List todos belonging to the logged-in user |

Protected routes require the header:
```
Authorization: Bearer <your_access_token>
```

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation
```bash
git clone https://github.com/tabita-bit/todo-backend-api.git
cd todo-backend-api
pip install -r requirements.txt
```

### Run the server
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

## Known Limitations
- The JWT secret key is currently hardcoded in `auth.py` for simplicity, since this is a coursework lab. In a production setting, it should be loaded from an environment variable instead.
- There are currently no endpoints to update or delete a todo, or mark it as completed.

## Author
Tabita Mali — [github.com/tabita-bit](https://github.com/tabita-bit)
