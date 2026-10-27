import unittest
from miilab.simulation import FAST_SAMPLE_SIZE, MAX_EXACT_JOBS, PROFILES, simulate


class FastSimulationTests(unittest.TestCase):
    def test_large_fast_mode_samples_instead_of_looping_every_logical_job(self):
        result = simulate("gpu_virtual", jobs=1_000_000, seed=42, mode="fast")
        self.assertEqual(result["evidence_class"], "SIMULATION")
        self.assertEqual(result["execution_mode"], "FAST_SAMPLED_ESTIMATE")
        self.assertEqual(result["sampled_jobs"], FAST_SAMPLE_SIZE)
        self.assertGreaterEqual(result["sampling_reduction_factor"], 100)
        self.assertTrue(result["work_units_estimated"])
        self.assertEqual(result["job_count"], 1_000_000)

    def test_small_fast_run_is_exact(self):
        result = simulate("cpu_virtual", jobs=12, seed=42, mode="fast")
        self.assertEqual(result["execution_mode"], "EXACT_SMALL_RUN")
        self.assertFalse(result["work_units_estimated"])

    def test_exact_run_is_deterministic_for_metrics(self):
        a = simulate("cpu_virtual", jobs=100, seed=17, mode="exact")
        b = simulate("cpu_virtual", jobs=100, seed=17, mode="exact")
        self.assertEqual(a["total_work_units"], b["total_work_units"])
        self.assertEqual(a["simulated_ticks"], b["simulated_ticks"])

    def test_exact_mode_has_a_guard(self):
        with self.assertRaises(ValueError):
            simulate("cpu_virtual", jobs=MAX_EXACT_JOBS + 1, mode="exact")

    def test_sample_size_has_minimum_for_finite_batch_estimates(self):
        with self.assertRaises(ValueError):
            simulate("gpu_virtual", jobs=1_000_000, mode="fast", sample_size=1)

    def test_unknown_profile_is_rejected(self):
        with self.assertRaises(ValueError):
            simulate("quantum_magic", jobs=1)

    def test_virtual_profiles_never_claim_hardware(self):
        for name in PROFILES:
            result = simulate(name, jobs=50, seed=42, mode="fast")
            self.assertFalse(result["physical_hardware_provisioned"])
            self.assertEqual(result["evidence_class"], "SIMULATION")


if __name__ == "__main__":
    unittest.main()
