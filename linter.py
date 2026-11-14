"""
Prompt Linter for Fine Tuner Application.

Grades user prompts on an A-F scale based on length and structural
composition. Designed to be deterministic and pure (no I/O, no
external dependencies) so it can be unit tested reliably.
"""

from typing import Dict, Any, List

# --- GRADING THRESHOLDS ---
# Score boundaries (0-100) that map to letter grades.
GRADE_A_MIN: int = 90
GRADE_B_MIN: int = 75
GRADE_C_MIN: int = 60
GRADE_D_MIN: int = 40

# --- LENGTH THRESHOLDS (characters) ---
MIN_PROMPT_LENGTH: int = 1          # anything > 0 is a real prompt
SHORT_PROMPT_LENGTH: int = 20       # below this is "overly short"
MODEST_PROMPT_LENGTH: int = 60
GOOD_PROMPT_LENGTH: int = 120
GREAT_PROMPT_LENGTH: int = 300

# --- STRUCTURE SIGNALS ---
# Keywords that indicate a well-structured, intentional prompt.
STRUCTURE_KEYWORDS: List[str] = [
    "step", "example", "first", "second", "third", "fourth",
    "context", "background", "objective", "goal", "purpose",
    "instruction", "format", "output", "role", "audience",
    "tone", "constraint", "requirement",
]


def _length_score(prompt: str) -> int:
    """
    Score prompt length on a 0-60 scale.

    Empty prompts earn 0. Very short prompts earn very little.
    Longer, fleshed-out prompts earn progressively more.
    """
    length = len(prompt)

    if length == 0:
        return 0
    if length < SHORT_PROMPT_LENGTH:
        return 10
    if length < MODEST_PROMPT_LENGTH:
        return 25
    if length < GOOD_PROMPT_LENGTH:
        return 40
    if length < GREAT_PROMPT_LENGTH:
        return 50
    return 60


def _structure_score(prompt: str) -> int:
    """
    Score prompt structure on a 0-40 scale.

    Rewards: an explicit question, domain vocabulary, multi-line
    formatting, and enumerated/list formatting.
    """
    lower = prompt.lower()
    score: int = 0

    if "?" in prompt:
        score += 10
    if any(keyword in lower for keyword in STRUCTURE_KEYWORDS):
        score += 10
    if "\n" in prompt:
        score += 10
    if any(char in prompt for char in ":-123456789"):
        score += 10

    return min(score, 40)


def _score_to_grade(score: int) -> str:
    """Map a numeric score to a letter grade (A-F)."""
    if score >= GRADE_A_MIN:
        return "A"
    if score >= GRADE_B_MIN:
        return "B"
    if score >= GRADE_C_MIN:
        return "C"
    if score >= GRADE_D_MIN:
        return "D"
    return "F"


def _feedback(grade: str, length: int) -> str:
    """Return a human-readable hint for the given grade."""
    if grade == "A":
        return "Excellent prompt. Clear, detailed, and well-structured."
    if grade == "B":
        return "Good prompt. Add more detail or structure to reach an A."
    if grade == "C":
        return "Fair prompt. Expand the context and clarify the goal."
    if grade == "D":
        return "Weak prompt. Add significant detail and structure to improve."
    return (
        "Failed. The prompt is empty or too short to be useful. "
        "Provide a clear question or instruction with enough context."
    )


def grade_prompt(prompt: str) -> Dict[str, Any]:
    """
    Grade a prompt on an A-F scale.

    Args:
        prompt: The prompt string to evaluate.

    Returns:
        A dictionary with keys:
            - 'grade': Letter grade (A-F)
            - 'score': Numeric score (0-100)
            - 'length': Character count of the prompt
            - 'feedback': Human-readable improvement hint

    Raises:
        TypeError: If prompt is not a string.
    """
    if not isinstance(prompt, str):
        raise TypeError("prompt must be a string.")

    length = len(prompt)
    length_part = _length_score(prompt)
    structure_part = _structure_score(prompt)
    score = length_part + structure_part
    grade = _score_to_grade(score)

    return {
        "grade": grade,
        "score": score,
        "length": length,
        "feedback": _feedback(grade, length),
    }


if __name__ == "__main__":
    # Simple demo run
    samples = [
        "",
        "Hi.",
        "What is 2 + 2?",
        "Write a function to reverse a string.",
        (
            "You are a helpful assistant. Your goal is to explain the quicksort "
            "algorithm. First, describe the partition step. Second, give an "
            "example with the array [3, 1, 4, 1, 5]. Finally, provide the "
            "implementation in Python with clear output formatting."
        ),
    ]
    for sample in samples:
        result = grade_prompt(sample)
        print(f"Grade {result['grade']} (score {result['score']}, "
              f"length {result['length']}): {sample[:40]!r}")