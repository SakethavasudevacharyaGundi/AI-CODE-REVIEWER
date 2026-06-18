# Multi-Agent AI Code Reviewer

An AI-powered pull request review system built with FastAPI, LangGraph, and Groq LLMs. The system uses multiple specialized reviewer agents to analyze code diffs and generate structured review reports covering security, performance, correctness, style, and test coverage.

---

# Overview

Multi-Agent AI Code Reviewer implements a reviewer pipeline where each agent specializes in a single responsibility:

* Security
* Performance
* Correctness
* Style
* Test Coverage

Each reviewer independently analyzes a supplied git diff and produces findings specific to its domain. LangGraph orchestrates the reviewers and merges their outputs into a structured review report.

---

# Features

* Multi-agent review architecture
* Security reviewer agent
* Performance reviewer agent
* Correctness reviewer agent
* Style reviewer agent
* Test coverage reviewer agent
* LangGraph-based orchestration
* Structured Pydantic output schemas
* JSON review reports
* Review persistence and retrieval
* FastAPI REST API
* Automated review generation
* Category-specific reviewer prompts

The system reviews unified git diffs and generates structured pull request feedback across multiple quality dimensions.

---

# Architecture

## Review Pipeline

```text
Git Diff
   │
   ▼
Review Request
   │
   ▼
LangGraph Orchestrator
   │
   ├── Security Reviewer
   ├── Performance Reviewer
   ├── Correctness Reviewer
   ├── Style Reviewer
   └── Test Coverage Reviewer
   │
   ▼
Merge & Aggregate Findings
   │
   ▼
Review Report
   │
   ▼
Storage Layer
```

## Components

* **FastAPI** – API layer exposing review endpoints
* **LangGraph** – Reviewer orchestration workflow
* **Groq LLM** – Structured code analysis
* **Pydantic** – Validation and response schemas
* **Reviewer Agents** – Specialized analysis nodes
* **Storage Layer** – Persists generated reviews

---

# Project Structure

```text
.
├── app
│   ├── graph
│   ├── models
│   ├── prompts
│   ├── reviewers
│   ├── storage
│   ├── llm.py
│   └── main.py
│
├── reviews
│   ├── diff1_review.json
│   ├── diff2_review.json
│   └── diff3_review.json
│
├── run_reviews.py
├── .env.example
├── requirements.txt
└── README.md
```

---

# Quick Start

## Clone the Repository

```bash
git clone <repository-url>
cd ai-code-reviewer
```

## Configure Environment Variables

Create a `.env` file from `.env.example`.

```env
GROQ_API_KEY=your_api_key_here
```

## One-Command Startup

```bash
pip install -r requirements.txt && uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Review a Diff

```http
POST /review
```

Request:

```json
{
  "diff": "<git diff>",
  "language": "python",
  "context": "PR review"
}
```

---

## Get Review by ID

```http
GET /review/{review_id}
```

---

## List Reviews

```http
GET /reviews
```

---

## Health Check

```http
GET /health
```

---

# Batch Review Generation

Generate review reports using:

```bash
python run_reviews.py
```

The script:

1. Reads the provided diff files locally
2. Sends each diff to the `/review` endpoint
3. Saves generated review reports to the `reviews/` directory

Generated outputs:

```text
reviews/diff1_review.json
reviews/diff2_review.json
reviews/diff3_review.json
```

---

# Output Schema

Each generated review follows the `ReviewReport` schema.

```json
{
  "pr_summary": "string",
  "verdict": "approve | request_changes | needs_discussion",
  "verdict_reason": "string",
  "overall_severity": "clean | low | medium | high | critical",
  "findings": [
    {
      "id": "F-001",
      "line": 42,
      "line_content": "string",
      "category": "security | performance | correctness | style | test_coverage",
      "severity": "critical | high | medium | low",
      "title": "string",
      "description": "string",
      "suggestion": "string"
    }
  ],
  "positive_observations": [
    "string"
  ],
  "missing_tests": [
    "string"
  ],
  "agent_findings_count": {
    "security": 0,
    "performance": 0,
    "correctness": 0,
    "style": 0,
    "test_coverage": 0
  },
  "processing_time_ms": 0
}
```

Review categories:

* Security
* Performance
* Correctness
* Style
* Test Coverage

---

# Example Workflow

1. Submit a git diff to `POST /review`
2. LangGraph dispatches the diff to all reviewer agents
3. Each reviewer generates findings for its category
4. Findings are aggregated and merged
5. The final report is validated using Pydantic schemas
6. The review is persisted to storage
7. A structured review report is returned to the client

---

# Design Decisions

## Most Happy With

### Multi-Agent Architecture

Instead of relying on a single prompt, the system uses specialized reviewer agents. This improves separation of concerns and allows each reviewer to focus on a specific aspect of code quality.

### Structured Output Schema

All findings are validated using Pydantic models, ensuring consistent and machine-readable review reports.

### LangGraph Orchestration

LangGraph provides a clean workflow for dispatching review tasks, collecting outputs, and generating a unified review report.

### Reviewer Isolation

Each reviewer focuses exclusively on one review category, reducing overlap and improving review quality.

---

## Areas for Future Improvement

### Repository-Aware Analysis

The current implementation intentionally reviews only the supplied diff. A future enhancement would incorporate repository-wide context to improve analysis of authorization flows, shared utilities, existing validation patterns, and architectural constraints.

### Cross-Agent Context Sharing

Reviewer agents currently operate independently and are merged afterwards. Future versions could allow agents to exchange contextual signals before generating findings, improving consistency and reducing duplicate observations.

### Expanded Language Support

The architecture is language-agnostic. Additional language-specific review rules and prompts could further improve review quality across a wider range of programming languages.

---

# Future Enhancements

* Repository-wide contextual analysis
* Pull request comment generation
* Additional programming language support
* Incremental review of changed files only
* Cross-agent reasoning and finding deduplication
* Reviewer confidence scoring
* Historical review analytics
* Reviewer benchmarking against human reviews

---

# Environment Variables

| Variable     | Description  |
| ------------ | ------------ |
| GROQ_API_KEY | Groq API key |

---

# Technologies Used

* Python
* FastAPI
* LangGraph
* Groq
* Pydantic
* Uvicorn
