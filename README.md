# Multi-Agent AI System for Intelligent Resume Parsing & Skill Matching

An industrial-grade, agentic AI pipeline designed for global talent acquisition. This system leverages a multi-agent orchestration layer to handle high-speed resume parsing, hierarchical skill normalization, and semantic vector matching with 95% correlation to expert rankings.

## 🚀 Mission Capabilities

*   **Neural Parsing (PRSE_01):** Agentic extraction from PDF/DOCX formats with structural layout preservation and layout-aware text analysis.
*   **Taxonomy Engine (NORM_02):** A hierarchical database of 5,600+ unique skills with vector normalization for high-precision alignment.
*   **Vector Matcher (MTCH_03):** Semantic similarity scoring using deep context matching between candidate profiles and job descriptions.
*   **AI Interview Protocol:** Automated generation of targeted interview questions and strategic rationales based on identified skill gaps.

## 🛠️ Operational Stack

*   **Agent Orchestration:** [LangGraph](https://github.com/langchain-ai/langgraph) (State machines for error-tolerant execution)
*   **LLM Infrastructure:** Groq (Llama 3.3 / 3.1) for high-density reasoning (Transitioned from OpenAI for 10x faster inference)
*   **Vector Core:** Sentence-Transformers for semantic embeddings
*   **Backend:** FastAPI (Python 3.10+)
*   **Frontend:** React (Single-file optimized dashboard)
*   **Database:** ChromaDB (Vector store for taxonomy and candidate profiles)

## 📂 System Architecture

```text
├── app/
│   ├── agents/          # Agentic logic (Parser, Matcher, Normalizer, etc.)
│   ├── api/             # RESTful API Endpoints (v1)
│   ├── core/            # System configuration & security
│   ├── models/          # Domain & API schemas
│   └── utils/           # Neural extraction & file utilities
├── data/
│   ├── samples/         # Ground truth datasets & sample resumes
│   └── taxonomy/        # Hierarchical skill matrix (5.6k+ entries)
├── frontend/
│   └── public/          # High-fidelity dashboard
└── scripts/             # System validation & evaluation tools
```

## ⚡ Quick Start

### 1. Environment Setup
Create a `.env` file in the root directory:
```bash
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_secret_key
USE_MOCK_PARSER=False
```

### 2. Initialization
Run the one-click demo loader to start both backend and frontend:
```bash
python scripts/run_demo.py
```

*   **Dashboard:** `http://localhost:3001`
*   **API Docs:** `http://localhost:8000/docs`

## 📊 Evaluation & Validation
The system includes a rigorous validation suite to ensure parsing accuracy and matching precision:
```bash
python scripts/validate_system.py
```

---
**System_Status:** `OPERATIONAL` // **Version:** `1.0.4`
