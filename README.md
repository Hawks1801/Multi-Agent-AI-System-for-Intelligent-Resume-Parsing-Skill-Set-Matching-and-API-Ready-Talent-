# Multi-Agent Resume Intelligence System 🚀

An advanced AI-powered talent intelligence platform designed for hackathons. This system intelligently parses resumes, normalizes skills against a hierarchical taxonomy, and performs semantic matching against job descriptions using a multi-agent architecture.

## ✨ Key Features
- **Multi-Agent Orchestration:** Uses **LangGraph** to manage specialized agents for Parsing, Normalization, and Matching.
- **Intelligent Parsing:** Extracts structured data from PDF, DOCX, and Text using layout analysis and **LLM-structured extraction (via `instructor`)**.
- **Skill Normalization:** Maps messy resume skills (e.g., 'K8s', 'ReactJS') to a canonical taxonomy using **Semantic Search (ChromaDB)**.
- **Semantic Matching:** Calculates deep compatibility scores between candidate profiles and job descriptions using **Sentence-Transformers**.
- **Production-Ready API:** Built with **FastAPI**, fully documented with Swagger/OpenAPI.
- **Deployment Ready:** Fully containerized with **Docker** and **Docker Compose**.

## 🛠 Tech Stack
- **Frameworks:** FastAPI, LangGraph, Pydantic, SQLModel.
- **AI/ML:** OpenAI (GPT-4o), Sentence-Transformers, ChromaDB.
- **Parsing:** pdfplumber, python-docx.
- **Infrastructure:** PostgreSQL, Redis, Docker.

## 🚀 Getting Started

### 1. Prerequisites
- Docker & Docker Compose
- OpenAI API Key

### 2. Setup
1. Clone the repository.
2. Create a `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   # Add your OPENAI_API_KEY
   ```

### 3. Run with Docker
```bash
docker-compose up --build
```
The API will be available at `http://localhost:8000`.
Explore the docs at `http://localhost:8000/docs`.

### 4. Local Validation (Development)
You can run the validation script to see the system in action:
```bash
pip install -r requirements.txt
python scripts/validate_system.py
```

## 🏗 System Architecture
1. **ParserAgent:** PDF/DOCX -> Raw Text -> Structured JSON.
2. **NormalizerAgent:** Structured JSON -> Taxonomy-mapped Skills.
3. **MatcherAgent:** Normalized Skills vs Job Description -> Match Score & Gap Analysis.
4. **Orchestrator (LangGraph):** Manages the flow and state between agents.

## 📊 Evaluation Metrics
- **Parsing Accuracy:** High-fidelity extraction of contact info, experience, and education.
- **Normalization Quality:** Efficient mapping of abbreviations and synonyms to canonical entries.
- **Latency:** Optimized pipeline designed to process resumes in < 10 seconds.
