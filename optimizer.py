"""
Prompt Optimizer for Fine Tuner Application.

Takes a raw user prompt and rewrites it into a higher-quality, LLM-ready
version by adding a role, explicit objective, step-by-step structure,
and output formatting constraints. Pure standard library: no I/O, no
network, no third-party dependencies, so it stays deterministic and
easy to unit test.
"""

from typing import Dict, Any, List

from linter import grade_prompt
from token_estimator import estimate_tokens

# --- DEFAULT TEMPLATE PARTS ---
# These pieces are appended to a prompt when the linter detects the
# original is missing them. They raise the structural score the most.
DEFAULT_ROLE: str = (
    "You are a meticulous, expert assistant."
)
DEFAULT_OBJECTIVE: str = (
    "Your goal is to answer the user's request clearly and accurately."
)
DEFAULT_FORMAT: str = (
    "Provide a concise, well-structured response. Use numbered steps "
    "or bullet points where helpful, and keep the final answer explicit."
)
DEFAULT_CONSTRAINTS: str = (
    "Stay on topic, avoid unnecessary commentary, and respect any "
    "limits the user set."
)


def _suggest_missing_parts(prompt: str) -> List[str]:
    """
    Inspect a prompt and return a list of structural parts it is missing.

    Uses the same vocabulary the linter rewards so the optimized
    output reliably grades higher.
    """
    lower = prompt.lower()
    missing: List[str] = []

    # Role / persona is rarely present in a raw one-liner.
    if not any(word in lower for word in ("you are", "as a", "role")):
        missing.append("role")

    # An explicit objective/goal sentence.
    if not any(word in lower for word in ("goal", "objective", "purpose", "aim")):
        missing.append("objective")

    # Formatting instructions.
    if not any(word in lower for word in ("format", "output", "step", "bullet")):
        missing.append("format")

    # Constraints / requirements.
    if not any(word in lower for word in ("constraint", "requirement", "limit", "must")):
        missing.append("constraints")

    return missing


def optimize_prompt(prompt: str) -> Dict[str, Any]:
    """
    Rewrite a raw prompt into a higher-quality, LLM-ready version.

    Args:
        prompt: The raw prompt string to optimize.

    Returns:
        A dictionary containing:
            - 'original': The original prompt string.
            - 'optimized': The rewritten, structured prompt string.
            - 'original_tokens': Estimated tokens of the original.
            - 'optimized_tokens': Estimated tokens of the optimized version.
            - 'original_grade': Letter grade of the original.
            - 'optimized_grade': Letter grade of the optimized version.
            - 'improvement': Estimated token delta (optimized - original).
            - 'added_parts': List of structural parts that were added.

    Raises:
        TypeError: If prompt is not a string.
    """
    if not isinstance(prompt, str):
        raise TypeError("prompt must be a string.")

    original = prompt.strip()
    if not original:
        # Nothing to optimize; return an empty-shell result.
        return {
            "original": original,
            "optimized": original,
            "original_tokens": 0,
            "optimized_tokens": 0,
            "original_grade": grade_prompt(original)["grade"],
            "optimized_grade": grade_prompt(original)["grade"],
            "improvement": 0,
            "added_parts": [],
        }

    missing = _suggest_missing_parts(original)

    # Build the optimized prompt by wrapping the original with the
    # structural parts it was missing. Keeping the user's own words
    # intact means the request itself is not altered, only framed.
    sections: List[str] = [DEFAULT_ROLE]

    if "objective" in missing:
        sections.append(DEFAULT_OBJECTIVE)

    sections.append("User request:")
    sections.append(f'"{original}"')

    if "format" in missing:
        sections.append(DEFAULT_FORMAT)

    if "constraints" in missing:
        sections.append(DEFAULT_CONSTRAINTS)

    optimized = "\n\n".join(sections).strip()

    original_tokens = estimate_tokens(original)
    optimized_tokens = estimate_tokens(optimized)

    original_grade = grade_prompt(original)["grade"]
    optimized_grade = grade_prompt(optimized)["grade"]

    return {
        "original": original,
        "optimized": optimized,
        "original_tokens": original_tokens,
        "optimized_tokens": optimized_tokens,
        "original_grade": original_grade,
        "optimized_grade": optimized_grade,
        "improvement": optimized_tokens - original_tokens,
        "added_parts": missing,
    }


if __name__ == "__main__":
    # Simple demo run
    samples = [
        "explain quicksort",
        "write a python function to reverse a string",
        (
            "You are a helpful assistant. Your goal is to explain the quicksort "
            "algorithm. First, describe the partition step. Second, give an "
            "example with the array [3, 1, 4, 1, 5]. Finally, provide the "
            "implementation in Python with clear output formatting."
        ),
    ]
    for sample in samples:
        result = optimize_prompt(sample)
        print(f"Original ({result['original_tokens']}t, {result['original_grade']}): "
              f"{sample[:50]!r}")
        print(f"Optimized ({result['optimized_tokens']}t, {result['optimized_grade']}): "
              f"{result['optimized'][:80]!r}")
        print(f"Added parts: {result['added_parts']}")
        print("-" * 60)