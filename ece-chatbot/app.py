"""
ECE (Elastic Certified Engineer) Exam Chatbot – Elasticsearch 8.1

A CLI chatbot that helps you prepare for the ECE exam by:
  • Quizzing you with multiple-choice questions from a built-in question bank
  • Generating additional questions on demand via an OpenAI-compatible LLM
  • Explaining answers in detail

Usage
-----
  python app.py                    # Interactive mode
  python app.py --quiz             # Jump straight into a quiz session
  python app.py --category CATEGORY  # Filter questions by category
  python app.py --list-categories  # Print available categories

Environment variables
---------------------
  OPENAI_API_KEY   – Required for LLM-generated questions (optional for built-in questions)
  OPENAI_BASE_URL  – Override the API endpoint (default: https://api.openai.com/v1)
  OPENAI_MODEL     – Model to use (default: gpt-4o-mini)
"""

import os
import sys
import json
import random
import textwrap
import argparse

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from questions import QUESTIONS, CATEGORIES

# ─── Styling helpers ──────────────────────────────────────────────────────────

WIDTH = 80


def hr(char="─"):
    return char * WIDTH


def wrap(text, indent=0):
    prefix = " " * indent
    return textwrap.fill(text, width=WIDTH, initial_indent=prefix, subsequent_indent=prefix)


def print_header():
    print()
    print(hr("═"))
    print("  🔍  ECE Exam Prep Chatbot  •  Elasticsearch 8.1")
    print(hr("═"))
    print()


def print_question(q, index, total):
    print()
    print(hr())
    category_label = f"[{q['category']}]"
    print(f"  Question {index}/{total}  {category_label}")
    print(hr())
    print()
    print(wrap(q["question"], indent=2))
    print()
    for key, text in sorted(q["options"].items()):
        print(wrap(f"  {key})  {text}", indent=6))
    print()


def print_result(correct, q):
    if correct:
        print("\n  ✅  Correct!\n")
    else:
        print(f"\n  ❌  Incorrect. The correct answer is: {q['answer']}\n")
    print(wrap(f"Explanation: {q['explanation']}", indent=4))
    print()


# ─── LLM client ───────────────────────────────────────────────────────────────

def get_openai_client():
    """Return an OpenAI client, or None if not configured."""
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key or not OPENAI_AVAILABLE:
        return None
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").strip()
    return OpenAI(api_key=api_key, base_url=base_url)


def ask_llm(client, prompt, system_prompt=None):
    """Send a prompt to the LLM and return the text response."""
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


SYSTEM_PROMPT = (
    "You are an expert Elasticsearch instructor helping candidates prepare for the "
    "ECE (Elastic Certified Engineer) exam for Elasticsearch 8.1. "
    "Provide accurate, detailed, and pedagogically useful answers. "
    "When generating exam questions, match the style and difficulty of the official ECE exam."
)


def generate_llm_question(client, category=None):
    """Ask the LLM to generate a new multiple-choice ECE exam question."""
    category_hint = f" in the domain '{category}'" if category else ""
    prompt = (
        f"Generate one multiple-choice exam question{category_hint} for the "
        "ECE (Elastic Certified Engineer) exam on Elasticsearch 8.1. "
        "Return ONLY valid JSON with the following keys: "
        "question (string), options (object with keys A/B/C/D), answer (string, one of A/B/C/D), "
        "explanation (string). Do not include any text outside the JSON object."
    )
    raw = ask_llm(client, prompt, SYSTEM_PROMPT)
    # Strip markdown code fences if present
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        data = json.loads(raw)
        return {
            "id": "llm",
            "category": category or "LLM-Generated",
            "question": data["question"],
            "options": data["options"],
            "answer": data["answer"].upper(),
            "explanation": data["explanation"],
        }
    except (json.JSONDecodeError, KeyError) as exc:
        return None


# ─── Chat mode ────────────────────────────────────────────────────────────────

CHAT_HELP = """
Commands you can type:
  quiz [N] [category]  – Start a quiz with N questions (default 5)
  generate [category]  – Generate a new LLM question for a category
  categories           – List available question categories
  help                 – Show this help message
  exit / quit          – Exit the chatbot

Or just ask anything about Elasticsearch 8.1 and the ECE exam!
"""


def run_chat_mode(client):
    """Interactive free-form chat loop."""
    print_header()
    print(wrap(
        "Welcome! I'm your ECE exam prep assistant for Elasticsearch 8.1. "
        "Type 'help' for available commands, or ask me anything about Elasticsearch!"
    ))
    print()

    history = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Good luck with your exam! 🎓")
            break

        if not user_input:
            continue

        lower = user_input.lower()

        # ── Built-in commands ──────────────────────────────────────────────

        if lower in ("exit", "quit"):
            print("Goodbye! Good luck with your exam! 🎓")
            break

        if lower == "help":
            print(CHAT_HELP)
            continue

        if lower == "categories":
            print("\nAvailable categories:")
            for cat in CATEGORIES:
                print(f"  • {cat}")
            print()
            continue

        if lower.startswith("quiz"):
            parts = lower.split()
            n = 5
            cat = None
            if len(parts) > 1 and parts[1].isdigit():
                n = int(parts[1])
                if len(parts) > 2:
                    cat = " ".join(parts[2:]).title()
            elif len(parts) > 1:
                cat = " ".join(parts[1:]).title()
            run_quiz(client, n, cat)
            continue

        if lower.startswith("generate"):
            parts = user_input.split(maxsplit=1)
            cat = parts[1].strip() if len(parts) > 1 else None
            if not client:
                print(
                    "\n⚠️  LLM question generation requires OPENAI_API_KEY to be set.\n"
                )
                continue
            print("\n⏳ Generating question…")
            q = generate_llm_question(client, cat)
            if q:
                print_question(q, 1, 1)
                answer = input("  Your answer (A/B/C/D): ").strip().upper()
                correct = answer == q["answer"]
                print_result(correct, q)
            else:
                print("\n❌ Failed to parse LLM response. Please try again.\n")
            continue

        # ── Free-form LLM conversation ─────────────────────────────────────

        if not client:
            print(
                "\n🤖 To chat freely, set OPENAI_API_KEY in your environment.\n"
                "   For now, try: quiz, generate, categories, or help.\n"
            )
            continue

        history.append({"role": "user", "content": user_input})
        messages_to_send = [{"role": "system", "content": SYSTEM_PROMPT}] + history

        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()
        response = client.chat.completions.create(
            model=model,
            messages=messages_to_send,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
        history.append({"role": "assistant", "content": reply})
        print(f"\nBot: {wrap(reply)}\n")


# ─── Quiz mode ────────────────────────────────────────────────────────────────

def run_quiz(client, n=5, category=None):
    """Run a quiz session."""
    pool = QUESTIONS[:]
    if category:
        # Case-insensitive partial match
        pool = [
            q for q in pool
            if category.lower() in q["category"].lower()
        ]
        if not pool:
            print(f"\n⚠️  No questions found for category '{category}'.\n")
            print("Available categories:")
            for cat in CATEGORIES:
                print(f"  • {cat}")
            print()
            return

    random.shuffle(pool)
    selected = pool[:n]

    if not selected:
        print("\n⚠️  Question pool is empty.\n")
        return

    score = 0
    total = len(selected)

    print()
    print(f"  Starting quiz: {total} question(s)")
    if category:
        print(f"  Category filter: {category}")
    print(hr())

    for i, q in enumerate(selected, start=1):
        print_question(q, i, total)
        while True:
            answer = input("  Your answer (A/B/C/D, or 'skip'): ").strip().upper()
            if answer in ("A", "B", "C", "D", "SKIP"):
                break
            print("  Please enter A, B, C, D, or 'skip'.")

        if answer == "SKIP":
            print(f"\n  ⏭️  Skipped. Correct answer: {q['answer']}\n")
            print(wrap(f"Explanation: {q['explanation']}", indent=4))
            print()
        else:
            correct = answer == q["answer"]
            if correct:
                score += 1
            print_result(correct, q)

    print(hr())
    pct = int(score / total * 100)
    print(f"\n  🏁 Quiz complete!  Score: {score}/{total} ({pct}%)\n")
    if pct >= 80:
        print("  🌟 Excellent work! You're well on your way to passing the ECE exam.")
    elif pct >= 60:
        print("  👍 Good effort! Keep reviewing the topics you missed.")
    else:
        print("  📚 Keep studying – practice makes perfect!")
    print()


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ECE Exam Prep Chatbot for Elasticsearch 8.1"
    )
    parser.add_argument(
        "--quiz",
        action="store_true",
        help="Start directly in quiz mode",
    )
    parser.add_argument(
        "--num-questions",
        type=int,
        default=5,
        metavar="N",
        help="Number of questions per quiz session (default: 5)",
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="Filter questions by category (partial, case-insensitive match)",
    )
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List available question categories and exit",
    )
    args = parser.parse_args()

    if args.list_categories:
        print("\nAvailable ECE exam question categories:")
        for cat in CATEGORIES:
            print(f"  • {cat}")
        print()
        sys.exit(0)

    client = get_openai_client()
    if not client and OPENAI_AVAILABLE:
        print(
            "\n⚠️  OPENAI_API_KEY is not set. LLM features are disabled.\n"
            "   Built-in question bank and quiz mode are fully available.\n"
        )
    elif not OPENAI_AVAILABLE:
        print(
            "\n⚠️  'openai' package not installed. LLM features are disabled.\n"
            "   Run: pip install openai\n"
        )

    if args.quiz:
        print_header()
        run_quiz(client, n=args.num_questions, category=args.category)
    else:
        run_chat_mode(client)


if __name__ == "__main__":
    main()
