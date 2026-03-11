Simple Flask Todo App using SQLAlchemy and SQLite database.

For styling [semantic-ui](https://semantic-ui.com/) is used.

### Setup
Create project with virtual environment

```console
$ mkdir myproject
$ cd myproject
$ python3 -m venv venv
```

Activate it
```console
$ . venv/bin/activate
```

or on Windows
```console
venv\Scripts\activate
```

Install Flask
```console
$ pip install Flask
$ pip install Flask-SQLAlchemy
```

Set environment variables in terminal
```console
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
```

or on Windows
```console
$ set FLASK_APP=app.py
$ set FLASK_ENV=development
```

Run the app
```console
$ flask run
```
---

## Assignment: Error Handling and Logging Improvements

This repository was forked from the original project:
https://github.com/patrickloeber/flask-todo

The purpose of this fork was to analyze weaknesses in the project's error handling and logging strategy, and implement improvements as part of a software engineering practical assignment.

### Problems Identified in the Original Code

The original implementation had several issues related to robustness and debugging:

1. **No input validation**
   - The `/add` route accepted empty todo titles.

2. **Missing exception handling**
   - Database operations (`add`, `update`, `delete`) were executed without `try/except` blocks.

3. **No rollback mechanism**
   - If a database operation failed, the transaction could leave the database in an inconsistent state.

4. **Unsafe update/delete operations**
   - The `update()` and `delete()` routes assumed that a todo item always exists.
   - If an invalid ID was used, the application could crash.

5. **No logging**
   - The application did not record important events such as errors, updates, or deletions.

---

### Improvements Implemented

The following improvements were added to make the application more robust and easier to debug:

#### 1. Input Validation
The `/add` route now checks that the todo title is not empty before saving it to the database.

#### 2. Exception Handling
All database operations are wrapped in `try/except` blocks to prevent application crashes.

#### 3. Transaction Rollback
`db.session.rollback()` is now used whenever a database error occurs to maintain database integrity.

#### 4. Safe Record Handling
The application now verifies that a todo item exists before performing update or delete operations.

#### 5. Meaningful Logging
Logging has been added using Python’s `logging` module. The application now records:

- INFO logs for successful operations
- WARNING logs for suspicious user actions
- ERROR logs for database failures

Example log messages:

```
INFO - Added new todo: 'Finish assignment'
WARNING - Update failed: todo with id=9999 not found
ERROR - Database error while deleting todo
```

Logs are written to the file:

```
app.log
```
---

### AI-Generated Logging vs Human Reasoning

AI-generated logging suggestions are often generic, such as:

```
logging.error("An error occurred")
```

Human reasoning improves logging by adding **context and useful debugging information**, for example:

```
logging.error("Database error while deleting todo id=%d: %s", todo_id, e)
```

This approach makes it much easier for developers to diagnose issues in production systems.

---

### Outcome

These improvements increase the **reliability**, **maintainability**, and **debuggability** of the application by introducing proper exception handling and meaningful logging.


---

### Running the Improved Version

After installing the required dependencies, the application can be started with:

```bash
python app.py
```

Then open the browser and navigate to:

```
http://127.0.0.1:5000
```

The application will now run with improved exception handling and logging enabled. Log entries will be written to:

```
app.log
```