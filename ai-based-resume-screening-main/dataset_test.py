import pandas as pd
from screening import analyze_resume


# ==========================================
# 1. LOAD RESUME DATASET
# ==========================================

resumes = pd.read_csv(
    "dataset/Resume.csv",
    usecols=["ID", "Resume_str", "Category"]
)


# ==========================================
# 2. SELECT INFORMATION-TECHNOLOGY RESUMES
# ==========================================

resumes = resumes[
    resumes["Category"] == "INFORMATION-TECHNOLOGY"
].head(20)


# ==========================================
# 3. LOAD JOB DESCRIPTION DATASET
# ==========================================

jobs = pd.read_csv(
    "dataset/job_descriptions_small.csv"
)


# ==========================================
# 4. SELECT WEB DEVELOPER JOB
# ==========================================

web_developer_jobs = jobs[
    jobs["Job Title"].str.contains(
        "Web Developer",
        case=False,
        na=False
    )
]

if web_developer_jobs.empty:
    print("No Web Developer job found.")
    exit()

job = web_developer_jobs.iloc[0]


job_title = str(job["Job Title"])

job_description = (
    str(job["Job Description"])
    + " "
    + str(job["skills"])
)


# ==========================================
# 5. DISPLAY JOB INFORMATION
# ==========================================

print("\n==========================================")
print("          RESUME SCREENING TEST")
print("==========================================")

print("\nJOB TITLE:")
print(job_title)

print("\nREQUIRED SKILLS:")
print(job["skills"])

print("\nNUMBER OF IT RESUMES TESTED:")
print(len(resumes))

print("\n------------------------------------------")
print("         RANKING IT RESUMES")
print("------------------------------------------\n")


# ==========================================
# 6. ANALYZE EACH RESUME
# ==========================================

results = []


for _, resume in resumes.iterrows():

    resume_text = str(resume["Resume_str"])

    analysis = analyze_resume(
        job_description,
        resume_text
    )

    results.append({

        "ID": resume["ID"],

        "Category": resume["Category"],

        "Score": analysis["score"],

        "Similarity": analysis["similarity_score"],

        "Skill Score": analysis["skill_score"],

        "Matched Skills": ", ".join(
            analysis["matched_skills"]
        ),

        "Missing Skills": ", ".join(
            analysis["missing_skills"]
        )
    })


# ==========================================
# 7. CREATE RESULTS TABLE
# ==========================================

results_df = pd.DataFrame(results)


# ==========================================
# 8. SORT BY FINAL SCORE
# ==========================================

results_df = results_df.sort_values(
    by="Score",
    ascending=False
)


# ==========================================
# 9. DISPLAY FINAL RANKING
# ==========================================

print(
    results_df.to_string(index=False)
)


print("\n==========================================")
print("Ranking completed successfully!")
print("==========================================")
