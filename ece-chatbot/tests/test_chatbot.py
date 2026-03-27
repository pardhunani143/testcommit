"""
Tests for the ECE Elasticsearch 8.1 exam chatbot.
Run with: python -m pytest tests/ -v
"""

import sys
import os
import unittest
from unittest.mock import MagicMock

# Ensure the ece-chatbot package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from questions import (
    QUESTION_BANK,
    ALL_TOPICS,
    get_questions_by_topic,
    get_random_question,
    get_all_questions,
)


# ---------------------------------------------------------------------------
# Question bank tests
# ---------------------------------------------------------------------------
class TestQuestionBank(unittest.TestCase):
    def test_all_topics_non_empty(self):
        self.assertTrue(len(ALL_TOPICS) > 0)

    def test_every_topic_has_questions(self):
        for topic in ALL_TOPICS:
            self.assertTrue(
                len(QUESTION_BANK[topic]) > 0,
                f"Topic '{topic}' has no questions.",
            )

    def test_each_question_has_required_keys(self):
        for topic, questions in QUESTION_BANK.items():
            for q in questions:
                self.assertIn("question", q, f"Missing 'question' key in {topic}")
                self.assertIn("answer", q, f"Missing 'answer' key in {topic}")
                self.assertIn("difficulty", q, f"Missing 'difficulty' key in {topic}")
                self.assertIn(
                    q["difficulty"],
                    ("easy", "medium", "hard"),
                    f"Invalid difficulty in {topic}: {q['difficulty']}",
                )

    def test_get_questions_by_topic_exact(self):
        for topic in ALL_TOPICS:
            results = get_questions_by_topic(topic)
            self.assertEqual(results, QUESTION_BANK[topic])

    def test_get_questions_by_topic_partial(self):
        results = get_questions_by_topic("security")
        self.assertTrue(len(results) > 0)

    def test_get_questions_by_topic_not_found(self):
        results = get_questions_by_topic("nonexistent_topic_xyz")
        self.assertEqual(results, [])

    def test_get_random_question_returns_dict(self):
        q = get_random_question()
        self.assertIsInstance(q, dict)
        self.assertIn("question", q)

    def test_get_random_question_with_topic(self):
        q = get_random_question("Aggregations")
        self.assertIsInstance(q, dict)
        self.assertIn("question", q)

    def test_get_random_question_invalid_topic(self):
        q = get_random_question("invalid_xyz")
        self.assertEqual(q, {})

    def test_get_all_questions_count(self):
        all_q = get_all_questions()
        expected = sum(len(qs) for qs in QUESTION_BANK.values())
        self.assertEqual(len(all_q), expected)


# ---------------------------------------------------------------------------
# Chatbot unit tests
# ---------------------------------------------------------------------------
class TestLLMClientOffline(unittest.TestCase):
    """Tests for LLMClient when no API key is set."""

    def test_llm_client_unavailable_without_key(self):
        from chatbot import LLMClient

        client = LLMClient(api_key="")
        self.assertFalse(client.available)


class TestECEChatbotOffline(unittest.TestCase):
    """Tests for ECEChatbot running in offline mode (no LLM)."""

    def setUp(self):
        from chatbot import ECEChatbot, LLMClient

        self.llm = LLMClient(api_key="")  # offline
        self.bot = ECEChatbot(llm=self.llm)

    def test_handle_topics_does_not_raise(self):
        self.bot.handle_topics()  # should print without error

    def test_handle_question_sets_current_question(self):
        self.bot.handle_question()
        self.assertIsNotNone(self.bot.current_question)
        self.assertIn("question", self.bot.current_question)

    def test_handle_question_with_topic(self):
        self.bot.handle_question("Security")
        self.assertIsNotNone(self.bot.current_question)

    def test_handle_answer_no_question(self):
        self.bot.current_question = None
        self.bot.handle_answer()  # should not raise

    def test_handle_answer_with_question(self):
        self.bot.handle_question()
        self.bot.handle_answer()  # should not raise

    def test_handle_hint_with_question(self):
        self.bot.handle_question()
        self.bot.handle_hint()  # should not raise

    def test_handle_hint_no_question(self):
        self.bot.current_question = None
        self.bot.handle_hint()  # should not raise


class TestECEChatbotWithMockedLLM(unittest.TestCase):
    """Tests for ECEChatbot with a mocked LLM."""

    def setUp(self):
        from chatbot import ECEChatbot, LLMClient

        self.llm = MagicMock(spec=LLMClient)
        self.llm.available = True
        self.llm.chat.return_value = "Question: What is an ILM policy?"
        self.bot = ECEChatbot(llm=self.llm)

    def test_handle_question_calls_llm(self):
        self.bot.handle_question()
        self.llm.chat.assert_called_once()

    def test_handle_explain_calls_llm(self):
        self.bot.handle_explain("data streams")
        self.llm.chat.assert_called_once()
        call_args = self.llm.chat.call_args[0][0]
        self.assertIn("data streams", call_args)

    def test_handle_user_chat_calls_llm(self):
        self.bot.handle_user_chat("What is shard allocation?")
        self.llm.chat.assert_called_once()


class TestParseArgs(unittest.TestCase):
    def test_defaults(self):
        from chatbot import parse_args

        args = parse_args([])
        self.assertIsNone(args.topic)
        self.assertFalse(args.quiz)
        self.assertEqual(args.model, "gpt-4o-mini")

    def test_topic_flag(self):
        from chatbot import parse_args

        args = parse_args(["--topic", "Security"])
        self.assertEqual(args.topic, "Security")

    def test_quiz_flag(self):
        from chatbot import parse_args

        args = parse_args(["--quiz"])
        self.assertTrue(args.quiz)

    def test_model_flag(self):
        from chatbot import parse_args

        args = parse_args(["--model", "gpt-4o"])
        self.assertEqual(args.model, "gpt-4o")


if __name__ == "__main__":
    unittest.main()
