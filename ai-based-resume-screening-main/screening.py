import re
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


SKILLS = [
    "python", "java", "c", "c++", "c#", "sql",
    "machine learning", "deep learning",
    "artificial intelligence", "data science",
    "data analysis", "html", "css", "javascript",
    "react", "node.js", "flask", "django",
    "git", "github", "docker", "aws", "azure",
    "tensorflow", "pytorch", "nlp",
    "natural language processing", "mongodb",
    "mysql", "postgresql", "rest api", "api",
    "linux", "kubernetes", "power bi", "tableau"
]


def preprocess_text(text):
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def skill_pattern(skill):
    escaped = re.escape(skill.lower())
    return rf"(?<![a-z0-9+#]){escaped}(?![a-z0-9+#])"


def extract_skills(text):
    clean_text = preprocess_text(text)
    found = []

    for skill in SKILLS:
        if re.search(skill_pattern(skill), clean_text):
            found.append(skill)

    return sorted(set(found))


def calculate_similarity(job_description, resume_text):
    documents = [
        preprocess_text(job_description),
        preprocess_text(resume_text)
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        matrix = vectorizer.fit_transform(documents)
    except ValueError:
        return 0.0

    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return round(score * 100, 2)


def analyze_resume(job_description, resume_text):
    jd_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    matched_skills = [
        skill for skill in jd_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in jd_skills
        if skill not in resume_skills
    ]

    similarity_score = calculate_similarity(
        job_description,
        resume_text
    )

    svm_result, svm_confidence = predict_svm(
    resume_text,
    job_description
    )

    if jd_skills:
        skill_score = round(
            (len(matched_skills) / len(jd_skills)) * 100,
            2
        )
    else:
        skill_score = similarity_score

    # Final ranking score:
    # 60% semantic similarity + 40% required-skill coverage
    final_score = round(
        (0.60 * similarity_score) +
        (0.40 * skill_score),
        2
    )

    explanation_parts = []

    if matched_skills:
        explanation_parts.append(
            "Matched required skills: "
            + ", ".join(matched_skills)
        )

    if missing_skills:
        explanation_parts.append(
            "Missing required skills: "
            + ", ".join(missing_skills)
        )

    if not explanation_parts:
        explanation_parts.append(
            "No predefined skills were detected; ranking is based mainly on text similarity."
        )

    return {
        "score": final_score,
        "similarity_score": similarity_score,
        "skill_score": skill_score,
        "svm_result": svm_result,
        "svm_confidence": round(svm_confidence, 2),
        "jd_skills": jd_skills,
        "resume_skills": resume_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "explanation": " | ".join(explanation_parts),
    }

def train_svm():

    # Load training dataset
    data = pd.read_csv("dataset/svm_training.csv")

    # Combine resume and job description
    text = (
        data["resume_text"].fillna("") +
        " " +
        data["job_description"].fillna("")
    )

    # Labels
    y = data["label"]

    # Split data into training and testing
    X_train_text, X_test_text, y_train, y_test = train_test_split(
        text,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    # TF-IDF conversion
    vectorizer = TfidfVectorizer()

    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)

    # Create SVM model
    model = SVC(
        kernel="linear",
        probability=True
    )

    # Train SVM
    model.fit(X_train, y_train)

    # Save trained model
    joblib.dump(vectorizer, "dataset/svm_vectorizer.pkl")
    joblib.dump(model, "dataset/svm_model.pkl")

    # Test model
    y_pred = model.predict(X_test)

    # Calculate evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print("\n===== SVM MODEL EVALUATION =====")
    print("Accuracy :", round(accuracy * 100, 2), "%")
    print("Precision:", round(precision * 100, 2), "%")
    print("Recall   :", round(recall * 100, 2), "%")
    print("F1 Score :", round(f1 * 100, 2), "%")
    print("================================\n")

    return vectorizer, model 

def predict_svm(resume_text, job_description):

    # Load saved TF-IDF vectorizer
    vectorizer = joblib.load("dataset/svm_vectorizer.pkl")

    # Load saved SVM model
    model = joblib.load("dataset/svm_model.pkl")

    # Combine resume and job description
    text = resume_text + " " + job_description

    # Convert new text into TF-IDF
    X_new = vectorizer.transform([text])

    # Predict
    prediction = model.predict(X_new)[0]

    # Get confidence
    probability = model.predict_proba(X_new)[0]
    confidence = max(probability) * 100

    if prediction == 1:
        result = "Suitable"
    else:
        result = "Not Suitable"

    return result, confidence
if __name__ == "__main__":

    # Train and evaluate SVM
    train_svm()

    # Test prediction
    resume = """
    HTML CSS Bootstrap
    """

    job_description = """
    We need a Python developer with SQL,
    machine learning, Flask and Git skills.
    """

    result, confidence = predict_svm(
        resume,
        job_description
    )

    print("SVM Result:", result)
    print("SVM Confidence:", round(confidence, 2), "%")
    