"""
Skill Detector — detects categorized skills from raw resume text using
word-boundary-aware regex matching.
"""

import re
from typing import Dict, List

# Skill dictionary: category → list of skill strings to detect
# All matching is case-insensitive and word-boundary-aware.
SKILL_DICTIONARY: Dict[str, List[str]] = {
    "programming_languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#",
        "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R",
        "MATLAB", "Perl", "Haskell", "Lua", "Dart", "Bash", "Shell",
    ],
    "web_technologies": [
        "React", "Next.js", "Vue", "Angular", "HTML", "CSS", "Tailwind",
        "Bootstrap", "Node.js", "Express", "FastAPI", "Django", "Flask",
        "Spring", "Laravel", "REST", "GraphQL", "WebSocket", "jQuery",
        "Sass", "SCSS", "Webpack", "Vite",
    ],
    "ai_ml": [
        "Machine Learning", "Deep Learning", "Neural Network",
        "Natural Language Processing", "NLP", "Computer Vision",
        "TensorFlow", "PyTorch", "Keras", "scikit-learn", "Pandas",
        "NumPy", "Matplotlib", "Seaborn", "OpenCV", "Hugging Face",
        "LangChain", "LLM", "Transformers", "BERT", "GPT",
        "Reinforcement Learning", "Data Science",
    ],
    "databases": [
        "SQL", "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis",
        "Cassandra", "DynamoDB", "Oracle", "SQL Server", "NoSQL",
        "Elasticsearch", "Firebase", "Supabase", "Neo4j",
    ],
    "cloud_devops": [
        "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes",
        "Terraform", "Ansible", "CI/CD", "Jenkins", "GitHub Actions",
        "CircleCI", "Heroku", "Vercel", "Netlify", "Linux", "Nginx",
        "Apache", "Serverless", "Lambda",
    ],
    "tools_platforms": [
        "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Confluence",
        "VS Code", "IntelliJ", "Eclipse", "Postman", "Figma", "Slack",
        "Trello", "Notion", "Excel", "PowerPoint", "Tableau", "Power BI",
    ],
    "core_cs": [
        "Data Structures", "Algorithms", "Object-Oriented Programming",
        "OOP", "Design Patterns", "System Design", "Operating Systems",
        "Computer Networks", "Networking", "Database Management",
        "Compiler Design", "Software Engineering", "Agile", "Scrum",
        "SOLID", "Microservices", "API", "REST API",
    ],
    "soft_skills": [
        "Leadership", "Communication", "Teamwork", "Problem Solving",
        "Critical Thinking", "Time Management", "Adaptability",
        "Collaboration", "Project Management", "Presentation",
        "Analytical", "Creative", "Self-motivated", "Detail-oriented",
    ],
}


def detect_skills(raw_text: str) -> Dict[str, List[str]]:
    """
    Scans raw_text for all skills in SKILL_DICTIONARY using word-boundary regex.

    Returns a dict mapping category → sorted list of detected skill names.
    Only skill names that are actually found in the text are included.
    """
    results: Dict[str, List[str]] = {}

    for category, skills in SKILL_DICTIONARY.items():
        found_skills: List[str] = []
        for skill in skills:
            # Use word-boundary matching; escape special regex chars in skill name
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, raw_text, re.IGNORECASE):
                found_skills.append(skill)
        results[category] = sorted(found_skills)

    return results
