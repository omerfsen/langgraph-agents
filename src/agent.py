from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes import (
    fetch_job_requirements,
    extract_skills,
    load_candidate_profile,
    run_gap_analysis,
    generate_report,
)


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("fetch_job_requirements", fetch_job_requirements)
    graph.add_node("extract_skills", extract_skills)
    graph.add_node("load_candidate_profile", load_candidate_profile)
    graph.add_node("gap_analysis", run_gap_analysis)
    graph.add_node("generate_report", generate_report)

    graph.set_entry_point("fetch_job_requirements")
    graph.add_edge("fetch_job_requirements", "extract_skills")
    graph.add_edge("extract_skills", "load_candidate_profile")
    graph.add_edge("load_candidate_profile", "gap_analysis")
    graph.add_edge("gap_analysis", "generate_report")
    graph.add_edge("generate_report", END)

    return graph.compile()


app = build_graph()
