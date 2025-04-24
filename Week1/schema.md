# Database Schema – TixIt DX

This document outlines the initial data model for the backend.

---

## User Table

| Field        | Type      | Notes                          |
|--------------|-----------|--------------------------------|
| id           | UUID / Int | Primary Key                    |
| username     | String    | Unique                         |
| email        | String    | Unique                         |
| password_hash| String    | Hashed password                |
| role         | Enum      | ['user', 'admin']              |
| created_at   | Timestamp | Default: now()                 |

---

## Project Table

| Field        | Type      | Notes                          |
|--------------|-----------|--------------------------------|
| id           | UUID / Int | Primary Key                    |
| name         | String    |                                |
| description  | Text      | Optional                       |
| created_by   | FK (User) | User who created the project   |
| created_at   | Timestamp |                                |

---

## Issue Table

| Field        | Type      | Notes                          |
|--------------|-----------|--------------------------------|
| id           | UUID / Int | Primary Key                    |
| title        | String    | Required                       |
| description  | Text      | Optional                       |
| status       | Enum      | ['open', 'in_progress', 'closed'] |
| priority     | Enum      | ['low', 'medium', 'high']      |
| project_id   | FK (Project) |                                |
| assigned_to  | FK (User) | Optional                       |
| created_by   | FK (User) | Who reported the issue         |
| created_at   | Timestamp |                                |
| updated_at   | Timestamp |                                |

---

## Comment Table

| Field        | Type      | Notes                          |
|--------------|-----------|--------------------------------|
| id           | UUID / Int | Primary Key                    |
| content      | Text      | Required                       |
| issue_id     | FK (Issue)|                                |
| user_id      | FK (User) | Who made the comment           |
| timestamp    | Timestamp |                                |

