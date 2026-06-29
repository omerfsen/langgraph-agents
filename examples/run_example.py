import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv

load_dotenv()

from src.agent import app

if __name__ == "__main__":
    job_title = sys.argv[1] if len(sys.argv) > 1 else "AI Engineer"

    print(f"\n{'='*60}")
    print(f"  Job Research Agent: {job_title}")
    print(f"{'='*60}\n")

    initial_state = {
        "job_title": job_title,
        "raw_job_data": None,
        "required_skills": None,
        "candidate_profile": None,
        "gap_analysis": None,
        "final_report": None,
        "error": None,
    }

    print("Running agent graph...\n")
    for step, state in enumerate(app.stream(initial_state), 1):
        node_name = list(state.keys())[0]
        print(f"[Step {step}] Completed: {node_name}")

    final_state = state[node_name]
    print(f"\n{'='*60}")
    print("  GAP ANALYSIS REPORT")
    print(f"{'='*60}\n")
    print(final_state.get("final_report", "No report generated."))
    print(f"\n{'='*60}\n")
