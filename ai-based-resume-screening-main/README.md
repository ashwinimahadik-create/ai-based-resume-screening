# AI Resume Screening & Candidate Ranking System

## Features
- Multiple PDF resume upload
- Job description input
- PDF text extraction using PyPDF2
- TF-IDF + cosine similarity
- Required-skill extraction
- Matched and missing skills
- Final ranking score
- SQLite database persistence
- Screening history dashboard
- Candidate statistics
- Basic explainability
- Drag-and-drop / multiple file selection

## Ranking formula

Final Score = 60% TF-IDF Similarity + 40% Required Skill Coverage

This is a project scoring rule, not a claim about how real hiring systems should make employment decisions.

## Run

Activate the virtual environment and run:

    python app.py

Then open:

    http://127.0.0.1:5000

The SQLite database is created automatically at:

    database/resumes.db
