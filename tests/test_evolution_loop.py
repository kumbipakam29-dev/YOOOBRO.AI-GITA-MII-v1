import unittest
from pathlib import Path
from miilab.evolution_loop import CHECK_ORDER, MAX_CYCLES_PER_RUN, MAX_TASK_TIMEOUT_SECONDS, execute_loop

ROOT=Path(".").resolve()
class EvolutionLoopTests(unittest.TestCase):
    def test_cycle_and_timeout_caps(self):
        with self.assertRaises(ValueError): execute_loop(ROOT,cycles=MAX_CYCLES_PER_RUN+1)
        with self.assertRaises(ValueError): execute_loop(ROOT,cycles=1,timeout_seconds=MAX_TASK_TIMEOUT_SECONDS+1)
    def test_schedule_includes_catalog_and_reality_gate(self):
        self.assertEqual(len(CHECK_ORDER),len(set(CHECK_ORDER)))
        self.assertIn("hard_task_catalog_integrity",CHECK_ORDER)
        self.assertIn("simulation_to_reality_gate",CHECK_ORDER)
    def test_one_cycle_runs_real_check_and_hashes_logs(self):
        r=execute_loop(ROOT,cycles=1,timeout_seconds=30)
        self.assertEqual(r["cycles_executed"],1); row=r["results"][0]
        self.assertTrue(row["real_execution"]); self.assertEqual(row["evidence_class"],"REAL_RUNNER_EXECUTION")
        self.assertEqual(len(row["stdout_sha256"]),64); self.assertEqual(len(row["stderr_sha256"]),64)
        self.assertIn(row["status"],("PASS","FAIL","TIMED_OUT","ERROR"))
if __name__=="__main__": unittest.main()
