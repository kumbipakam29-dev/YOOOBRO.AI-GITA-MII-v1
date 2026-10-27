"""Schema validation for the hard-task catalog; checks definitions, not solutions."""
import argparse, json
from pathlib import Path

REQUIRED = ("task_id","domain","challenge","required_verifier","execution_class","status","safety_boundary")
ALLOWED_STATUS = {"PLANNED_NOT_RUN","SIMULATION","REAL_RUNNER_EXECUTION","EXTERNAL_BENCHMARK","HUMAN_REVIEW","BLOCKED_RESOURCE","VERIFIED_SOLVED"}
ALLOWED_CLASSES = {"local_sandbox","custom_dataset","human_review","external_data_review","external_tool_required","external_benchmark_or_custom_sandbox","external_model_access_required"}

def validate(path="experiments/miilab_hard_tasks_v1.jsonl"):
    rows=[json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows)<30: raise ValueError(f"Expected at least 30 tasks; got {len(rows)}")
    ids=[x.get("task_id") for x in rows]
    if any(not isinstance(x,str) or not x for x in ids) or len(set(ids))!=len(ids):
        raise ValueError("Task IDs must be nonempty and unique")
    for row in rows:
        missing=[key for key in REQUIRED if not row.get(key)]
        if missing: raise ValueError(f"{row.get('task_id')}: missing {missing}")
        if row["status"] not in ALLOWED_STATUS: raise ValueError(f"{row['task_id']}: bad status")
        if row["execution_class"] not in ALLOWED_CLASSES: raise ValueError(f"{row['task_id']}: bad execution class")
        if row["status"]=="VERIFIED_SOLVED" and not (row.get("verifier_run_id") and row.get("evidence_uri")):
            raise ValueError(f"{row['task_id']}: verified solved requires run ID and evidence URI")
    domains=sorted({row["domain"] for row in rows})
    return {"status":"PASS","task_count":len(rows),"unique_task_ids":len(set(ids)),"domain_count":len(domains),"domains":domains,
            "all_initially_planned":all(x["status"]=="PLANNED_NOT_RUN" for x in rows)}
def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--path",default="experiments/miilab_hard_tasks_v1.jsonl")
    print(json.dumps(validate(parser.parse_args().path),ensure_ascii=False,indent=2))
if __name__=="__main__": main()
