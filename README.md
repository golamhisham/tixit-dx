# tixit-dx

Tixit DX is a lightweight, real world issue tracking system inspired by Jira and Linear.
Building it out of curiosity.

## Tech Stack

- FastAPI (backend)
- SQLAlchemy (ORM)
- PostgreSQL (database)
- Docker (containerization)
- JWT + OAuth2 (authentication)
- React (planned frontend, optional for now)

## Purpose

This project is part of a 12-week internship-style simulation to:

- Build software in a real-world setting
- Practice backend engineering skills

## Structure

- `week2/app/models/`: SQLAlchemy models (User, Project, Issue, Comment, etc.)
- `week2/app/schemas/`: Pydantic schemas for request/response validation
- `week2/app/routes/`: FastAPI route files (auth, project, issue, comment)
- `week2/app/crud/` and `week2/app/services/`: (for business logic, refactor in progress)
- `week2/tests/`: Automated tests for all major features
- `week2/main.py`: FastAPI app entry point

## Features Built So Far

- User registration and JWT login
- Project CRUD (create, read, update, delete)
- Issue CRUD (with filtering, search, and permissions)
- Commenting on issues
- Full test coverage for auth, projects, and issues
- Modular, production-ready backend structure

## How to Run the App

1. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] pytest
   ```
2. **Set up your database:**
   - Default: PostgreSQL (see DATABASE_URL in `week2/database.py`)
   - Or use SQLite for local testing (change the URL to `sqlite:///./tixitdx.db`)
3. **Run the app:**
   ```bash
   cd week2
   uvicorn main:app --reload
   ```
4. **Open Swagger UI:**
   - Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Docker

To run the app and Postgres together using Docker Compose:

```bash
cd week2
# Build and start containers
docker-compose up --build
```

## Example .env and .env.example

Copy `.env.example` to `.env` and fill in your secrets:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tixit_db
JWT_SECRET_KEY=your-secret-key
```

## Testing

Run all tests with:

```bash
PYTHONPATH=week2 pytest tests/
```

## Continuous Integration

- All tests run automatically on push/PR to GitHub via GitHub Actions (see `.github/workflows/test.yml`).

---

Feel free to fork, contribute, or use as a learning resource!
