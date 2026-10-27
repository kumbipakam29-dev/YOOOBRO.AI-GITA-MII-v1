"""Fast synthetic compute-profile simulator. It provisions no physical resources."""
from __future__ import annotations
import argparse
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROFILES = {
    "cpu_virtual": {"device_class": "CPU", "slots": 4, "units_per_tick": 10, "storage_units": 1_000},
    "gpu_virtual": {"device_class": "GPU", "slots": 16, "units_per_tick": 160, "storage_units": 10_000},
    "tpu_virtual": {"device_class": "TPU", "slots": 32, "units_per_tick": 240, "storage_units": 20_000},
    "server_virtual": {"device_class": "SERVER", "slots": 64, "units_per_tick": 500, "storage_units": 100_000},
    "infinity_space_server": {"device_class": "FICTIONAL_ELASTIC_SIMULATOR", "slots": None, "units_per_tick": 1_000, "storage_units": None},
}
FAST_SAMPLE_SIZE = 4_096
MAX_FAST_JOBS = 10_000_000
MAX_EXACT_JOBS = 100_000
DETAILS_MAX_JOBS = 1_000


def _workload(seed: int, count: int) -> list[int]:
    """Create integers only; avoid per-job dictionaries to reduce allocation overhead."""
    rng = random.Random(seed)
    return [rng.randint(100, 2_500) for _ in range(count)]


def _exact_ticks(work: list[int], slots: int, units_per_tick: int) -> tuple[int, int, list[dict[str, Any]]]:
    ticks = 0
    batches: list[dict[str, Any]] = []
    for batch_index, offset in enumerate(range(0, len(work), slots), start=1):
        batch = work[offset:offset + slots]
        batch_work = sum(batch)
        batch_ticks = math.ceil(batch_work / units_per_tick)
        ticks += batch_ticks
        if len(work) <= DETAILS_MAX_JOBS:
            batches.append({
                "batch": batch_index,
                "jobs": len(batch),
                "work_units": batch_work,
                "simulated_ticks": batch_ticks,
            })
    return ticks, math.ceil(len(work) / slots), batches


def simulate(name: str, jobs: int = 12, seed: int = 42, mode: str = "exact",
             sample_size: int = FAST_SAMPLE_SIZE, max_ticks: int = 100_000) -> dict[str, Any]:
    """Simulate exact small tasks or estimate large logical workloads from a deterministic sample.

    Fast-mode sampling applies to the simulation inner loop, not GitHub runner startup time.
    """
    if name not in PROFILES:
        raise ValueError(f"Unknown profile: {name}")
    if mode not in ("exact", "fast"):
        raise ValueError("mode must be 'exact' or 'fast'")
    if not 1 <= jobs <= MAX_FAST_JOBS:
        raise ValueError(f"jobs must be in [1, {MAX_FAST_JOBS}]")
    if not 1 <= sample_size <= 100_000:
        raise ValueError("sample_size must be in [1, 100000]")
    if not 1 <= max_ticks <= 1_000_000_000:
        raise ValueError("max_ticks must be in [1, 1000000000]")
    if mode == "exact" and jobs > MAX_EXACT_JOBS:
        raise ValueError(f"exact mode is limited to {MAX_EXACT_JOBS} jobs; use fast mode for larger workloads")

    profile = PROFILES[name]
    slots = profile["slots"] if profile["slots"] is not None else jobs
    sampled = mode == "fast" and jobs > sample_size
    measured_jobs = min(jobs, sample_size) if sampled else jobs
    work = _workload(seed, measured_jobs)
    sample_total = sum(work)
    estimated = sampled
    total_work = round((sample_total / measured_jobs) * jobs) if sampled else sample_total
    batches: list[dict[str, Any]] = []

    if not sampled:
        total_ticks, batch_count, batches = _exact_ticks(work, slots, profile["units_per_tick"])
    elif profile["slots"] is None:
        total_ticks = math.ceil(total_work / profile["units_per_tick"])
        batch_count = 1
    else:
        # Current finite slot sizes divide 4096. Estimate mean batch ticks and scale by
        # the logical batch count; estimate a final partial batch from sampled mean work.
        full_sample_batches = len(work) // slots
        sample_batch_ticks = [
            math.ceil(sum(work[i:i + slots]) / profile["units_per_tick"])
            for i in range(0, full_sample_batches * slots, slots)
        ]
        mean_batch_ticks = sum(sample_batch_ticks) / max(1, len(sample_batch_ticks))
        full_batches = jobs // slots
        remainder = jobs % slots
        tail_ticks = math.ceil((sample_total / measured_jobs) * remainder / profile["units_per_tick"]) if remainder else 0
        total_ticks = round(mean_batch_ticks * full_batches) + tail_ticks
        batch_count = math.ceil(jobs / slots)

    execution_mode = "FAST_SAMPLED_ESTIMATE" if sampled else ("EXACT_SMALL_RUN" if mode == "fast" else "EXACT")
    return {
        "schema_version": "miilab.simulation.v2",
        "evidence_class": "SIMULATION",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "profile": name,
        "device_class": profile["device_class"],
        "physical_hardware_provisioned": False,
        "logical_slots": "unbounded-in-simulator" if profile["slots"] is None else profile["slots"],
        "logical_storage_units": "unbounded-in-simulator" if profile["storage_units"] is None else profile["storage_units"],
        "job_count": jobs,
        "sampled_jobs": measured_jobs,
        "sampling_reduction_factor": round(jobs / measured_jobs, 3),
        "requested_mode": mode,
        "execution_mode": execution_mode,
        "work_units_estimated": estimated,
        "total_work_units": total_work,
        "synthetic_units_per_tick": profile["units_per_tick"],
        "batch_count": batch_count,
        "simulated_ticks": total_ticks,
        "max_ticks": max_ticks,
        "status": "SIMULATED_COMPLETE" if total_ticks <= max_ticks else "SIMULATED_TIMEOUT",
        "batch_detail_included": bool(batches),
        "batches": batches,
        "limitations": [
            "Not a hardware benchmark",
            "Not real wall-clock timing",
            "No real storage or compute allocated",
            "Fast sampled mode estimates large workloads from a deterministic sample",
            "Fictional unbounded capacity is only a model assumption",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=[*PROFILES, "all"], default="all")
    parser.add_argument("--jobs", type=int, default=12, help=f"Logical jobs (1-{MAX_FAST_JOBS}); fast mode recommended for large values")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--mode", choices=["fast", "exact"], default="fast")
    parser.add_argument("--sample-size", type=int, default=FAST_SAMPLE_SIZE)
    parser.add_argument("--max-ticks", type=int, default=100_000)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    names = list(PROFILES) if args.profile == "all" else [args.profile]
    runs = [simulate(n, args.jobs, args.seed, args.mode, args.sample_size, args.max_ticks) for n in names]
    payload = json.dumps({
        "schema_version": "miilab.simulation-bundle.v2",
        "evidence_class": "SIMULATION",
        "requested_mode": args.mode,
        "runs": runs,
    }, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
