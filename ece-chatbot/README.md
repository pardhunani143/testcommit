# ECE Elasticsearch 8.1 Exam Preparation Chatbot

An LLM-powered chatbot that helps you prepare for the **Elastic Certified Engineer (ECE)** exam on **Elasticsearch 8.1**.

## Features

- **LLM mode** (with an OpenAI API key): generates contextual exam questions, evaluates your answers, and provides detailed explanations with Elasticsearch 8.1 API examples.
- **Offline mode** (no API key needed): uses a built-in question bank covering all ECE exam domains.
- **Interactive CLI**: ask questions, get hints, reveal answers, or start a scored quiz session.
- **Topic filtering**: focus study sessions on a specific exam domain.

## ECE Exam Domains Covered

| Domain | Description |
|--------|-------------|
| Data Management | ILM, data streams, ingest pipelines, index templates |
| Searching Data | Query DSL, relevance, pagination, runtime fields |
| Aggregations | Metric, bucket, pipeline aggregations |
| Mappings & Analysis | Field types, analyzers, dynamic mapping |
| Cluster Management | Node roles, shard allocation, CCS |
| Security | TLS, RBAC, DLS/FLS, API keys |
| Performance & Monitoring | JVM, thread pools, circuit breakers |
| Snapshot & Restore | Repositories, searchable snapshots |

## Prerequisites

- Python 3.8+
- (Optional) An [OpenAI API key](https://platform.openai.com/api-keys) for LLM features

## Installation

```bash
cd ece-chatbot

# Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and fill in your OpenAI API key:

```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY=sk-...
```

Or export the key directly:

```bash
export OPENAI_API_KEY=sk-...your-key-here...
```

> **Without an API key** the chatbot runs in offline mode using the built-in question bank — no API calls are made.

## Usage

### Interactive mode (default)

```bash
python chatbot.py
```

### Start with a specific topic

```bash
python chatbot.py --topic "Cluster Management"
```

### Quiz mode

```bash
python chatbot.py --quiz
# Or with a topic
python chatbot.py --quiz --topic "Security"
```

### Use a specific OpenAI model

```bash
python chatbot.py --model gpt-4o
```

### Pass an API key inline

```bash
python chatbot.py --api-key sk-...
```

## In-session Commands

| Command | Description |
|---------|-------------|
| `question [topic]` | Get a random exam question (optionally topic-filtered) |
| `answer` | Reveal the answer to the current question |
| `hint` | Get a hint without revealing the full answer |
| `quiz [topic]` | Start a scored quiz session |
| `topics` | List all available exam topic areas |
| `explain <concept>` | Get a detailed explanation of an Elasticsearch concept |
| `help` | Show the help banner |
| `quit` / `exit` | Exit the chatbot |

You can also type a free-form answer to the current question and the LLM will evaluate it.

## Example Session

```
You: question Security
📝 Question: How do you configure TLS for inter-node communication in Elasticsearch 8.1?

You: hint
💡 Think about the xpack.security.transport.ssl settings in elasticsearch.yml and the
   elasticsearch-certutil tool.

You: answer
✅ Answer:
In Elasticsearch 8.x, TLS is enabled by default for new clusters. Configure in
elasticsearch.yml:

  xpack.security.transport.ssl.enabled: true
  xpack.security.transport.ssl.verification_mode: certificate
  xpack.security.transport.ssl.keystore.path: certs/elastic-certificates.p12

Generate certificates with:
  bin/elasticsearch-certutil ca
  bin/elasticsearch-certutil cert
```

## Project Structure

```
ece-chatbot/
├── chatbot.py        # Main chatbot – interactive CLI and LLM integration
├── questions.py      # Built-in ECE 8.1 question bank (offline mode)
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variable template
└── README.md         # This file
```

## License

MIT
