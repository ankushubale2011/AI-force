# User Verification App

A simple Python application with a Tkinter-based frontend and PostgreSQL backend that verifies whether a user exists in the database.

## Project Structure
```
app/
  ├── frontend/
  │     └── ui_app.py
  └── backend/
        └── check_user.sql
```

## Prerequisites
- Python 3.x
- PostgreSQL installed and running
- `psycopg2` Python library

## Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/ankushubale2011/AI-force.git
   cd AI-force
   ```
2. Install dependencies:
   ```bash
   pip install psycopg2
   ```

## Database Setup
1. Create a PostgreSQL database (e.g., `test_db`).
2. Create the `users` table:
   ```sql
   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100) UNIQUE NOT NULL
   );
   ```
3. Insert sample data:
   ```sql
   INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie');
   ```
4. Update `db_connection_details` in `app/frontend/ui_app.py` with your PostgreSQL credentials.

## Running the App
```bash
cd app/frontend
python ui_app.py
```

## Troubleshooting
- **Database connection errors**: Ensure PostgreSQL is running and credentials are correct.
- **Module not found**: Verify `psycopg2` is installed.
- **Permission issues**: Ensure your PostgreSQL user has access to the database.

## License
This project is licensed under the MIT License.