import re
from io import BytesIO
from collections import OrderedDict

SKILL_CATEGORIES = {
    "Programming": [
        "python", "java", "javascript", "typescript", "c++", "c#", "c",
        "go", "golang", "ruby", "php", " kotlin", "swift", "r"
    ],
    "Web & Backend": [
        "html", "css", "react", "angular", "vue", "node.js", "nodejs",
        "express", "fastapi", "django", "flask", "rest api", "rest apis",
        "graphql", "api development"
    ],
    "Data & Databases": [
        "sql", "postgresql", "mysql", "mongodb", "sqlite", "redis",
        "pandas", "numpy", "excel", "power bi", "tableau", "data analysis",
        "data visualization", "etl"
    ],
    "AI & Machine Learning": [
        "machine learning", "deep learning", "artificial intelligence",
        "natural language processing", "nlp", "llm", "llms", "generative ai",
        "prompt engineering", "rag", "embeddings", "vector database",
        "tensorflow", "pytorch", "scikit-learn", "opencv", "computer vision",
        "classification", "regression"
    ],
    "Cloud & Tools": [
        "aws", "azure", "google cloud", "gcp", "docker", "kubernetes",
        "git", "github", "linux", "ci/cd", "jenkins"
    ],
    "Core CS": [
        "data structures", "algorithms", "object oriented programming",
        "oop", "dbms", "operating systems", "computer networks",
        "problem solving", "software engineering"
    ]
}

ALL_SKILLS = list(OrderedDict.fromkeys(
    skill.strip() for skills in SKILL_CATEGORIES.values() for skill in skills
))

def extract_text(uploaded_file):
    """Extract text from an uploaded PDF, DOCX or TXT Streamlit file object."""
    name = uploaded_file.name.lower()
    data = uploaded_file.getvalue()

    if name.endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if name.endswith(".docx"):
        from docx import Document
        document = Document(BytesIO(data))
        paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
        for table in document.tables:
            for row in table.rows:
                paragraphs.append(" | ".join(cell.text for cell in row.cells))
        return "\n".join(paragraphs)

    if name.endswith(".txt"):
        return data.decode("utf-8", errors="ignore")

    raise ValueError("Unsupported file format. Upload PDF, DOCX or TXT.")

def _contains_term(text, term):
    text = text.lower()
    term = term.lower().strip()
    if not term:
        return False
    # Flexible matching for terms containing punctuation or spaces.
    pattern = r"(?<![a-z0-9])" + re.escape(term).replace(r"\ ", r"\s+") + r"(?![a-z0-9])"
    return re.search(pattern, text) is not None

def extract_skills(text):
    found = []
    for skill in ALL_SKILLS:
        if _contains_term(text, skill):
            found.append(skill.strip())
    return found

def _similarity(resume_text, job_description):
    """TF-IDF cosine similarity; gracefully falls back if dependencies are unavailable."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vectorizer.fit_transform([resume_text, job_description])
        score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
        return round(score * 100)
    except ValueError:
        return 0

def analyze_resume(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched = [skill for skill in job_skills if skill in resume_skills]
    missing = [skill for skill in job_skills if skill not in resume_skills]

    skill_coverage = round((len(matched) / len(job_skills)) * 100) if job_skills else 0
    similarity_score = _similarity(resume_text, job_description)

    # Weighted, transparent heuristic. If no known skills are detected in the JD,
    # use text similarity alone rather than incorrectly reporting zero coverage.
    if job_skills:
        overall = round(0.55 * similarity_score + 0.45 * skill_coverage)
    else:
        overall = similarity_score

    suggestions = []
    if missing:
        suggestions.append(
            "If you genuinely have these skills, make the relevant experience visible: "
            + ", ".join(missing[:10]) + ". Do not add skills you cannot demonstrate."
        )
    if similarity_score < 40:
        suggestions.append("Tailor the resume summary and project descriptions to the role using accurate terminology from the job description.")
    if not re.search(r"\b(project|projects)\b", resume_text, re.I):
        suggestions.append("Add a Projects section with the problem, technologies used and measurable outcome.")
    if not re.search(r"\b(intern|internship|experience|employment)\b", resume_text, re.I):
        suggestions.append("If applicable, add internships, practical experience, volunteering or relevant contributions.")
    if not suggestions:
        suggestions.append("Keep the resume concise and support each listed skill with a project, internship or work example.")

    return {
        "match_score": max(0, min(100, overall)),
        "similarity_score": similarity_score,
        "skill_coverage": skill_coverage,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions,
    }

def build_report(result, filename):
    lines = [
        "AI RESUME ANALYZER - REPORT",
        "=" * 34,
        f"Resume file: {filename}",
        f"Overall match: {result['match_score']}%",
        f"Text similarity: {result['similarity_score']}%",
        f"Required-skill coverage: {result['skill_coverage']}%",
        "",
        "MATCHED SKILLS:",
        ", ".join(result["matched_skills"]) or "None detected",
        "",
        "SKILLS NOT FOUND IN RESUME:",
        ", ".join(result["missing_skills"]) or "None detected",
        "",
        "SUGGESTIONS:",
        *[f"- {item}" for item in result["suggestions"]],
        "",
        "NOTE: This is an indicative text-based tool, not an objective measure of candidate ability.",
        "Review the original resume and assess candidates fairly. Do not use this score alone for hiring."
    ]
    return "\n".join(lines)
