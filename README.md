# Full Auth Flask Backend - Productivity App

A secure RESTful Flask API designed for task management and productivity tracking. This application features JWT-based authentication, user password hashing, and user-scoped resource management (CRUD) with pagination.

---

## Features

- **Authentication & Authorization:** Secure user registration, login, and session checks using JSON Web Tokens (JWT) and Bcrypt password hashing.
- **User-Scoped Resources:** Users can only view, create, update, and delete their own tasks/resources.
- **Pagination:** The resource index route returns paginated data to handle large lists efficiently.
- **Database Migrations:** Database schema management powered by Flask-Migrate and SQLAlchemy.

---

## Prerequisites & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/WarrenNyaga/flask-auth-productivity.git](https://github.com/WarrenNyaga/flask-auth-productivity.git)
   cd flask-auth-productivity