"""
Token Estimator Module for Fine Tuner Application.

This module provides quick token estimation heuristics and context limit validation
for various Large Language Models (LLMs) using pure Python standard libraries.
"""

import math
from typing import Dict, Any, Optional

# --- CONFIGURATION & CONSTANTS ---
# Standard heuristic ratio: average characters per token (approx. 4 characters per token in English)
CHARS_PER_TOKEN: float = 4.0

# Context window limits (in tokens) for popular AI models
MODEL_CONTEXT_LIMITS: Dict[str, int] = {
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-3.5-turbo": 4096,
    "claude-3": 200000,
    "claude-3-opus": 200000,
    "claude-3-sonnet": 200000,
    "claude-3-haiku": 200000,
    "mistral": 32768,
    "mistral-7b": 32768,
    "mixtral-8x7b": 32768,
    "llama-3-8b": 8192,
    "llama-3-70b": 8192,
}

# Fallback token limit used when an unknown model name is provided
DEFAULT_CONTEXT_LIMIT: int = 4096


def estimate_tokens(text: str, chars_per_token: float = CHARS_PER_TOKEN) -> int:
    """
    Estimate the number of tokens in a text string based on character count.

    Args:
        text: The input prompt or text string to estimate.
        chars_per_token: Average characters per token ratio (defaults to 4.0).

    Returns:
        Estimated count of tokens (rounded up to nearest integer).
    """
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")

    if chars_per_token <= 0:
        raise ValueError("chars_per_token ratio must be greater than zero.")

    if not text:
        return 0

    # We use math.ceil so even partial tokens count towards the limit safely
    return math.ceil(len(text) / chars_per_token)


def check_context_limit(
    prompt: str,
    model_name: str,
    custom_limits: Optional[Dict[str, int]] = None
) -> Dict[str, Any]:
    """
    Check whether a given prompt exceeds the context limit of a specified LLM.

    Args:
        prompt: The input prompt string.
        model_name: The key or identifier of the AI model.
        custom_limits: Optional dictionary of model limits to override default limits.

    Returns:
        A dictionary containing:
            - 'prompt': Original prompt string
            - 'model_name': Specified model name
            - 'estimated_tokens': Calculated token count
            - 'model_limit': Context limit for the model
            - 'exceeds_limit': Boolean indicating if prompt exceeds limit
    """
    limits = custom_limits if custom_limits is not None else MODEL_CONTEXT_LIMITS

    # Normalize model name for friendly lookup (lowercase & trimmed)
    normalized_model_name = model_name.strip().lower()

    # Retrieve limit from dictionary or fallback to default limit
    model_limit = limits.get(normalized_model_name, DEFAULT_CONTEXT_LIMIT)

    # Estimate tokens in the prompt
    tokens = estimate_tokens(prompt)

    # Determine if prompt exceeds model limit
    exceeds = tokens > model_limit

    return {
        "prompt": prompt,
        "model_name": model_name,
        "estimated_tokens": tokens,
        "model_limit": model_limit,
        "exceeds_limit": exceeds
    }


if __name__ == "__main__":
    # Simple demo run
    sample_prompt = "Hello world! " * 1000
    model = "gpt-4"

    result = check_context_limit(sample_prompt, model)
    print("Token Estimation Test:")
    print(f"Model: {result['model_name']}")
    print(f"Estimated Tokens: {result['estimated_tokens']}")
    print(f"Model Limit: {result['model_limit']}")
    print(f"Exceeds Limit: {result['exceeds_limit']}")
