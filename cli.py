"""
Command Line Interface for Fine Tuner.
"""
import argparse
import sys
import json
from pathlib import Path
from typing import List, Optional

from linter import grade_prompt
from optimizer import optimize_prompt
from token_estimator import estimate_tokens

HISTORY_FILE = Path(r"D:\projects\FineTuner\history.json")

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="finetuner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Lint Command
    lint_parser = subparsers.add_parser("lint", help="Grade a prompt")
    lint_parser.add_argument("prompt", type=str)

    # Optimize Command
    opt_parser = subparsers.add_parser("optimize", help="Optimize a prompt")
    opt_parser.add_argument("prompt", type=str)

    # Diff Command
    diff_parser = subparsers.add_parser("diff", help="Compare two prompts")
    diff_parser.add_argument("prompt_a", type=str)
    diff_parser.add_argument("prompt_b", type=str)

    # History Command
    subparsers.add_parser("history", help="View saved prompts")

    return parser

def _save_history(prompt: str, action: str):
    """Save prompt to local JSON history."""
    history = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    history.append({"action": action, "prompt": prompt})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "lint":
        res = grade_prompt(args.prompt)
        print(f"Grade: {res['grade']} | Score: {res['score']} | {res['feedback']}")
        _save_history(args.prompt, "lint")
        
    elif args.command == "optimize":
        res = optimize_prompt(args.prompt)
        print(f"--- Original ({res['original_grade']}) ---\n{args.prompt}\n")
        print(f"--- Optimized ({res['optimized_grade']}) ---\n{res['optimized']}")
        _save_history(args.prompt, "optimize")
        
    elif args.command == "diff":
        res_a = estimate_tokens(args.prompt_a)
        res_b = estimate_tokens(args.prompt_b)
        print(f"Prompt A: {res_a} tokens")
        print(f"Prompt B: {res_b} tokens")
        print(f"Difference: {abs(res_a - res_b)} tokens")
        
    elif args.command == "history":
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
                for idx, item in enumerate(history):
                    print(f"{idx + 1}. [{item['action'].upper()}] {item['prompt'][:50]}...")
        else:
            print("No history found.")
            
    return 0

if __name__ == "__main__":
    sys.exit(main())