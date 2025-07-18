# tixit-dx

Tixit DX is a lightweight, real-world issue tracking system inspired by Jira and Linear. Built out of curiosity and as part of a 12-week internship-style simulation to practice backend engineering skills.

---

## Tech Stack

- **FastAPI** (backend)
- **SQLAlchemy** (ORM)
- **SQLite** (default local database)
- **PostgreSQL** (optional, for production)
- **Docker** (containerization)
- **JWT + OAuth2** (authentication)
- **Click CLI** (command-line tool)
- **React** (planned frontend)

---

## Project Structure

- `week2/app/models/` — SQLAlchemy models (User, Project, Issue, Comment, etc.)
- `week2/app/schemas/` — Pydantic schemas for request/response validation
- `week2/app/routes/` — FastAPI route files (auth, project, issue, comment)
- `week2/app/core/` — Core utilities (exception handlers, dependencies, JWT)
- `week2/app/crud/` and `week2/app/services/` — Business logic
- `week2/tests/` — Automated tests for all major features
- `cli/main.py` — Command-line interface for interacting with the API
- `week2/main.py` — FastAPI app entry point

---

## Features

- User registration and JWT login
- Project CRUD (create, read, update, delete)
- Issue CRUD (with filtering, search, and permissions)
- Commenting on issues
- Global exception handlers for 404 and 422 errors
- Full test coverage for auth, projects, and issues
- Modular, production-ready backend structure
- CLI tool for managing projects and issues from your terminal

---

## How to Run the App

1. **Install dependencies:**
   ```bash
   pip install -r week2/requirements.txt
   ```
2. **Set up your database:**
   - **Default:** SQLite (no setup needed, uses `tixitdx.db` in `week2/`)
   - **Optional:** PostgreSQL (set `DATABASE_URL` in `.env`)
3. **Configure environment:**
   - Copy `.env.example` to `.env` and set your secrets (see below).
4. **Run the app:**
   ```bash
   cd week2
   uvicorn main:app --reload
   ```
5. **Open Swagger UI:**
   - Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## CLI Tool

Interact with your Tixit DX backend from the command line:

```bash
cd tixit-dx
python cli/main.py --help
```

**Example commands:**

- `python cli/main.py ping` — Check if CLI is working
- `python cli/main.py login` — Log in and store your JWT token
- `python cli/main.py list-projects` — List all your projects
- `python cli/main.py create-project` — Create a new project
- `python cli/main.py create-issue --project-id 1` — Create an issue in project 1
- `python cli/main.py list-issues --project-id 1` — List issues in project 1

---

## Testing

Run all tests with:

```bash
cd tixit-dx
pytest
```

- Tests use a temporary SQLite database (`test.db`) and are fully automated.

---

## Docker

To run the app and Postgres together using Docker Compose:

```bash
cd week2
# Build and start containers
docker-compose up --build
```

---

## Example .env and .env.example

Copy `.env.example` to `.env` and fill in your secrets:

```
DATABASE_URL=sqlite:///./tixitdx.db
JWT_SECRET_KEY=your-secret-key
```

- For Postgres, use: `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tixit_db`

---

## ⚡ Continuous Integration

- All tests run automatically on push/PR to GitHub via GitHub Actions (see `.github/workflows/test.yml`).

---

## Contributing & Notes

- Feel free to fork, contribute, or use as a learning resource!
- The backend is modular and ready for extension (e.g., notifications, more CLI commands, frontend integration).
- If you spot any issues or want to suggest improvements, open an issue or PR.

---
