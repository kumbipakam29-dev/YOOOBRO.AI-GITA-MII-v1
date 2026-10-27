"""Train a tiny Naive Bayes intent classifier on synthetic examples; not an LLM."""
import argparse, hashlib, json, math, re, sys, platform, time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

TOKEN_RE = re.compile(r"[a-z0-9]+|[\u0900-\u097f]+", re.IGNORECASE)

def read_rows(path):
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise ValueError("Empty training dataset")
    for row in rows:
        if not isinstance(row.get("text"), str) or not row["text"].strip() or not isinstance(row.get("label"), str):
            raise ValueError("Every row requires non-empty text and label")
    return rows

def train(rows):
    docs, counts, vocab = Counter(), defaultdict(Counter), set()
    for row in rows:
        tokens = TOKEN_RE.findall(row["text"].lower())
        if not tokens:
            raise ValueError("Example produced no tokens")
        docs[row["label"]] += 1
        counts[row["label"]].update(tokens)
        vocab.update(tokens)
    labels = sorted(docs)
    model = {"schema_version":"miilab.nb-model.v1","algorithm":"multinomial_naive_bayes","labels":labels,
             "vocabulary":sorted(vocab),"document_count":len(rows),"document_counts":dict(docs),
             "class_log_prior":{},"token_log_likelihood":{},"smoothing_alpha":1.0}
    for label in labels:
        model["class_log_prior"][label] = math.log(docs[label] / len(rows))
        total = sum(counts[label].values())
        model["token_log_likelihood"][label] = {
            word: math.log((counts[label][word] + 1) / (total + len(vocab))) for word in sorted(vocab)}
    return model

def predict(model, text):
    vocab = set(model["vocabulary"])
    tokens = [t for t in TOKEN_RE.findall(text.lower()) if t in vocab]
    scores = {}
    for label in model["labels"]:
        scores[label] = model["class_log_prior"][label] + sum(model["token_log_likelihood"][label][t] for t in tokens)
    best = max(scores, key=lambda k: (scores[k], k))
    return best

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", default="datasets/principle_intents.jsonl")
    p.add_argument("--output", default="evidence/cpu_baseline_model.json")
    p.add_argument("--metrics", default="evidence/latest_cpu_training.json")
    a = p.parse_args()
    start = time.perf_counter()
    rows = read_rows(a.data)
    model = train(rows)
    accuracy = sum(predict(model, r["text"]) == r["label"] for r in rows) / len(rows)
    model_bytes = (json.dumps(model, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    Path(a.output).write_bytes(model_bytes)
    data_bytes = Path(a.data).read_bytes()
    metric = {"schema_version":"miilab.training-run.v1","run_id":"CPU-BASELINE","evidence_class":"ACTUAL_TRAINING",
      "training_performed":True,"trained_at":datetime.now(timezone.utc).isoformat(),
      "duration_seconds":round(time.perf_counter()-start,6),
      "environment":{"python_version":sys.version.split()[0],"platform":platform.platform(),"hardware_class":"CPU_ONLY"},
      "algorithm":model["algorithm"],"base_model":None,"full_language_model":False,
      "dataset_path":a.data,"dataset_sha256":hashlib.sha256(data_bytes).hexdigest(),"dataset_rows":len(rows),
      "classes":model["labels"],"vocabulary_size":len(model["vocabulary"]),
      "training_example_accuracy":round(accuracy,6),
      "accuracy_warning":"Training-set score only; not held-out generalization performance.",
      "model_artifact_path":a.output,"model_artifact_sha256":hashlib.sha256(model_bytes).hexdigest(),
      "capability_limit":"Tiny bag-of-words classifier; not a generative LLM or frontier-task solution."}
    Path(a.metrics).parent.mkdir(parents=True, exist_ok=True)
    Path(a.metrics).write_text(json.dumps(metric, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(metric, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
