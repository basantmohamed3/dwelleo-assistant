# Dwelleo RAG Support Assistant

## Overview

Dwelleo RAG Support Assistant is a Retrieval-Augmented Generation (RAG) based AI support system designed for a real estate SaaS platform operating in KSA and UAE.

The system combines:

* Semantic retrieval from a knowledge base
* LLM-powered answer generation
* Intent classification
* Prompt injection protection
* Automatic ticket escalation

The assistant answers platform-related questions such as:

* Pricing and subscriptions
* Platform features
* Supported regions
* Account and usage support
* Listings and real estate platform guidance

---

# Architecture

The system follows a layered architecture:

```text
User Question
      ↓
Intent Classification Layer
      ↓
Safety & Scope Validation
      ↓
RAG Retrieval Layer
      ↓
Context Formatting
      ↓
LLM Answer Generation
      ↓
Fallback / Ticket Escalation
      ↓
Final JSON Response
```

---

# Project Structure

```text
dwelleo1/
├── app/
│   ├── __init__.py
│   ├── agent.py            # Main RAG pipeline, async handlers, post-LLM guardrails
│   ├── prompts.py          # Strict guardrailed system & intent classification prompts
│   ├── rag.py              # Vector DB loading and retriever configuration
│   └── main.py             # Async FastAPI web server endpoints
├── knowledge_base/         # Raw Markdown source documentation files
├── pyproject.toml          # PEP 621 compliant environment configuration for uv
├── requirements.txt        # Legacy standard requirements manifest
├── evaluate.py             # Automated evaluation test suite
└── evaluation_results.json # Serialized evaluation logs and matrix status
```

---

# Core Components

## 1. Intent Classification Layer

The system uses an LLM-based semantic router instead of hardcoded keyword matching.

It classifies user queries into:

| Intent       | Description                                      |
| ------------ | ------------------------------------------------ |
| normal       | Valid Dwelleo platform-related question          |
| out_of_scope | Unrelated topics such as sports, crypto, weather |
| attack       | Prompt injection or jailbreak attempt            |

### Why LLM Routing?

Initially, the system used keyword-based routing:

```python
keywords = ["weather", "crypto", "sports"]
```

This approach was brittle and difficult to scale.

The system was upgraded to semantic classification using GPT-based routing to:

* Improve generalization
* Reduce false positives
* Handle natural language variations
* Remove hardcoded dependency maintenance

---

## 2. Retrieval-Augmented Generation (RAG)

The assistant retrieves relevant information from the internal knowledge base before generating responses.

### Flow

```text
Question → Vector Search → Relevant Chunks → LLM Context
```

### Knowledge Base

The knowledge base is stored as Markdown files.

Examples:

```text
knowledge_base/
├── pricing.md
├── subscriptions.md
├── supported_regions.md
├── refund_policy.md
```

---

## 3. Context Formatting

Retrieved documents are transformed into structured context before being sent to the LLM.

Example:

```text
Source: supported_regions.md
Dwelleo currently supports UAE, KSA, and Qatar.
```

This helps ground the model response in retrieved knowledge.

---

## 4. LLM Answer Generation

The system uses LangChain with OpenAI chat models.

Responsibilities of the LLM:

* Read retrieved context
* Generate grounded answers
* Follow support assistant behavior
* Avoid hallucinations

The LLM is intentionally separated from:

* Safety logic
* Ticketing
* Business rules

This keeps the architecture modular and deterministic.

---

## 5. Ticket Escalation System

If no relevant context is found:

* The system avoids hallucinating
* A support ticket is created automatically
* The user receives a controlled fallback response

Example ticket:

```json
{
  "ticket_id": "DWL-ABCD1234",
  "status": "open",
  "issue": "Do you support Egypt?",
  "reason": "No relevant match found"
}
```

---

# Safety & Guardrails

The assistant includes a lightweight LLM guard layer.

## Protection Areas

### Prompt Injection Detection

Examples:

* Ignore previous instructions
* Reveal system prompt
* Act as another assistant
* Jailbreak attempts

### Out-of-Scope Protection

Blocks unrelated topics such as:

* Sports
* Weather
* Cryptocurrency
* General knowledge

---

# Example API Response

```json
{
  "question": "Do you support UAE?",
  "answer": "Yes, Dwelleo supports UAE.",
  "sources": [
    "knowledge_base/supported_regions.md"
  ],
  "ticket": null,
  "intent": "normal"
}
```

---

# Evaluation Framework

The project includes an evaluation script to validate:

* Correct answering behavior
* Out-of-scope handling
* Ticket creation
* Injection handling

Example test categories:

| Category        | Example                      |
| --------------- | ---------------------------- |
| Pricing         | Professional plan cost       |
| Support Regions | Do you support Qatar?        |
| Out of Scope    | Weather in Dubai             |
| Injection       | Ignore previous instructions |

---

# Key Technical Challenges

## 1. RAG Retrieval vs Generation Mismatch

One of the main issues encountered was:

* Correct documents were retrieved
* But the LLM still generated generic fallback responses

### Root Causes

* Weak chunk retrieval
* Overly restrictive prompts
* Missing context validation
* Poor retrieval granularity

### Fixes Implemented

* Improved prompt structure
* Added deterministic fallback logic
* Simplified system instructions
* Refined intent routing

---

## 2. Hardcoded Intent Classification Limitations

The initial version relied on keyword matching.

Example:

```python
if "weather" in text:
```

Problems:

* Difficult to scale
* Easy to bypass
* High false positives
* Weak semantic understanding

The solution was migrating to LLM-based semantic routing.

---

# Technologies Used

| Technology       | Purpose            |
| ---------------- | ------------------ |
| Python           | Backend logic      |
| LangChain        | LLM orchestration  |
| OpenAI API       | Language model     |
| ChromaDB         | Vector database    |
| Markdown KB      | Knowledge storage  |
| RAG Architecture | Grounded responses |

---

# Future Improvements

Potential production-level enhancements:

* Hybrid retrieval (keyword + semantic)
* Reranking layer
* Hallucination detection
* caching
* Confidence scoring
* Streaming responses
* Persistent ticket storage
* Multi-intent routing
* Evaluation dashboard

---

# Installation
uv sync

Create a .env file containing: OPENAI_API_KEY=your_api_key

uv run uvicorn app.main:app --reload

uv run python -m app.evaluate

# Deliverables

## Repository Contents

The repository includes:

* Source code for the Dwelleo RAG Support Assistant
* Knowledge base files
* Evaluation framework
* README documentation
* Evaluation output JSON

---



---



---

### 3. Evaluation Output

// FINAL METRIC SUMMARY
Total Test Cases Run : 10
Successful Passes    : 10/10
Tickets Generated    : 1
System Accuracy Rate : 100.0%

Run:

```bash
python evaluation.py
```

This generates:

```text
evaluation_results.json
```

The output contains:

* Test questions
* Expected behavior
* Actual responses
* Pass/fail status
* Ticket creation results

---

## Short Project Update Summary

### What I Built

I built a RAG-based AI support assistant for a real estate SaaS platform. The system combines semantic retrieval, LLM-based answer generation, intent classification, safety guardrails, and automatic ticket escalation.

The assistant can:

* Answer platform-related questions
* Retrieve information from a knowledge base
* Detect out-of-scope or malicious requests
* Escalate unanswered queries into support tickets

---

### One Decision I’m Proud Of

One key improvement was replacing hardcoded keyword-based intent classification with an LLM-based semantic router.

This significantly improved:

* Generalization
* Natural language understanding
* Scalability
* Handling of edge-case phrasing

It also reduced maintenance complexity compared to manually updating keyword lists.

---

### One Thing I’d Improve With More Time

Given more time, I would improve retrieval quality and evaluation depth by adding:

* Hybrid retrieval (semantic + keyword)
* Caching layer
* Presitent ticket storage (CRM, DB)

---

