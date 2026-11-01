from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("STUDENT_DB", BASE_DIR / "students.db"))
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me")


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connect_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                program TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                capacity INTEGER NOT NULL CHECK (capacity > 0)
            );
            CREATE TABLE IF NOT EXISTS registrations (
                student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
                registered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (student_id, course_id)
            );
        """)
        if db.execute("SELECT COUNT(*) FROM courses").fetchone()[0] == 0:
            db.executemany("INSERT INTO courses(code, title, capacity) VALUES (?, ?, ?)", [
                ("CS101", "Introduction to Programming", 30),
                ("DB202", "Database Fundamentals", 24),
                ("WEB110", "Web Application Development", 20),
            ])


@app.get("/")
def index():
    with connect_db() as db:
        students = db.execute("""
            SELECT s.*, COUNT(r.course_id) AS course_count
            FROM students s LEFT JOIN registrations r ON r.student_id = s.id
            GROUP BY s.id ORDER BY s.name COLLATE NOCASE
        """).fetchall()
        courses = db.execute("""
            SELECT c.*, COUNT(r.student_id) AS enrolled
            FROM courses c LEFT JOIN registrations r ON r.course_id = c.id
            GROUP BY c.id ORDER BY c.code
        """).fetchall()
    return render_template("index.html", students=students, courses=courses)


@app.post("/students")
def add_student():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    program = request.form.get("program", "").strip()
    if not name or not email or "@" not in email:
        flash("Enter a name and a valid email address.", "error")
        return redirect(url_for("index"))
    try:
        with connect_db() as db:
            db.execute("INSERT INTO students(name, email, program) VALUES (?, ?, ?)", (name, email, program))
        flash(f"Added {name}.", "success")
    except sqlite3.IntegrityError:
        flash("That email is already in use.", "error")
    return redirect(url_for("index"))


@app.post("/students/<int:student_id>/delete")
def delete_student(student_id: int):
    with connect_db() as db:
        db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    flash("Student and their registrations removed.", "success")
    return redirect(url_for("index"))


@app.post("/courses")
def add_course():
    code = request.form.get("code", "").strip().upper()
    title = request.form.get("title", "").strip()
    try:
        capacity = int(request.form.get("capacity", ""))
        if capacity < 1 or not code or not title:
            raise ValueError
        with connect_db() as db:
            db.execute("INSERT INTO courses(code, title, capacity) VALUES (?, ?, ?)", (code, title, capacity))
        flash(f"Added course {code}.", "success")
    except ValueError:
        flash("Provide a course code, title, and positive capacity.", "error")
    except sqlite3.IntegrityError:
        flash("That course code already exists.", "error")
    return redirect(url_for("index"))


@app.post("/register")
def register():
    try:
        student_id = int(request.form.get("student_id", ""))
        course_id = int(request.form.get("course_id", ""))
    except ValueError:
        flash("Choose a student and course.", "error")
        return redirect(url_for("index"))
    with connect_db() as db:
        course = db.execute("SELECT c.*, COUNT(r.student_id) AS enrolled FROM courses c LEFT JOIN registrations r ON r.course_id=c.id WHERE c.id=? GROUP BY c.id", (course_id,)).fetchone()
        student = db.execute("SELECT id FROM students WHERE id=?", (student_id,)).fetchone()
        if not course or not student:
            flash("The selected student or course could not be found.", "error")
        elif course["enrolled"] >= course["capacity"]:
            flash("This course is full.", "error")
        else:
            try:
                db.execute("INSERT INTO registrations(student_id, course_id) VALUES (?, ?)", (student_id, course_id))
                flash("Registration complete.", "success")
            except sqlite3.IntegrityError:
                flash("This student is already registered for that course.", "error")
    return redirect(url_for("index"))


@app.get("/students/<int:student_id>")
def student_detail(student_id: int):
    with connect_db() as db:
        student = db.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
        courses = db.execute("""
            SELECT c.code, c.title, r.registered_at FROM registrations r
            JOIN courses c ON c.id=r.course_id WHERE r.student_id=? ORDER BY c.code
        """, (student_id,)).fetchall()
    if not student:
        flash("Student not found.", "error")
        return redirect(url_for("index"))
    return render_template("student.html", student=student, courses=courses)


if __name__ == "__main__":
    init_db()
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
