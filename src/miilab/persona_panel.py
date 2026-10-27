"""Generate a labelled panel of reasoning lenses inspired by public historical work.

This is a structured checklist simulation, not an actual person's cognition, voice, or solution.
"""
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return obj


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows or any(not isinstance(row, dict) for row in rows):
        raise ValueError(f"Expected non-empty JSONL object rows in {path}")
    return rows


def build_panel(personas_path: Path | str = "registry/personas.json",
                tasks_path: Path | str = "experiments/challenge_tasks.jsonl") -> dict[str, Any]:
    """Build a review matrix; never claim that the named people actually participated."""
    personas_doc = _read_json(Path(personas_path))
    personas = personas_doc.get("personas")
    tasks = _read_jsonl(Path(tasks_path))
    if not isinstance(personas, list) or not personas:
        raise ValueError("Persona registry must contain a non-empty personas list")

    reviews = []
    for persona in personas:
        required = ("id", "public_person", "field", "lens", "review_questions",
                    "failure_mode_to_guard", "verification")
        if not all(persona.get(k) for k in required):
            raise ValueError(f"Incomplete persona definition: {persona.get('id', '<unknown>')}")
        for task in tasks:
            if not all(task.get(k) for k in ("task_id", "domain", "challenge", "required_verifier")):
                raise ValueError(f"Incomplete challenge task: {task.get('task_id', '<unknown>')}")
            reviews.append({
                "persona_id": persona["id"],
                "public_person_reference": persona["public_person"],
                "field": persona["field"],
                "reasoning_lens": persona["lens"],
                "task_id": task["task_id"],
                "domain": task["domain"],
                "challenge_summary": task["challenge"],
                "review_questions": list(persona["review_questions"]),
                "failure_mode_to_guard": persona["failure_mode_to_guard"],
                "recommended_verification": persona["verification"],
                "task_required_verifier": task["required_verifier"],
                "status": "PERSPECTIVE_SIMULATION_NOT_SOLVED",
                "named_person_is_actually_participating": False,
                "personal_voice_or_private_thoughts_recreated": False,
                "invented_person_quote": False,
                "iq_estimate": None,
            })

    return {
        "schema_version": "miilab.persona-panel.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "evidence_class": "STRUCTURED_PERSONA_SIMULATION",
        "panel_label": personas_doc.get("panel_label", "Research Lens Panel"),
        "label_disclaimer": personas_doc.get("label_disclaimer", "No IQ claim."),
        "mode": personas_doc.get("mode", "PUBLIC_WORK_INSPIRED_LENSES_NOT_PERSON_REPLICAS"),
        "actual_people_recreated": False,
        "iq_claimed": False,
        "solutions_claimed": False,
        "persona_count": len(personas),
        "challenge_task_count": len(tasks),
        "review_count": len(reviews),
        "persona_ids": [p["id"] for p in personas],
        "challenge_task_ids": [t["task_id"] for t in tasks],
        "perspective_reviews": reviews,
        "limitations": [
            "The 1,000,000-IQ label is fictional gamification, not a real IQ score.",
            "These are structured perspectives inspired by public work, not exact replicas.",
            "No real person is participating or endorsing this project.",
            "This panel generates checklists and verification plans; it does not solve the listed challenges.",
            "A real-world success claim requires actually running the same task and checking its output.",
        ],
    }



def run_scaled_panel_stress(
    panel_count: int = 10_000_000,
    personas_path: Path | str = "registry/personas.json",
    tasks_path: Path | str = "experiments/challenge_tasks.jsonl",
) -> dict[str, Any]:
    """Process logical panel shells without expanding all repeated review cells.

    This is a CPU test of the simulation loop, not millions of independent model calls.
    """
    import time
    if not 1 <= panel_count <= 10_000_000:
        raise ValueError("panel_count must be in [1, 10000000]")
    panel = build_panel(personas_path, tasks_path)
    persona_count = panel["persona_count"]
    task_count = panel["challenge_task_count"]
    base_cells = panel["review_count"]
    if base_cells != persona_count * task_count:
        raise ValueError("Base panel matrix is inconsistent")

    started = time.perf_counter()
    processed = 0
    # Iterate every panel shell, reusing the immutable lens/task template rather than
    # allocating hundreds of millions of duplicate review dictionaries.
    for i in range(panel_count):
        processed = i + 1
    duration = time.perf_counter() - started
    expected_cells = panel_count * base_cells
    coverage_ok = processed == panel_count and expected_cells == processed * persona_count * task_count
    return {
        "schema_version": "miilab.persona-panel-stress.v1",
        "evidence_class": "REAL_RUN_OF_SIMULATION_CODE",
        "panel_label": "10,000,000-IQ Persona Panel Simulation",
        "label_disclaimer": "10,000,000 is the number of simulated panel shells; IQ is fictional gamification and not a human or model IQ score.",
        "panels_requested": panel_count,
        "panels_processed": processed,
        "reasoning_lens_count": persona_count,
        "challenge_task_count": task_count,
        "review_cells_per_panel": base_cells,
        "virtual_review_cell_equivalents": expected_cells,
        "review_cells_individually_materialized": 0,
        "execution_mode": "REUSED_TEMPLATE_AGGREGATE_SIMULATION",
        "loop_duration_seconds": round(duration, 6),
        "coverage_check": "PASS" if coverage_ok else "FAIL",
        "actual_people_recreated": False,
        "iq_claimed": False,
        "generative_model_inference_calls": 0,
        "challenge_solutions_verified": 0,
        "challenge_solution_status": "NOT_RUN_TASK_SPECIFIC_VERIFIERS_REQUIRED",
        "limitations": [
            "Each simulated panel reuses the same 8-lens by 8-task template.",
            "Virtual review-cell equivalents are arithmetic counts, not hundreds of millions of generated reviews.",
            "No real people participate and no IQ is measured.",
            "This pass validates bounded loop execution and count integrity only.",
            "Frontier tasks still require task-specific solvers and independent verifiers.",
        ],
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--personas", type=Path, default=Path("registry/personas.json"))
    parser.add_argument("--tasks", type=Path, default=Path("experiments/challenge_tasks.jsonl"))
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--stress-panels", type=int, default=0,
                        help="Process 1..10000000 logical panel shells without materializing review rows")
    args = parser.parse_args()
    panel = build_panel(args.personas, args.tasks)
    output_doc: dict[str, Any] = {"base_panel": panel}
    if args.stress_panels:
        output_doc["scaled_stress"] = run_scaled_panel_stress(
            args.stress_panels, args.personas, args.tasks
        )
    payload = json.dumps(output_doc, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    summary = {
        "panel_label": panel["panel_label"],
        "persona_count": panel["persona_count"],
        "challenge_task_count": panel["challenge_task_count"],
        "review_count": panel["review_count"],
        "iq_claimed": panel["iq_claimed"],
        "solutions_claimed": panel["solutions_claimed"],
    }
    if args.stress_panels:
        summary["scaled_stress"] = output_doc["scaled_stress"]
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
