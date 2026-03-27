#!/usr/bin/env python3
"""
ECE Elasticsearch 8.1 Exam Chatbot
====================================
An LLM-powered chatbot that helps you prepare for the
Elastic Certified Engineer (ECE) exam on Elasticsearch 8.1.

Modes:
  - With OPENAI_API_KEY: uses GPT to generate contextual exam questions/answers.
  - Without API key: uses the built-in question bank (questions.py).

Usage:
  python chatbot.py               # interactive CLI mode
  python chatbot.py --topic "Aggregations"   # start in a specific topic
  python chatbot.py --quiz        # quiz mode (answer questions, get scored)
"""

import os
import sys
import json
import argparse
import textwrap
import random
from typing import Optional

# ---------------------------------------------------------------------------
# Optional OpenAI integration
# ---------------------------------------------------------------------------
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from questions import (
    QUESTION_BANK,
    ALL_TOPICS,
    get_questions_by_topic,
    get_random_question,
    get_all_questions,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are an expert Elasticsearch instructor and exam coach specializing in
the Elastic Certified Engineer (ECE) certification for Elasticsearch version 8.1.

Your role is to:
1. Generate challenging, realistic exam questions covering all ECE exam domains:
   - Data Management (ILM, data streams, ingest pipelines, mappings)
   - Searching Data (queries, relevance scoring, pagination, runtime fields)
   - Aggregations (metric, bucket, pipeline aggregations)
   - Mappings & Analysis (analyzers, field types, dynamic mapping)
   - Cluster Management (node roles, shard allocation, cross-cluster search)
   - Security (TLS, RBAC, DLS, FLS, API keys)
   - Performance & Monitoring (metrics, thread pools, circuit breakers)
   - Snapshot & Restore (repositories, searchable snapshots)

2. Provide clear, accurate answers with Elasticsearch 8.1 API examples.
3. Explain *why* an answer is correct to reinforce understanding.
4. When the user answers a question, evaluate their answer and give constructive feedback.
5. Adjust difficulty based on user performance.

Always include real API calls, JSON bodies, and Elasticsearch 8.1-specific details.
Keep your responses concise and focused on exam preparation.
"""

WELCOME_BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║      ECE Elasticsearch 8.1 Exam Preparation Chatbot             ║
╚══════════════════════════════════════════════════════════════════╝

Welcome! I will help you prepare for the Elastic Certified Engineer exam.

Commands:
  question [topic]  - Get an exam question (optionally for a specific topic)
  quiz              - Start a scored quiz session
  topics            - List available exam topic areas
  hint              - Get a hint for the current question
  answer            - Reveal the answer to the current question
  explain <topic>   - Get an explanation of a concept
  help              - Show this help message
  quit / exit       - Exit the chatbot

Topics: """ + ", ".join(ALL_TOPICS) + """

Type a message or command to get started!
"""

WRAP_WIDTH = 80


def wrap(text: str) -> str:
    """Wrap text for terminal display."""
    lines = []
    for paragraph in text.split("\n"):
        if paragraph.strip() == "":
            lines.append("")
        else:
            lines.extend(textwrap.wrap(paragraph, width=WRAP_WIDTH) or [""])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# LLM client
# ---------------------------------------------------------------------------
class LLMClient:
    """Thin wrapper around the OpenAI chat completions API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.available = False
        self.model = model
        if not OPENAI_AVAILABLE:
            return
        key = api_key or os.environ.get("OPENAI_API_KEY", "")
        if not key:
            return
        self.client = OpenAI(api_key=key)
        self.available = True
        self.conversation_history: list = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def chat(self, user_message: str) -> str:
        """Send a message and return the assistant reply."""
        if not self.available:
            raise RuntimeError("OpenAI client is not available.")
        self.conversation_history.append(
            {"role": "user", "content": user_message}
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            temperature=0.7,
            max_tokens=1024,
        )
        reply = response.choices[0].message.content
        self.conversation_history.append(
            {"role": "assistant", "content": reply}
        )
        return reply

    def reset_conversation(self):
        """Reset conversation history (keep system prompt)."""
        self.conversation_history = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]


# ---------------------------------------------------------------------------
# Chatbot logic
# ---------------------------------------------------------------------------
class ECEChatbot:
    """Main chatbot controller."""

    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.current_question: Optional[dict] = None
        self.quiz_score = 0
        self.quiz_total = 0
        self.quiz_mode = False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _print(self, text: str, prefix: str = "🤖 ") -> None:
        print(f"\n{prefix}{wrap(text)}\n")

    def _get_llm_question(self, topic: Optional[str] = None) -> str:
        """Ask the LLM to generate an exam question."""
        if topic:
            prompt = (
                f"Generate a single exam question for the ECE Elasticsearch 8.1 exam "
                f"in the topic area: '{topic}'. "
                "Present only the question text (no answer yet). "
                "Start with 'Question:'"
            )
        else:
            prompt = (
                "Generate a single exam question for the ECE Elasticsearch 8.1 exam. "
                "Choose a random topic from the exam domains. "
                "Present only the question text (no answer yet). "
                "Start with 'Question:'"
            )
        return self.llm.chat(prompt)

    def _get_llm_answer(self, question: str) -> str:
        """Ask the LLM to answer the last question."""
        return self.llm.chat(
            f"Now provide a detailed answer to the question: '{question}'. "
            "Include Elasticsearch 8.1 API examples and JSON where relevant."
        )

    def _get_llm_hint(self, question: str) -> str:
        """Ask the LLM for a hint."""
        return self.llm.chat(
            f"Give a brief hint for this question without revealing the full answer: '{question}'"
        )

    def _evaluate_answer(self, question: str, user_answer: str) -> str:
        """Ask the LLM to evaluate the user's answer."""
        return self.llm.chat(
            f"The question was: '{question}'\n"
            f"The user answered: '{user_answer}'\n"
            "Evaluate the answer: is it correct, partially correct, or incorrect? "
            "Provide the correct answer and explain any gaps."
        )

    # ------------------------------------------------------------------
    # Command handlers
    # ------------------------------------------------------------------
    def handle_question(self, topic: Optional[str] = None) -> None:
        """Fetch and display an exam question."""
        if self.llm.available:
            text = self._get_llm_question(topic)
            self.current_question = {"question": text, "answer": None, "source": "llm"}
            self._print(text, prefix="📝 ")
        else:
            q = get_random_question(topic)
            if not q:
                self._print(
                    f"No questions found for topic '{topic}'. "
                    f"Available topics: {', '.join(ALL_TOPICS)}"
                )
                return
            self.current_question = q
            self._print(q["question"], prefix="📝 ")

    def handle_answer(self) -> None:
        """Reveal the answer to the current question."""
        if not self.current_question:
            self._print("No active question. Type 'question' to get one.")
            return

        q = self.current_question
        if self.llm.available and q.get("source") == "llm":
            answer = self._get_llm_answer(q["question"])
            self._print(answer, prefix="✅ ")
        else:
            answer = q.get("answer", "No answer available.")
            self._print(f"Answer:\n{answer}", prefix="✅ ")

    def handle_hint(self) -> None:
        """Give a hint for the current question."""
        if not self.current_question:
            self._print("No active question. Type 'question' to get one.")
            return

        q = self.current_question
        if self.llm.available:
            hint = self._get_llm_hint(q["question"])
            self._print(hint, prefix="💡 ")
        else:
            self._print(
                "Hint: Think about the Elasticsearch 8.1 documentation for this topic. "
                "Type 'answer' to reveal the full answer.",
                prefix="💡 ",
            )

    def handle_topics(self) -> None:
        """List available topics."""
        lines = ["Available ECE exam topic areas:\n"]
        for i, topic in enumerate(ALL_TOPICS, 1):
            count = len(QUESTION_BANK[topic])
            lines.append(f"  {i}. {topic} ({count} questions in bank)")
        self._print("\n".join(lines), prefix="📚 ")

    def handle_explain(self, concept: str) -> None:
        """Explain a concept."""
        if self.llm.available:
            reply = self.llm.chat(
                f"Explain the concept of '{concept}' in the context of Elasticsearch 8.1 "
                "for an ECE exam candidate. Include practical examples."
            )
            self._print(reply, prefix="📖 ")
        else:
            self._print(
                f"Concept: {concept}\n\n"
                "LLM explanation is not available (no OpenAI API key configured).\n"
                "Please refer to the official Elasticsearch 8.1 documentation at "
                "https://www.elastic.co/guide/en/elasticsearch/reference/8.1/",
                prefix="📖 ",
            )

    def handle_user_chat(self, user_input: str) -> None:
        """Pass free-form user input to the LLM."""
        if self.llm.available:
            reply = self.llm.chat(user_input)
            self._print(reply)
        else:
            self._print(
                "I'm running in offline mode (no OpenAI API key). "
                "Available commands: question, answer, hint, topics, explain <topic>, quiz, help, quit."
            )

    # ------------------------------------------------------------------
    # Quiz mode
    # ------------------------------------------------------------------
    def run_quiz(self, num_questions: int = 5, topic: Optional[str] = None) -> None:
        """Run an interactive quiz session."""
        self._print(
            f"Starting quiz – {num_questions} questions"
            + (f" on '{topic}'" if topic else " (mixed topics)")
            + ".\nType your answer and press Enter. Type 'skip' to skip a question.",
            prefix="🎯 ",
        )

        if topic:
            pool = get_questions_by_topic(topic)
        else:
            pool = get_all_questions()

        if not pool:
            self._print(f"No questions available for topic '{topic}'.")
            return

        selected = random.sample(pool, min(num_questions, len(pool)))
        score = 0

        for idx, q in enumerate(selected, 1):
            print(f"\n{'─' * 60}")
            print(f"Question {idx}/{len(selected)}:")
            print(wrap(q["question"]))
            print()

            user_answer = input("Your answer: ").strip()
            if user_answer.lower() == "skip":
                print(wrap(f"\n⏭  Skipped. Correct answer:\n{q['answer']}"))
                continue

            if self.llm.available:
                feedback = self._evaluate_answer(q["question"], user_answer)
                print("\n" + wrap(feedback))
                correct = input("\nDid you get it right? (y/n): ").strip().lower()
                if correct == "y":
                    score += 1
            else:
                print(f"\nCorrect answer:\n{wrap(q['answer'])}")
                correct = input("\nDid you get it right? (y/n): ").strip().lower()
                if correct == "y":
                    score += 1

        self.quiz_score += score
        self.quiz_total += len(selected)
        pct = round(score / len(selected) * 100)

        print(f"\n{'═' * 60}")
        print(f"Quiz complete! Score: {score}/{len(selected)} ({pct}%)")
        if pct >= 80:
            print("🎉 Excellent! You're well prepared for the ECE exam.")
        elif pct >= 60:
            print("📈 Good progress. Keep studying the weaker areas.")
        else:
            print("📚 Keep practicing – review the official Elasticsearch 8.1 docs.")
        print(f"Session total: {self.quiz_score}/{self.quiz_total}")
        print(f"{'═' * 60}\n")

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self, initial_topic: Optional[str] = None, quiz_mode: bool = False) -> None:
        """Start the interactive chatbot loop."""
        print(WELCOME_BANNER)

        if not self.llm.available:
            print(
                "ℹ️  Running in OFFLINE mode (no OpenAI API key detected).\n"
                "   Set OPENAI_API_KEY environment variable to enable LLM features.\n"
            )

        if quiz_mode:
            self.run_quiz()
            return

        if initial_topic:
            self.handle_question(initial_topic)

        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye! Good luck with the ECE exam! 🎓")
                break

            if not user_input:
                continue

            cmd = user_input.lower()

            if cmd in ("quit", "exit", "q"):
                print("\nGoodbye! Good luck with the ECE exam! 🎓")
                break
            elif cmd == "help":
                print(WELCOME_BANNER)
            elif cmd == "topics":
                self.handle_topics()
            elif cmd.startswith("question"):
                parts = user_input.split(maxsplit=1)
                topic = parts[1] if len(parts) > 1 else None
                self.handle_question(topic)
            elif cmd == "answer":
                self.handle_answer()
            elif cmd == "hint":
                self.handle_hint()
            elif cmd.startswith("explain "):
                concept = user_input[8:].strip()
                self.handle_explain(concept)
            elif cmd.startswith("quiz"):
                parts = user_input.split(maxsplit=1)
                topic = parts[1] if len(parts) > 1 else None
                self.run_quiz(topic=topic)
            else:
                # Evaluate user answer if there's an active question
                if self.current_question and self.llm.available:
                    feedback = self._evaluate_answer(
                        self.current_question["question"], user_input
                    )
                    self._print(feedback, prefix="🔍 ")
                else:
                    self.handle_user_chat(user_input)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="ECE Elasticsearch 8.1 Exam Preparation Chatbot"
    )
    parser.add_argument(
        "--topic",
        metavar="TOPIC",
        help="Start with a question from this exam topic",
    )
    parser.add_argument(
        "--quiz",
        action="store_true",
        help="Start in quiz mode",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model to use (default: gpt-4o-mini)",
    )
    parser.add_argument(
        "--api-key",
        metavar="KEY",
        help="OpenAI API key (overrides OPENAI_API_KEY env var)",
    )
    return parser.parse_args(argv)


def main():
    args = parse_args()
    llm = LLMClient(api_key=args.api_key, model=args.model)
    bot = ECEChatbot(llm=llm)
    bot.run(initial_topic=args.topic, quiz_mode=args.quiz)


if __name__ == "__main__":
    main()
