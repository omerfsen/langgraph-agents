import json
import os
from anthropic import Anthropic
from src.state import AgentState

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-6"


def fetch_job_requirements(state: AgentState) -> AgentState:
    """Node 1: Generate realistic job requirements for the given job title."""
    prompt = f"""You are a senior technical recruiter. Generate a realistic and detailed job requirements specification for the role: "{state['job_title']}".

Include:
- 5-8 must-have technical skills
- 3-5 nice-to-have skills
- 2-3 soft skills
- Any certifications commonly required
- Typical years of experience required
- Brief role summary (2-3 sentences)

Respond as plain text, structured clearly."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return {**state, "raw_job_data": response.content[0].text}


def extract_skills(state: AgentState) -> AgentState:
    """Node 2: Parse raw job data into a structured skills list."""
    prompt = f"""Extract all skills from this job description and return them as JSON.

Job description:
{state['raw_job_data']}

Return ONLY valid JSON in this exact format:
{{
  "technical_skills": ["skill1", "skill2"],
  "nice_to_have": ["skill1", "skill2"],
  "soft_skills": ["skill1", "skill2"],
  "certifications": ["cert1"],
  "years_experience": 5
}}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    required_skills = json.loads(text.strip())
    return {**state, "required_skills": required_skills}


def load_candidate_profile(state: AgentState) -> AgentState:
    """Node 3: Load the candidate profile (passed via state or use default)."""
    if state.get("candidate_profile"):
        return state

    default_profile = """
    Omer Sen — Principal Consultant | DevOps, DevSecOps, MLOps, LLMOps

    Skills: Python, Kubernetes, Docker, Helm, Terraform, Azure (AKS), AWS (EKS),
    HashiCorp Vault, GitLab CI/CD, Prometheus, Grafana, vLLM, KServe,
    GPU infrastructure (NVIDIA B200/H100), RAG pipelines, Azure AI Search,
    LangChain, Claude API, OpenAI API, Linux, NGINX, Redis, PostgreSQL.

    Experience: 25 years in infrastructure and platform engineering.
    Certifications: Multiple AWS and Azure certifications.
    Published articles on GPU Kubernetes, RAG pipelines, MLOps vs LLMOps.
    """
    return {**state, "candidate_profile": default_profile.strip()}


def run_gap_analysis(state: AgentState) -> AgentState:
    """Node 4: Compare required skills against candidate profile."""
    prompt = f"""Compare the required job skills against the candidate profile and classify each skill.

Required skills:
{json.dumps(state['required_skills'], indent=2)}

Candidate profile:
{state['candidate_profile']}

Return ONLY valid JSON in this exact format:
{{
  "has_skill": ["skill1", "skill2"],
  "missing_skill": ["skill1", "skill2"],
  "partial_skill": ["skill1 (needs: specific area)"],
  "match_percentage": 75
}}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    gap_analysis = json.loads(text.strip())
    return {**state, "gap_analysis": gap_analysis}


def generate_report(state: AgentState) -> AgentState:
    """Node 5: Generate a markdown gap analysis report."""
    prompt = f"""Write a concise, actionable gap analysis report in markdown for a candidate applying to: "{state['job_title']}".

Gap analysis data:
{json.dumps(state['gap_analysis'], indent=2)}

Required skills context:
{json.dumps(state['required_skills'], indent=2)}

Structure the report with:
1. Executive Summary (2-3 sentences)
2. Strengths (bullet list of confirmed skills)
3. Gaps to Address (bullet list with priority: High/Medium/Low)
4. Recommended Actions (3-5 concrete next steps)
5. Overall Match Score

Be direct and specific. No fluff."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return {**state, "final_report": response.content[0].text}
