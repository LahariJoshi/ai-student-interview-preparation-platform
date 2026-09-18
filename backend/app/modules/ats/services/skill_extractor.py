# backend/app/modules/ats/services/skill_extractor.py

ATS_SKILL_TAXONOMY = {
    "programming_languages": [
        "python",
        "java",
        "c",
        "c++",
        "c#",
        "javascript",
        "typescript",
        "go",
        "golang",
        "rust",
        "kotlin",
        "swift",
        "php",
        "ruby",
        "r",
        "scala",
        "dart",
        "matlab",
    ],

    "web_technologies": [
        "html",
        "css",
        "javascript",
        "typescript",
        "react",
        "react.js",
        "next.js",
        "angular",
        "vue",
        "node.js",
        "nodejs",
        "express",
        "express.js",
        "django",
        "flask",
        "fastapi",
        "spring",
        "spring boot",
        "rest api",
        "restful api",
        "graphql",
    ],

    "ai_ml": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "natural language processing",
        "nlp",
        "computer vision",
        "tensorflow",
        "pytorch",
        "keras",
        "scikit-learn",
        "sklearn",
        "opencv",
        "pandas",
        "numpy",
        "langchain",
        "large language models",
        "llm",
        "generative ai",
    ],

    "databases": [
        "sql",
        "mysql",
        "postgresql",
        "postgres",
        "mongodb",
        "oracle",
        "sqlite",
        "redis",
        "firebase",
        "dynamodb",
        "nosql",
    ],

    "cloud_devops": [
        "aws",
        "amazon web services",
        "azure",
        "microsoft azure",
        "google cloud",
        "gcp",
        "docker",
        "kubernetes",
        "jenkins",
        "github actions",
        "gitlab ci",
        "terraform",
        "ansible",
        "ci/cd",
        "linux",
    ],

    "tools_platforms": [
        "git",
        "github",
        "gitlab",
        "bitbucket",
        "postman",
        "jira",
        "visual studio code",
        "vs code",
        "jupyter",
        "jupyter notebook",
        "android studio",
        "figma",
    ],

    "core_cs": [
        "data structures",
        "algorithms",
        "data structures and algorithms",
        "object oriented programming",
        "oop",
        "operating systems",
        "database management systems",
        "dbms",
        "computer networks",
        "computer architecture",
        "software engineering",
        "system design",
        "distributed systems",
    ],

    "soft_skills": [
        "communication",
        "leadership",
        "teamwork",
        "problem solving",
        "problem-solving",
        "critical thinking",
        "time management",
        "adaptability",
        "collaboration",
        "presentation",
        "interpersonal skills",
    ],
}

import re
from typing import Dict, List


def normalize_text(text: str) -> str:
    """
    Normalize text before skill matching.
    """
    text = text.lower()
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extract known skills from text and organize them
    according to the ATS skill taxonomy.
    """

    normalized_text = normalize_text(text)

    extracted_skills: Dict[str, List[str]] = {
        category: []
        for category in ATS_SKILL_TAXONOMY
    }

    for category, skills in ATS_SKILL_TAXONOMY.items():
        for skill in skills:
            normalized_skill = normalize_text(skill)

            # Escape special regex characters such as +, ., / etc.
            pattern = rf"(?<!\w){re.escape(normalized_skill)}(?!\w)"

            if re.search(pattern, normalized_text):
                extracted_skills[category].append(skill)

    return extracted_skills

if __name__ == "__main__":
    sample_jd = """
    We are looking for a Python Developer with experience in
    FastAPI, REST APIs, PostgreSQL, Docker and Git.
    Knowledge of Machine Learning and AWS is preferred.
    """

    result = extract_skills(sample_jd)

    for category, skills in result.items():
        print(f"{category}: {skills}")