"""Synthetic compute profiles; no physical accelerator or unlimited compute is provisioned."""
import argparse, json, math, random
from datetime import datetime, timezone
from pathlib import Path

PROFILES = {
 "cpu_virtual":{"device_class":"CPU","slots":4,"units_per_tick":10,"storage_units":1000},
 "gpu_virtual":{"device_class":"GPU","slots":16,"units_per_tick":160,"storage_units":10000},
 "tpu_virtual":{"device_class":"TPU","slots":32,"units_per_tick":240,"storage_units":20000},
 "server_virtual":{"device_class":"SERVER","slots":64,"units_per_tick":500,"storage_units":100000},
 "infinity_space_server":{"device_class":"FICTIONAL_ELASTIC_SIMULATOR","slots":None,"units_per_tick":1000,"storage_units":None}}

def simulate(name, jobs=12, seed=42):
    if name not in PROFILES: raise ValueError("Unknown profile")
    if not 1 <= jobs <= 1000: raise ValueError("jobs must be 1..1000")
    profile=PROFILES[name]; rng=random.Random(seed)
    tasks=[{"job_id":f"JOB-{i+1:04d}","work_units":rng.randint(100,2500)} for i in range(jobs)]
    slots=profile["slots"] or jobs
    total=sum(t["work_units"] for t in tasks)
    ticks=sum(math.ceil(sum(x["work_units"] for x in tasks[i:i+slots])/profile["units_per_tick"]) for i in range(0,len(tasks),slots))
    return {"schema_version":"miilab.simulation.v1","evidence_class":"SIMULATION","generated_at":datetime.now(timezone.utc).isoformat(),
      "profile":name,"device_class":profile["device_class"],"physical_hardware_provisioned":False,
      "logical_slots":"unbounded-in-simulator" if profile["slots"] is None else profile["slots"],
      "logical_storage_units":"unbounded-in-simulator" if profile["storage_units"] is None else profile["storage_units"],
      "job_count":jobs,"total_work_units":total,"synthetic_units_per_tick":profile["units_per_tick"],"simulated_ticks":ticks,
      "status":"SIMULATED_COMPLETE","limitations":["Not a hardware benchmark","Not real wall-clock timing","No real storage or compute allocated"]}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--profile",choices=[*PROFILES,"all"],default="all")
    p.add_argument("--jobs",type=int,default=12); p.add_argument("--seed",type=int,default=42); p.add_argument("--output")
    a=p.parse_args(); names=list(PROFILES) if a.profile=="all" else [a.profile]
    result={"schema_version":"miilab.simulation-bundle.v1","evidence_class":"SIMULATION","runs":[simulate(n,a.jobs,a.seed) for n in names]}
    payload=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if a.output:
        Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(payload,encoding="utf-8")
    print(payload,end="")

if __name__=="__main__": main()
