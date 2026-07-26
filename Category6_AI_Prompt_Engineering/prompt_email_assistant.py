"""Skillova Category 6 - AI Chatbots and Prompt Engineering.

Uses the Groq Chat Completions API to generate short professional updates.
The script tests several inputs, validates the output constraints, retries once
when needed, and saves the real test evidence to TEST_RESULTS.md and
 test_results.json.
"""

from __future__ import annotations

import getpass
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from groq import Groq
except ImportError:
    print("The Groq package is not installed. Run: pip install groq")
    sys.exit(1)

MODEL = "llama-3.3-70b-versatile"
MAX_SENTENCES = 3
MAX_WORDS = 70

SYSTEM_PROMPT = """
You write short professional workplace emails and status updates.

Follow every rule below:
1. Return only the final message body. Do not add analysis, labels, a subject line, bullet points, or markdown.
2. Use plain, professional English with a calm and factual tone.
3. Write two sentences by default and never exceed three sentences.
4. Keep the complete response under 70 words.
5. State the key update first, then the next action, timing, or expectation.
6. Avoid dramatic language, unnecessary apologies, filler, repetition, and exaggerated politeness.
7. Use only facts explicitly provided by the user. Do not infer or add deadlines, dates, processing steps, reasons, names, promises, actions, or other details.
8. Preserve all factual details supplied by the user.
""".strip()

TEST_INPUTS = [
    {
        "name": "Deployment delay",
        "prompt": (
            "Write a client update. The deployment is delayed by one day because "
            "final quality checks are still in progress. The revised delivery time "
            "is tomorrow at 3:00 PM."
        ),
    },
    {
        "name": "Dashboard complete",
        "prompt": (
            "Tell my manager that the sales dashboard is complete and ready for "
            "review. Ask them to share any changes they need."
        ),
    },
    {
        "name": "Refund approved",
        "prompt": (
            "Reply to a customer: their refund has been approved and should appear "
            "within five to seven business days."
        ),
    },
    {
        "name": "Meeting rescheduled",
        "prompt": (
            "Update the team that Thursday's meeting has moved from 10:00 AM to "
            "2:00 PM. The meeting link is unchanged."
        ),
    },
]


def get_client() -> Groq:
    """Create a Groq client without storing the API key in the code."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        api_key = getpass.getpass("Enter your Groq API key (input hidden): ").strip()
    if not api_key:
        raise RuntimeError("A Groq API key is required.")
    return Groq(api_key=api_key)


def sentence_count(text: str) -> int:
    """Count sentence-ending punctuation groups for concise-output validation."""
    cleaned = " ".join(text.strip().split())
    if not cleaned:
        return 0
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    return len([part for part in parts if part.strip()])


def has_list_format(text: str) -> bool:
    """Detect list-like output, which the system prompt forbids."""
    return any(
        re.match(r"^\s*(?:[-*•]|\d+[.)])\s+", line)
        for line in text.splitlines()
        if line.strip()
    )


def evaluate(text: str) -> dict[str, Any]:
    """Evaluate the response against the visible assignment constraints."""
    sentences = sentence_count(text)
    words = len(text.split())
    list_format = has_list_format(text)
    passed = 1 <= sentences <= MAX_SENTENCES and words <= MAX_WORDS and not list_format
    return {
        "sentence_count": sentences,
        "word_count": words,
        "contains_list_format": list_format,
        "passed": passed,
    }


def call_model(client: Groq, user_prompt: str, previous: str | None = None) -> str:
    """Call the model; on retry, include the failed answer and a correction request."""
    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
    if previous is not None:
        messages.extend(
            [
                {"role": "assistant", "content": previous},
                {
                    "role": "user",
                    "content": (
                        "Rewrite the message so it follows every system rule. "
                        "Return only the corrected message."
                    ),
                },
            ]
        )

    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2,
        max_completion_tokens=140,
    )
    content = completion.choices[0].message.content
    if not content:
        raise RuntimeError("The API returned an empty response.")
    return content.strip()


def run_test(client: Groq, test: dict[str, str]) -> dict[str, Any]:
    """Run one test and retry once if the measurable constraints fail."""
    first_response = call_model(client, test["prompt"])
    first_evaluation = evaluate(first_response)

    final_response = first_response
    final_evaluation = first_evaluation
    retried = False

    if not first_evaluation["passed"]:
        retried = True
        final_response = call_model(client, test["prompt"], previous=first_response)
        final_evaluation = evaluate(final_response)

    return {
        "name": test["name"],
        "input": test["prompt"],
        "response": final_response,
        "sentence_count": final_evaluation["sentence_count"],
        "word_count": final_evaluation["word_count"],
        "contains_list_format": final_evaluation["contains_list_format"],
        "retried": retried,
        "passed": final_evaluation["passed"],
    }


def save_results(results: list[dict[str, Any]]) -> None:
    """Save machine-readable and reviewer-friendly evidence."""
    timestamp = datetime.now(timezone.utc).isoformat()
    payload = {
        "generated_at_utc": timestamp,
        "model": MODEL,
        "constraints": {
            "maximum_sentences": MAX_SENTENCES,
            "maximum_words": MAX_WORDS,
            "list_format_allowed": False,
        },
        "system_prompt": SYSTEM_PROMPT,
        "tests": results,
    }

    Path("test_results.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    passed_count = sum(item["passed"] for item in results)
    lines = [
        "# Category 6 Test Results",
        "",
        f"- Model: `{MODEL}`",
        f"- Generated: `{timestamp}`",
        f"- Passed: **{passed_count}/{len(results)}**",
        "",
    ]
    for index, item in enumerate(results, start=1):
        lines.extend(
            [
                f"## Test {index}: {item['name']}",
                "",
                f"**Input:** {item['input']}",
                "",
                f"**Response:** {item['response']}",
                "",
                (
                    f"**Check:** {item['sentence_count']} sentence(s), "
                    f"{item['word_count']} words, retried: {item['retried']}, "
                    f"result: {'PASS' if item['passed'] else 'FAIL'}"
                ),
                "",
            ]
        )
    Path("TEST_RESULTS.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    client = get_client()
    results: list[dict[str, Any]] = []

    for test in TEST_INPUTS:
        try:
            result = run_test(client, test)
        except Exception as exc:
            result = {
                "name": test["name"],
                "input": test["prompt"],
                "response": "",
                "sentence_count": 0,
                "word_count": 0,
                "contains_list_format": False,
                "retried": False,
                "passed": False,
                "error": str(exc),
            }
        results.append(result)
        status = "PASS" if result["passed"] else "FAIL"
        print(f"{test['name']}: {status}")
        if result.get("response"):
            print(result["response"])
        if result.get("error"):
            print(f"Error: {result['error']}")
        print()

    save_results(results)
    passed_count = sum(item["passed"] for item in results)
    print(f"Completed: {passed_count}/{len(results)} tests passed.")
    print("Saved TEST_RESULTS.md and test_results.json")

    if passed_count != len(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
