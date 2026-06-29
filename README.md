# LangGraph Agents — AI Job Research Assistant

A multi-agent pipeline built with [LangGraph](https://github.com/langchain-ai/langgraph) that researches a job title, extracts required skills, and produces a personalised gap analysis report against a candidate profile.

Built as a portfolio project demonstrating LangGraph state graph orchestration with Claude as the LLM backbone.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph StateGraph                     │
│                                                             │
│  ┌─────────────────┐     ┌──────────────────┐              │
│  │ fetch_job_reqs  │────▶│  extract_skills  │              │
│  └─────────────────┘     └──────────────────┘              │
│                                   │                         │
│                                   ▼                         │
│  ┌─────────────────┐     ┌──────────────────┐              │
│  │ generate_report │◀────│  gap_analysis    │              │
│  └─────────────────┘     └──────────────────┘              │
│           │                       ▲                         │
│           │               ┌───────────────┐                 │
│           │               │ load_profile  │                 │
│           │               └───────────────┘                 │
│           ▼                                                 │
│          END                                                │
└─────────────────────────────────────────────────────────────┘
```

## Graph Nodes

| Node | Responsibility |
|------|---------------|
| `fetch_job_requirements` | Uses Claude to generate realistic job requirements for the given title |
| `extract_skills` | Parses requirements into structured JSON (technical, soft, certs) |
| `load_candidate_profile` | Loads candidate profile from state (or uses default) |
| `gap_analysis` | Claude compares required skills vs profile → has/missing/partial |
| `generate_report` | Claude writes a markdown gap analysis report with recommendations |

## Shared State

```python
class AgentState(TypedDict):
    job_title: str
    raw_job_data: Optional[str]
    required_skills: Optional[dict]
    candidate_profile: Optional[str]
    gap_analysis: Optional[dict]
    final_report: Optional[str]
    error: Optional[str]
```

## Quick Start

```bash
git clone https://github.com/omerfsen/langgraph-agents
cd langgraph-agents

cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

pip install -r requirements.txt

python examples/run_example.py "AI Engineer"
python examples/run_example.py "Senior MLOps Engineer"
```

## Docker

```bash
docker pull omerfsen/langgraph-agents:latest

docker run --rm \
  -e ANTHROPIC_API_KEY=your_key_here \
  omerfsen/langgraph-agents:latest

# Custom job title
docker run --rm \
  -e ANTHROPIC_API_KEY=your_key_here \
  omerfsen/langgraph-agents:latest \
  python examples/run_example.py "LLMOps Engineer"
```

## Sample Output

```
==============================
  Job Research Agent: AI Engineer
==============================

[Step 1] Completed: fetch_job_requirements
[Step 2] Completed: extract_skills
[Step 3] Completed: load_candidate_profile
[Step 4] Completed: gap_analysis
[Step 5] Completed: generate_report

==============================
  GAP ANALYSIS REPORT
==============================

## Executive Summary
Strong infrastructure background with 85% skill match for AI Engineer roles...

## Strengths
- ✅ GPU infrastructure at scale (B200/H100 clusters)
- ✅ Kubernetes, Docker, Helm, Terraform
...
```

## Tech Stack

- **[LangGraph](https://github.com/langchain-ai/langgraph)** — agent graph orchestration
- **[Anthropic Claude](https://www.anthropic.com)** (claude-sonnet-4-6) — LLM for all reasoning nodes
- **Python 3.11+**

## Related Articles

- [MLOps vs LLMOps: Why Large Language Models Force Us to Rethink Production AI](https://www.linkedin.com/pulse/mlops-vs-llmops-why-large-language-models-force-us-rethink-omer-sen-xudge/)
- [Build a RAG Pipeline Using Azure AI Search and Azure OpenAI with Terraform](https://www.linkedin.com/pulse/build-rag-pipeline-using-azure-ai-search-openai-terraform-3amqe)

## Author

[Omer Sen](https://www.linkedin.com/in/omerfsen/) — Principal Consultant | DevOps · DevSecOps · MLOps · LLMOps
