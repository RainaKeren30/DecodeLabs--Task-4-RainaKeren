import re
import math
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# ─── Text Preprocessing ───────────────────────────────────────────────────────

STOPWORDS = {
    "and", "the", "is", "in", "at", "of", "to", "a", "an", "with",
    "for", "on", "by", "from", "as", "or", "be", "are", "was", "were",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "i", "my", "we", "our", "you", "your"
}

def preprocess_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s\+\#\./\-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_skill(skill: str) -> str:
    skill = preprocess_text(skill)
    # Common aliases
    aliases = {
        "js": "javascript", "ts": "typescript", "ml": "machine learning",
        "dl": "deep learning", "ai": "machine learning", "k8s": "kubernetes",
        "tf": "tensorflow", "cv": "computer vision", "nlp": "nlp",
        "aws": "aws", "gcp": "gcp", "ci cd": "ci/cd", "node": "node.js",
        "react.js": "react", "reactjs": "react", "vue.js": "vue",
        "vuejs": "vue", "angular.js": "angular", "postgres": "postgresql",
        "mongo": "mongodb", "py": "python", "c++": "c++", "c#": "c#",
        "dotnet": ".net", ".net core": ".net"
    }
    return aliases.get(skill.strip(), skill.strip())


def parse_skills_input(raw: str) -> list[str]:
    """Parse comma/newline/semicolon-separated skills."""
    delimiters = r"[,\n;|/]"
    parts = re.split(delimiters, raw)
    skills = []
    for part in parts:
        s = normalize_skill(part.strip())
        if s and len(s) > 1 and s not in STOPWORDS:
            skills.append(s)
    return list(dict.fromkeys(skills))  # deduplicate, preserve order


# ─── TF-IDF + Cosine Similarity Engine ────────────────────────────────────────

def compute_similarity(user_skills: list[str], required_skills: list[str]) -> float:
    """Basic cosine similarity between user and required skill sets."""
    user_doc = " ".join(user_skills)
    req_doc = " ".join(required_skills)
    if not user_doc.strip() or not req_doc.strip():
        return 0.0
    try:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        corpus = [user_doc, req_doc]
        matrix = vectorizer.fit_transform(corpus)
        sim = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return float(sim)
    except Exception:
        return 0.0


def weighted_match_score(
    user_skills: list[str],
    role_data: dict,
    experience_multiplier: float = 1.0
) -> dict:
    """
    Comprehensive scoring:
      - Weighted coverage of required skills
      - TF-IDF cosine similarity bonus
      - Adjusted by experience multiplier
    """
    required = role_data["required_skills"]
    weights = role_data.get("weights", {k: 5 for k in required})

    user_set = set(user_skills)

    matched = []
    missing = []
    total_weight = sum(weights.get(s, 5) for s in required)
    earned_weight = 0

    for skill in required:
        w = weights.get(skill, 5)
        if skill in user_set:
            matched.append(skill)
            earned_weight += w
        else:
            # Partial fuzzy match
            for u in user_set:
                if skill in u or u in skill:
                    matched.append(skill)
                    earned_weight += w * 0.8
                    break
            else:
                missing.append(skill)

    raw_score = (earned_weight / total_weight) * 100 if total_weight > 0 else 0
    cosine_bonus = compute_similarity(user_skills, required) * 15
    score = min(raw_score + cosine_bonus, 100) * experience_multiplier
    score = min(score, 99.0)  # cap at 99 — 100 reserved for perfect

    # Strengths = matched skills with high weights
    strengths = sorted(
        [(s, weights.get(s, 5)) for s in matched],
        key=lambda x: x[1],
        reverse=True
    )[:8]

    # Missing sorted by priority weight
    missing_sorted = sorted(
        [(s, weights.get(s, 5)) for s in missing],
        key=lambda x: x[1],
        reverse=True
    )

    return {
        "match_score": round(score, 1),
        "matched_skills": matched,
        "missing_skills": [s for s, _ in missing_sorted],
        "strengths": [s for s, _ in strengths],
        "missing_with_weights": missing_sorted,
        "coverage_ratio": len(matched) / len(required) if required else 0,
    }


def compute_readiness_score(match_score: float, experience_multiplier: float) -> dict:
    """
    Readiness = composite of match score + experience bonus.
    Returns a label + numeric score.
    """
    base = match_score * 0.85 + (experience_multiplier - 0.7) * 20
    readiness = min(round(base, 1), 99.0)

    if readiness >= 80:
        label, color = "Job-Ready", "#2d7a4f"
    elif readiness >= 60:
        label, color = "Nearly Ready", "#4E7AB1"
    elif readiness >= 40:
        label, color = "Progressing", "#CEB5D4"
    else:
        label, color = "Early Stage", "#aaa"

    return {"score": readiness, "label": label, "color": color}


def generate_learning_roadmap(
    missing_skills: list[str],
    role_data: dict,
    top_n: int = 8
) -> list[dict]:
    """Return prioritized learning roadmap for missing skills."""
    paths = role_data.get("learning_paths", {})
    weights = role_data.get("weights", {})
    roadmap = []

    for skill in missing_skills[:top_n]:
        entry = paths.get(skill, {
            "resource": f"Search: {skill.title()} tutorials (Coursera / edX / YouTube)",
            "duration": "2–4 weeks",
            "priority": "Medium"
        })
        roadmap.append({
            "skill": skill.title(),
            "resource": entry["resource"],
            "duration": entry["duration"],
            "priority": entry["priority"],
            "weight": weights.get(skill, 5),
        })

    return roadmap


def estimate_timeline(roadmap: list[dict]) -> str:
    """Rough total timeline based on roadmap durations."""
    total_weeks = 0
    for item in roadmap:
        dur = item.get("duration", "2 weeks")
        nums = re.findall(r"\d+", dur)
        if nums:
            avg = sum(int(n) for n in nums) / len(nums)
            total_weeks += avg
    if total_weeks == 0:
        return "Not available"
    months = total_weeks / 4
    if months < 1:
        return f"~{int(total_weeks)} weeks"
    elif months < 2:
        return "~1 month"
    else:
        return f"~{math.ceil(months)} months"


def radar_chart_data(
    user_skills: list[str],
    required_skills: list[str],
    weights: dict
) -> dict:
    """Prepare data for radar chart — category scores."""
    categories = {
        "Core Tech": [],
        "Tools & Platforms": [],
        "Data & Analytics": [],
        "Cloud & Infra": [],
        "Soft Skills": [],
    }

    cloud_terms = {"aws", "gcp", "azure", "docker", "kubernetes", "terraform", "cloud"}
    data_terms = {"sql", "pandas", "spark", "numpy", "data", "statistics", "analytics", "tableau", "bigquery", "snowflake"}
    tool_terms = {"git", "jira", "figma", "confluence", "airflow", "jenkins", "kafka", "monitoring"}
    soft_terms = {"leadership", "communication", "agile", "scrum", "stakeholder", "roadmapping", "prioritization"}

    user_set = set(user_skills)
    category_scores = {}

    for cat, terms in [
        ("Cloud & Infra", cloud_terms),
        ("Data & Analytics", data_terms),
        ("Tools & Platforms", tool_terms),
        ("Soft Skills", soft_terms),
    ]:
        relevant = [s for s in required_skills if any(t in s for t in terms)]
        if not relevant:
            category_scores[cat] = 0
            continue
        earned = sum(weights.get(s, 5) for s in relevant if s in user_set)
        total = sum(weights.get(s, 5) for s in relevant)
        category_scores[cat] = round((earned / total) * 100, 1) if total > 0 else 0

    core_skills = [s for s in required_skills if s not in
                   cloud_terms | data_terms | tool_terms | soft_terms]
    if core_skills:
        earned = sum(weights.get(s, 5) for s in core_skills if s in user_set)
        total = sum(weights.get(s, 5) for s in core_skills)
        category_scores["Core Tech"] = round((earned / total) * 100, 1) if total > 0 else 0
    else:
        category_scores["Core Tech"] = 0

    return category_scores
