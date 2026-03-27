# ECE Exam Prep Chatbot – Elasticsearch 8.1

An interactive CLI chatbot that helps you prepare for the
**ECE (Elastic Certified Engineer)** exam on **Elasticsearch 8.1**.

## Features

- 📚 **Built-in question bank** – 35 exam-style multiple-choice questions covering all ECE exam domains
- 🤖 **LLM-powered chat** – ask free-form questions about Elasticsearch 8.1 (requires OpenAI API key)
- ✨ **LLM question generation** – generate additional exam questions on demand
- 🏆 **Scored quiz mode** – track your progress with instant feedback and explanations
- 🔍 **Category filtering** – focus on specific domains (Indexing, Security, Aggregations, etc.)

## Exam Domains Covered

| Domain | # Questions |
|---|---|
| Installation & Configuration | 4 |
| Indexing | 4 |
| Mappings | 4 |
| Searching | 4 |
| Aggregations | 3 |
| Cluster Management | 4 |
| Security | 3 |
| Snapshots & Restore | 2 |
| Index Lifecycle Management | 2 |
| Data Streams | 2 |
| Cross-Cluster Replication | 1 |
| Monitoring | 2 |
| **Total** | **35** |

## Requirements

- Python 3.9+
- `openai` package (optional – only needed for LLM features)

## Installation

```bash
cd ece-chatbot

# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Configure your OpenAI API key
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

## Usage

### Interactive chat mode (default)

```bash
python app.py
```

In chat mode you can:
- Type natural language questions about Elasticsearch 8.1
- Use built-in commands: `quiz`, `generate`, `categories`, `help`, `exit`

### Quiz mode

```bash
# Quick 5-question quiz (random categories)
python app.py --quiz

# 10-question quiz
python app.py --quiz --num-questions 10

# Quiz focused on a specific category
python app.py --quiz --category "Security"
python app.py --quiz --category "Indexing"
```

### List available categories

```bash
python app.py --list-categories
```

### In-chat commands

| Command | Description |
|---|---|
| `quiz [N] [category]` | Start a quiz with N questions (default 5), optionally filtered by category |
| `generate [category]` | Generate a new LLM question (requires API key) |
| `categories` | List all available question categories |
| `help` | Show the help message |
| `exit` / `quit` | Exit the chatbot |

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | – | Your OpenAI API key (required for LLM features) |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | API endpoint (override for Azure OpenAI, local LLMs, etc.) |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model to use for LLM requests |

## Example Session

```
════════════════════════════════════════════════════════════════════════════════
  🔍  ECE Exam Prep Chatbot  •  Elasticsearch 8.1
════════════════════════════════════════════════════════════════════════════════

Welcome! I'm your ECE exam prep assistant for Elasticsearch 8.1. Type 'help'
for available commands, or ask me anything about Elasticsearch!

You: quiz 3 security

  Starting quiz: 3 question(s)
  Category filter: Security
────────────────────────────────────────────────────────────────────────────────

  Question 1/3  [Security]
────────────────────────────────────────────────────────────────────────────────

  In Elasticsearch 8.1, what is enabled by default that was optional in
  earlier versions?

      A)  Cross-cluster search
      B)  Security features (TLS and authentication)
      C)  Index lifecycle management
      D)  Machine learning

  Your answer (A/B/C/D, or 'skip'): B

  ✅  Correct!

    Explanation: Since Elasticsearch 8.0, security features are enabled by
    default. TLS for transport and HTTP layers and basic authentication are
    automatically configured when you start a new cluster.
```

## Project Structure

```
ece-chatbot/
├── app.py           # Main chatbot application
├── questions.py     # Built-in ECE 8.1 question bank
├── requirements.txt # Python dependencies
├── .env.example     # Environment variable template
└── README.md        # This file
```

## License

MIT
