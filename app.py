from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)


@app.route("/")
def home():
    try:
        todo_list = Todo.query.all()
        logging.info("Loaded %d todo items", len(todo_list))
        return render_template("base.html", todo_list=todo_list)
    except SQLAlchemyError as e:
        logging.error("Database error while loading todo list: %s", e)
        return "An error occurred while loading tasks.", 500


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()

    if not title:
        logging.warning("User attempted to add an empty todo title")
        return "Todo title cannot be empty.", 400

    try:
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        logging.info("Added new todo: '%s'", title)
        return redirect(url_for("home"))
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error("Database error while adding todo '%s': %s", title, e)
        return "An error occurred while adding the task.", 500


@app.route("/update/<int:todo_id>")
def update(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).first()

        if todo is None:
            logging.warning("Update failed: todo with id=%d not found", todo_id)
            return "Task not found.", 404

        todo.complete = not todo.complete
        db.session.commit()
        logging.info("Updated todo id=%d, complete=%s", todo_id, todo.complete)
        return redirect(url_for("home"))
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error("Database error while updating todo id=%d: %s", todo_id, e)
        return "An error occurred while updating the task.", 500


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).first()

        if todo is None:
            logging.warning("Delete failed: todo with id=%d not found", todo_id)
            return "Task not found.", 404

        db.session.delete(todo)
        db.session.commit()
        logging.info("Deleted todo id=%d", todo_id)
        return redirect(url_for("home"))
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error("Database error while deleting todo id=%d: %s", todo_id, e)
        return "An error occurred while deleting the task.", 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        logging.info("Database initialized successfully")
    app.run(debug=True)