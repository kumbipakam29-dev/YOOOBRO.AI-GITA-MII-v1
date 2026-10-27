import json, unittest
from pathlib import Path
from miilab.hard_task_catalog import validate

class HardTaskCatalogTests(unittest.TestCase):
    def test_catalog_is_broad_unique_and_valid(self):
        r=validate("experiments/miilab_hard_tasks_v1.jsonl")
        self.assertGreaterEqual(r["task_count"],35)
        self.assertGreaterEqual(r["domain_count"],20)
        self.assertTrue(r["all_initially_planned"])
    def test_every_task_has_verifier_and_safety_boundary(self):
        rows=[json.loads(x) for x in Path("experiments/miilab_hard_tasks_v1.jsonl").read_text().splitlines() if x.strip()]
        for row in rows:
            for key in ("task_id","domain","challenge","required_verifier","execution_class","status","safety_boundary"):
                self.assertTrue(row.get(key),f"{row.get('task_id')} missing {key}")
            self.assertEqual(row["status"],"PLANNED_NOT_RUN")
    def test_psychology_tasks_are_synthetic_and_non_diagnostic(self):
        rows={x["task_id"]:x for x in [json.loads(y) for y in Path("experiments/miilab_hard_tasks_v1.jsonl").read_text().splitlines() if y.strip()]}
        for tid in ("human_perspective_taking","emotion_uncertainty_calibration"):
            self.assertIn("synthetic",rows[tid]["challenge"].lower())
            self.assertIn("diagnosis",rows[tid]["safety_boundary"].lower())
if __name__=="__main__": unittest.main()
