from typing import TypedDict, Optional


class AgentState(TypedDict):
    job_title: str
    raw_job_data: Optional[str]
    required_skills: Optional[dict]
    candidate_profile: Optional[str]
    gap_analysis: Optional[dict]
    final_report: Optional[str]
    error: Optional[str]
