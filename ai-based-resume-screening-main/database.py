import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_FILE = DATABASE_DIR / "resumes.db"


def get_connection():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(DATABASE_FILE))
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                job_description TEXT NOT NULL,
                score REAL NOT NULL,
                similarity_score REAL NOT NULL,
                skill_score REAL NOT NULL,
                matched_skills TEXT,
                missing_skills TEXT,
                resume_skills TEXT,
                created_at TEXT NOT NULL
            )
        """)
        connection.commit()


def save_candidate(
    filename,
    job_description,
    score,
    matched_skills,
    missing_skills,
    skill_score,
    similarity_score,
    resume_skills,
):
    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO candidates (
                filename,
                job_description,
                score,
                similarity_score,
                skill_score,
                matched_skills,
                missing_skills,
                resume_skills,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            filename,
            job_description,
            score,
            similarity_score,
            skill_score,
            ", ".join(matched_skills),
            ", ".join(missing_skills),
            ", ".join(resume_skills),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ))
        connection.commit()
        return cursor.lastrowid


def get_all_candidates():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT *
            FROM candidates
            ORDER BY score DESC, id ASC
        """).fetchall()
        return [dict(row) for row in rows]


def get_statistics():
    with get_connection() as connection:
        row = connection.execute("""
            SELECT
                COUNT(*) AS total_candidates,
                ROUND(AVG(score), 2) AS average_score,
                ROUND(MAX(score), 2) AS highest_score
            FROM candidates
        """).fetchone()

        return {
            "total_candidates": row["total_candidates"] or 0,
            "average_score": row["average_score"] or 0,
            "highest_score": row["highest_score"] or 0,
        }


def clear_history():
    with get_connection() as connection:
        connection.execute("DELETE FROM candidates")
        connection.commit()
