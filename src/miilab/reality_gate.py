"""Compare declared simulation predictions with safe tasks actually run on a GitHub runner.

This executes bounded local checks only. It does not contact production systems,
download model weights, spend money, access external accounts, or provision GPUs/TPUs.
"""
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from miilab.trainer import predict, read_rows, train
from miilab.simulation import PROFILES, simulate

PROFILE_NAMES = list(PROFILES)

# Explicit assumptions used by the virtual simulator; not learned predictions.
SIMULATED_TASKS = {
    "dataset_validation": {
        "description": "Parse and validate the checked-in synthetic dataset",
        "simulated_success_profiles": PROFILE_NAMES,
        "real_runner_safe": True,
    },
    "tiny_classifier_training": {
        "description": "Train and serialize the small Naive Bayes baseline",
        "simulated_success_profiles": PROFILE_NAMES,
        "real_runner_safe": True,
    },
    "python_source_compile": {
        "description": "Compile repository Python sources",
        "simulated_success_profiles": PROFILE_NAMES,
        "real_runner_safe": True,
    },
    "accelerator_probe": {
        "description": "Probe this runner for a detectable GPU/TPU accelerator",
        "simulated_success_profiles": [
            "gpu_virtual", "tpu_virtual", "server_virtual", "infinity_space_server"
        ],
        "real_runner_safe": True,
    },
    "large_llm_finetune": {
        "description": "Fine-tune a large foundation model",
        "simulated_success_profiles": ["infinity_space_server"],
        "real_runner_safe": False,
    },
}

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def run_real_tasks(root):
    """Execute bounded tasks on this actual CI runner and capture explicit statuses."""
    results = {}
    data_path = root / "datasets" / "principle_intents.jsonl"

    started = time.perf_counter()
    try:
        rows = read_rows(data_path)
        labels = sorted({row["label"] for row in rows})
        results["dataset_validation"] = {
            "status": "PASS", "rows": len(rows), "labels": labels,
            "dataset_sha256": sha256_bytes(data_path.read_bytes()),
            "duration_seconds": round(time.perf_counter() - started, 6),
        }
    except Exception as exc:
        results["dataset_validation"] = {
            "status": "FAIL", "error_type": type(exc).__name__,
            "error": str(exc), "duration_seconds": round(time.perf_counter() - started, 6),
        }
        rows = []

    started = time.perf_counter()
    try:
        if not rows:
            raise RuntimeError("Training blocked because dataset validation failed")
        model = train(rows)
        predictions = [predict(model, row["text"]) for row in rows]
        correct = sum(pred == row["label"] for pred, row in zip(predictions, rows))
        encoded = (json.dumps(model, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        with tempfile.TemporaryDirectory(prefix="mii-reality-gate-") as temp_dir:
            artifact = Path(temp_dir) / "tiny_classifier.json"
            artifact.write_bytes(encoded)
            reloaded = json.loads(artifact.read_text(encoding="utf-8"))
            round_trip = all(predict(reloaded, row["text"]) == row["label"] for row in rows)
            artifact_hash = sha256_bytes(artifact.read_bytes())
        results["tiny_classifier_training"] = {
            "status": "PASS" if round_trip and len(encoded) > 0 else "FAIL",
            "algorithm": model["algorithm"],
            "is_generative_llm": False,
            "training_rows": len(rows),
            "training_example_accuracy": round(correct / len(rows), 6) if rows else None,
            "training_accuracy_warning": "Training-set metric only; not held-out generalization.",
            "artifact_round_trip": round_trip,
            "temporary_artifact_sha256": artifact_hash,
            "duration_seconds": round(time.perf_counter() - started, 6),
        }
    except Exception as exc:
        results["tiny_classifier_training"] = {
            "status": "FAIL", "error_type": type(exc).__name__,
            "error": str(exc), "duration_seconds": round(time.perf_counter() - started, 6),
        }

    started = time.perf_counter()
    try:
        py_files = sorted((root / "src").rglob("*.py")) + sorted((root / "tests").rglob("*.py"))
        for path in py_files:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        results["python_source_compile"] = {
            "status": "PASS", "files_compiled": len(py_files),
            "duration_seconds": round(time.perf_counter() - started, 6),
        }
    except Exception as exc:
        results["python_source_compile"] = {
            "status": "FAIL", "error_type": type(exc).__name__,
            "error": str(exc), "duration_seconds": round(time.perf_counter() - started, 6),
        }

    # Conservative capability probe: absence means NOT_DETECTED, not proof that the
    # underlying host infrastructure has no accelerator.
    nvidia_smi = shutil.which("nvidia-smi")
    device_paths = ["/dev/nvidia0", "/dev/kfd"]
    detected_paths = [p for p in device_paths if Path(p).exists()]
    gpu_command_ok = False
    if nvidia_smi:
        try:
            probe = subprocess.run(
                [nvidia_smi, "-L"], capture_output=True, text=True,
                timeout=3, check=False,
            )
            gpu_command_ok = probe.returncode == 0 and bool(probe.stdout.strip())
        except (OSError, subprocess.TimeoutExpired):
            gpu_command_ok = False
    tpu_hint = bool(os.environ.get("TPU_NAME") or os.environ.get("COLAB_TPU_ADDR"))
    detected = bool(detected_paths or gpu_command_ok or tpu_hint)
    results["accelerator_probe"] = {
        "status": "AVAILABLE" if detected else "NOT_DETECTED",
        "nvidia_smi_present": bool(nvidia_smi),
        "device_paths_detected": detected_paths,
        "tpu_environment_hint": tpu_hint,
        "interpretation": (
            "A recognized accelerator signal was detected; workload-specific support still needs testing."
            if detected else
            "No supported accelerator signal was detected in this runner; do not infer that every underlying host lacks accelerators."
        ),
    }

    # Guard the large fine-tune: no pinned weights, reviewed license, hardware qualification,
    # or approved compute budget exists in this workflow.
    results["large_llm_finetune"] = {
        "status": "NOT_ATTEMPTED_RESOURCE_GUARD",
        "reason": "Requires pinned model weights, license review, measured accelerator memory, and an approved compute budget.",
    }
    return results

def classify_comparison(simulated_expected, actual_status):
    if actual_status == "NOT_ATTEMPTED_RESOURCE_GUARD":
        return "NOT_COMPARABLE_NOT_RUN"
    if actual_status == "NOT_DETECTED":
        if simulated_expected == "SIMULATED_SUCCESS":
            return "SIMULATION_REALITY_GAP_RESOURCE_NOT_DETECTED"
        return "RESOURCE_ABSENCE_NOT_VERIFIED"
    if actual_status == "AVAILABLE":
        return "RESOURCE_SIGNAL_MATCH" if simulated_expected == "SIMULATED_SUCCESS" else "SIMULATION_REALITY_GAP"
    if simulated_expected == "SIMULATED_SUCCESS" and actual_status == "PASS":
        return "MATCH_TASK_EXECUTED"
    if simulated_expected != "SIMULATED_SUCCESS" and actual_status == "PASS":
        return "REAL_TASK_SUCCEEDED_DESPITE_SIMULATOR_ASSUMPTION"
    return "DIVERGENCE_OR_FAILURE"

def build_report(root, real_results):
    sim_runs = [simulate(name, jobs=12, seed=42) for name in PROFILE_NAMES]
    profiles = {}
    for run in sim_runs:
        profile = run["profile"]
        task_rows = []
        for task_id, task in SIMULATED_TASKS.items():
            expected = "SIMULATED_SUCCESS" if profile in task["simulated_success_profiles"] else "SIMULATED_UNAVAILABLE"
            actual = real_results[task_id]["status"]
            task_rows.append({
                "task_id": task_id,
                "description": task["description"],
                "simulation_prediction": expected,
                "actual_runner_status": actual,
                "comparison": classify_comparison(expected, actual),
                "real_execution_attempted": task["real_runner_safe"] and actual != "NOT_ATTEMPTED_RESOURCE_GUARD",
            })
        profiles[profile] = {"simulator_profile": run, "task_comparisons": task_rows}

    all_comparisons = [item for profile in profiles.values() for item in profile["task_comparisons"]]
    executed = sum(item["real_execution_attempted"] for item in all_comparisons)
    matches = sum(item["comparison"] in ("MATCH_TASK_EXECUTED", "RESOURCE_SIGNAL_MATCH") for item in all_comparisons)
    gaps = sum("GAP" in item["comparison"] or item["comparison"] == "DIVERGENCE_OR_FAILURE" for item in all_comparisons)
    not_comp = sum(item["comparison"] == "NOT_COMPARABLE_NOT_RUN" for item in all_comparisons)
    data_path = root / "datasets" / "principle_intents.jsonl"
    script_path = root / "src" / "miilab" / "reality_gate.py"
    return {
        "schema_version": "miilab.reality-gate.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "evidence_class": "MIXED_SIMULATION_AND_REAL_RUNNER_EXECUTION",
        "execution_environment": {
            "provider": "GitHub Actions runner when run in CI",
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "hardware_class": "hosted runner; accelerator capability independently probed",
            "not_equivalent_to": ["founder Android device", "production server", "external customer system"],
        },
        "evidence_hashes": {
            "dataset_sha256": sha256_bytes(data_path.read_bytes()) if data_path.exists() else None,
            "reality_gate_script_sha256": sha256_bytes(script_path.read_bytes()) if script_path.exists() else None,
        },
        "real_world_scope": "Actual code execution in this CI runner, restricted to bounded repository-local checks; not a production deployment test.",
        "real_task_results": real_results,
        "profiles": profiles,
        "summary": {
            "profile_count": len(profiles),
            "comparison_rows": len(all_comparisons),
            "real_execution_attempts_counted_per_profile": executed,
            "matching_comparisons": matches,
            "simulation_reality_gaps_or_failures": gaps,
            "not_comparable_because_not_run": not_comp,
            "large_model_training_claimed": False,
        },
        "rules": [
            "SIMULATED_SUCCESS is a prediction from declared synthetic assumptions, not evidence of real capability.",
            "A task counts as real-run validated only when the same defined check executes and returns PASS in this runner.",
            "NOT_DETECTED is not proof that the underlying host infrastructure has no accelerator.",
            "A passing CI-runner check does not prove the task works on an Android device, production system, or external account.",
            "Large foundation-model fine-tuning is deliberately not attempted in this gate.",
        ],
    }

def render_markdown(report):
    summary = report["summary"]
    lines = [
        "# Simulation-to-Reality Gate", "",
        f"- Generated UTC: {report['generated_at']}",
        f"- Evidence class: {report['evidence_class']}",
        f"- Profiles compared: {summary['profile_count']}",
        f"- Comparison rows: {summary['comparison_rows']}",
        f"- Matching comparisons: {summary['matching_comparisons']}",
        f"- Simulation/reality gaps or failures: {summary['simulation_reality_gaps_or_failures']}",
        f"- Not comparable (task intentionally not run): {summary['not_comparable_because_not_run']}",
        "", "## Actual runner checks", "",
        "| Task | Actual status | Evidence |",
        "|---|---|---|",
    ]
    for task, result in report["real_task_results"].items():
        evidence = result.get("reason") or result.get("interpretation") or result.get("error") or result.get("artifact_round_trip", "")
        lines.append(f"| {task} | {result['status']} | {str(evidence).replace('|', '/')} |")
    lines += [
        "", "## Interpretation", "",
        "A simulation result is not a real-world success. Here, real means the same bounded check executed on the hosted CI runner. It does not certify the founder's device, customer systems, production services, or a generative AI model.",
        "",
        "Large-model fine-tuning is guarded and not attempted until model revision, license, hardware memory, and compute budget have been qualified.",
    ]
    return "\n".join(lines) + "\n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="evidence/reality_gate_latest.json")
    parser.add_argument("--markdown-output", default="reports/reality/reality_gate_latest.md")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    results = run_real_tasks(root)
    report = build_report(root, results)
    output = root / args.output
    markdown = root / args.markdown_output
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    return 0 if all(results[key]["status"] == "PASS" for key in ("dataset_validation", "tiny_classifier_training", "python_source_compile")) else 1

if __name__ == "__main__":
    raise SystemExit(main())
