"""Bounded self-improvement research controller: actual local checks, hashes and failures."""
from __future__ import annotations
import argparse, hashlib, json, os, platform, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path

CHECK_ORDER=["dataset_integrity","hard_task_catalog_integrity","source_compile","tiny_cpu_training",
             "virtual_compute_smoke","persona_panel_integrity","psychology_task_schema","simulation_to_reality_gate"]
MAX_CYCLES_PER_RUN=20
MAX_TASK_TIMEOUT_SECONDS=300
QUARANTINE_AFTER_CONSECUTIVE_FAILURES=3

def _sha(data): return hashlib.sha256(data).hexdigest()
def _command(name, temp):
    py=sys.executable
    if name=="dataset_integrity":
        return [py,"-c","from miilab.trainer import read_rows; r=read_rows('datasets/principle_intents.jsonl'); assert len(r)>=20 and len({x['label'] for x in r})>=7; print({'rows':len(r)})"]
    if name=="hard_task_catalog_integrity": return [py,"-m","miilab.hard_task_catalog"]
    if name=="source_compile":
        return [py,"-c","from pathlib import Path; f=list(Path('src').rglob('*.py'))+list(Path('tests').rglob('*.py')); [compile(p.read_text(encoding='utf-8'),str(p),'exec') for p in f]; print({'compiled_files':len(f)})"]
    if name=="tiny_cpu_training":
        return [py,"-m","miilab.trainer","--data","datasets/principle_intents.jsonl","--output",str(temp/"model.json"),"--metrics",str(temp/"metrics.json")]
    if name=="virtual_compute_smoke":
        return [py,"-m","miilab.simulation","--profile","all","--jobs","12","--mode","exact","--output",str(temp/"compute.json")]
    if name=="persona_panel_integrity": return [py,"-m","miilab.persona_panel","--output",str(temp/"panel.json")]
    if name=="psychology_task_schema":
        code=("import json; from pathlib import Path; r=[json.loads(x) for x in Path('experiments/miilab_hard_tasks_v1.jsonl').read_text().splitlines() if x.strip()]; d={x['task_id']:x for x in r}; "
              "assert 'synthetic' in d['human_perspective_taking']['challenge'].lower(); assert 'synthetic' in d['emotion_uncertainty_calibration']['challenge'].lower(); "
              "assert all('diagnosis' in d[k]['safety_boundary'].lower() for k in ('human_perspective_taking','emotion_uncertainty_calibration')); print({'psychology':'synthetic/non-diagnostic'})")
        return [py,"-c",code]
    if name=="simulation_to_reality_gate":
        return [py,"-m","miilab.reality_gate","--output",str(temp/"reality.json"),"--markdown-output",str(temp/"reality.md")]
    raise ValueError(f"Unknown check: {name}")

def run_check(name, root, timeout_seconds):
    started=time.perf_counter()
    with tempfile.TemporaryDirectory(prefix=f"miilab-{name}-") as tmp:
        temp=Path(tmp); env=os.environ.copy(); env["PYTHONPATH"]=str(root/"src")+os.pathsep+env.get("PYTHONPATH","")
        try:
            proc=subprocess.run(_command(name,temp),cwd=root,env=env,text=True,capture_output=True,timeout=timeout_seconds,check=False)
            out,err=proc.stdout or "",proc.stderr or ""; status="PASS" if proc.returncode==0 else "FAIL"; code=proc.returncode
        except subprocess.TimeoutExpired as exc:
            def dec(v):
                if v is None: return ""
                return v.decode("utf-8",errors="replace") if isinstance(v,bytes) else v
            out,err=dec(exc.stdout),dec(exc.stderr); status,code="TIMED_OUT",None
        except OSError as exc:
            out,err,status,code="",str(exc),"ERROR",None
        return {"check_id":name,"status":status,"exit_code":code,"duration_seconds":round(time.perf_counter()-started,6),
                "timeout_seconds":timeout_seconds,"stdout_sha256":_sha(out.encode()),"stderr_sha256":_sha(err.encode()),
                "stdout_tail":out[-1200:],"stderr_tail":err[-1200:],"real_execution":True,"evidence_class":"REAL_RUNNER_EXECUTION"}

def execute_loop(root, cycles=7, timeout_seconds=120):
    if not 1<=cycles<=MAX_CYCLES_PER_RUN: raise ValueError(f"cycles must be 1..{MAX_CYCLES_PER_RUN}")
    if not 1<=timeout_seconds<=MAX_TASK_TIMEOUT_SECONDS: raise ValueError(f"timeout must be 1..{MAX_TASK_TIMEOUT_SECONDS}")
    results=[]; failures={}; quarantined=[]; cursor=0; priority=None
    for cycle in range(1,cycles+1):
        available=[x for x in CHECK_ORDER if x not in quarantined]
        if not available: break
        is_retry=priority in available and failures.get(priority,0)<QUARANTINE_AFTER_CONSECUTIVE_FAILURES
        name=priority if is_retry else available[cursor%len(available)]
        if not is_retry: cursor+=1
        result=run_check(name,root,timeout_seconds); result["cycle"]=cycle
        result["selected_reason"]="retry_recent_failure" if is_retry else "round_robin_coverage"; results.append(result)
        if result["status"]=="PASS": failures[name]=0; priority=None
        else:
            failures[name]=failures.get(name,0)+1
            if failures[name]>=QUARANTINE_AFTER_CONSECUTIVE_FAILURES:
                if name not in quarantined: quarantined.append(name)
                priority=None
            else: priority=name
    statuses=("PASS","FAIL","TIMED_OUT","ERROR")
    counts={s:sum(x["status"]==s for x in results) for s in statuses}
    attempted={x["check_id"] for x in results}
    catalog=root/"experiments/miilab_hard_tasks_v1.jsonl"
    return {"schema_version":"miilab.evolution-loop.v1","generated_at":datetime.now(timezone.utc).isoformat(),
            "evidence_class":"BOUNDED_REAL_RUNNER_EXPERIMENT_LOOP","controller":"deterministic scheduler; no hidden LLM calls",
            "environment":{"python_version":sys.version.split()[0],"platform":platform.platform()},
            "requested_cycles":cycles,"cycles_executed":len(results),"timeout_seconds_per_check":timeout_seconds,
            "max_cycles_per_run":MAX_CYCLES_PER_RUN,"max_timeout_seconds":MAX_TASK_TIMEOUT_SECONDS,
            "quarantine_after_consecutive_failures":QUARANTINE_AFTER_CONSECUTIVE_FAILURES,"check_rotation":CHECK_ORDER,
            "results":results,"failure_counts":failures,"quarantined_checks":quarantined,
            "checks_not_attempted_this_run":[x for x in CHECK_ORDER if x not in attempted],"status_counts":counts,
            "hard_task_catalog_count":sum(bool(x.strip()) for x in catalog.read_text(encoding="utf-8").splitlines()),
            "frontier_challenge_tasks_solved":0,
            "limits":["Bounded loop, not infinite within one workflow.","Hourly runs depend on GitHub scheduling and quotas.",
                      "Passing repository checks does not solve frontier challenges.","No source self-editing, paid calls or external side effects.",
                      "Failed checks are quarantined after three consecutive failures."]}
def render_markdown(report):
    c=report["status_counts"]
    lines=["# MIi Bounded Evolution Loop","",f"- Generated UTC: {report['generated_at']}",
           f"- Cycles: {report['cycles_executed']}/{report['requested_cycles']}",
           f"- Hard-task definitions: {report['hard_task_catalog_count']}",
           f"- PASS / FAIL / TIMEOUT / ERROR: {c['PASS']} / {c['FAIL']} / {c['TIMED_OUT']} / {c['ERROR']}",
           f"- Frontier tasks claimed solved: {report['frontier_challenge_tasks_solved']}",
           f"- Quarantined checks: {', '.join(report['quarantined_checks']) or 'none'}","",
           "| Cycle | Check | Status | Seconds | Exit |","|---:|---|---|---:|---:|"]
    lines += [f"| {r['cycle']} | {r['check_id']} | {r['status']} | {r['duration_seconds']} | {r['exit_code']} |" for r in report["results"]]
    lines += ["","This report validates only these bounded runner checks. The hard-task catalog remains planned until task-specific verifiers and independent reviews pass.",""]
    return "\n".join(lines)
def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--root",type=Path,default=Path("."))
    p.add_argument("--cycles",type=int,default=7); p.add_argument("--timeout-seconds",type=int,default=120)
    p.add_argument("--output",type=Path,default=Path("reports/evolution/latest.json")); p.add_argument("--markdown-output",type=Path,default=Path("reports/evolution/latest.md"))
    a=p.parse_args(); root=a.root.resolve(); report=execute_loop(root,a.cycles,a.timeout_seconds)
    out,md=root/a.output,root/a.markdown_output; out.parent.mkdir(parents=True,exist_ok=True); md.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); md.write_text(render_markdown(report),encoding="utf-8")
    print(json.dumps({"cycles_executed":report["cycles_executed"],"status_counts":report["status_counts"],"quarantined_checks":report["quarantined_checks"]},indent=2))
    return 0 if report["results"] and all(x["status"]=="PASS" for x in report["results"]) else 1
if __name__=="__main__": raise SystemExit(main())
