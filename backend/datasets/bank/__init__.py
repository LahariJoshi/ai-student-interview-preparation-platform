"""
__init__.py - Aggregates the 220+ curated Coding Questions for the Interview Platform.
"""

from typing import List, Dict, Any

from .arrays import QUESTIONS as ARRAYS_QUESTIONS
from .strings import QUESTIONS as STRINGS_QUESTIONS
from .hash_tables import QUESTIONS as HASH_TABLE_QUESTIONS
from .linked_lists import QUESTIONS as LINKED_LIST_QUESTIONS
from .stacks_queues import QUESTIONS as STACK_QUEUE_QUESTIONS
from .binary_search import QUESTIONS as BINARY_SEARCH_QUESTIONS
from .trees import QUESTIONS as TREE_QUESTIONS
from .heaps import QUESTIONS as HEAP_QUESTIONS
from .graphs import QUESTIONS as GRAPH_QUESTIONS
from .dp import QUESTIONS as DP_QUESTIONS
from .backtracking import QUESTIONS as BACKTRACKING_QUESTIONS
from .greedy_intervals import QUESTIONS as GREEDY_QUESTIONS
from .math_bit_matrix import QUESTIONS as MATH_BIT_MATRIX_QUESTIONS

ALL_QUESTION_MODULES = [
    ARRAYS_QUESTIONS,
    STRINGS_QUESTIONS,
    HASH_TABLE_QUESTIONS,
    LINKED_LIST_QUESTIONS,
    STACK_QUEUE_QUESTIONS,
    BINARY_SEARCH_QUESTIONS,
    TREE_QUESTIONS,
    HEAP_QUESTIONS,
    GRAPH_QUESTIONS,
    DP_QUESTIONS,
    BACKTRACKING_QUESTIONS,
    GREEDY_QUESTIONS,
    MATH_BIT_MATRIX_QUESTIONS,
]


def get_all_questions() -> List[Dict[str, Any]]:
    """Return all questions with deduplicated slugs."""
    seen_slugs = set()
    deduped = []
    for module_questions in ALL_QUESTION_MODULES:
        for q in module_questions:
            if q["slug"] not in seen_slugs:
                seen_slugs.add(q["slug"])
                deduped.append(q)
    return deduped


def get_bank_summary() -> Dict[str, Any]:
    """Calculate summary statistics for the question bank."""
    questions = get_all_questions()
    diff_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    topic_counts: Dict[str, int] = {}
    total_test_cases = 0

    for q in questions:
        diff_counts[q["difficulty"]] = diff_counts.get(q["difficulty"], 0) + 1
        topic_counts[q["topic"]] = topic_counts.get(q["topic"], 0) + 1
        total_test_cases += len(q.get("test_cases", []))

    return {
        "total_questions": len(questions),
        "difficulty_counts": diff_counts,
        "topic_counts": topic_counts,
        "total_test_cases": total_test_cases,
    }
