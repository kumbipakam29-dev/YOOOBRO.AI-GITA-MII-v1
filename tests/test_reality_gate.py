import unittest

from miilab.reality_gate import classify_comparison, SIMULATED_TASKS, PROFILE_NAMES

class RealityGateTests(unittest.TestCase):
    def test_known_profiles_are_compared(self):
        self.assertEqual(len(PROFILE_NAMES), 5)
        self.assertIn("infinity_space_server", PROFILE_NAMES)

    def test_safe_tasks_have_simulated_expected_success(self):
        for task_id in ("dataset_validation", "tiny_classifier_training", "python_source_compile", "persona_panel_generation"):
            self.assertEqual(set(SIMULATED_TASKS[task_id]["simulated_success_profiles"]), set(PROFILE_NAMES))

    def test_ten_million_panel_stress_is_in_reality_gate(self):
        self.assertEqual(
            set(SIMULATED_TASKS["persona_panel_stress_10m"]["simulated_success_profiles"]),
            set(PROFILE_NAMES)
        )

    def test_simulation_pass_requires_actual_pass(self):
        self.assertEqual(classify_comparison("SIMULATED_SUCCESS", "PASS"), "MATCH_TASK_EXECUTED")

    def test_simulated_accelerator_does_not_claim_real_accelerator(self):
        self.assertEqual(
            classify_comparison("SIMULATED_SUCCESS", "NOT_DETECTED"),
            "SIMULATION_REALITY_GAP_RESOURCE_NOT_DETECTED"
        )

    def test_no_accelerator_signal_is_not_proof_of_absence(self):
        self.assertEqual(
            classify_comparison("SIMULATED_UNAVAILABLE", "NOT_DETECTED"),
            "RESOURCE_ABSENCE_NOT_VERIFIED"
        )

    def test_large_training_is_blocked_when_infinity_simulation_overpromises(self):
        self.assertEqual(
            classify_comparison("SIMULATED_SUCCESS", "NOT_ATTEMPTED_RESOURCE_GUARD"),
            "SIMULATED_SUCCESS_REAL_BLOCKED_GUARD"
        )

    def test_unavailable_prediction_and_guarded_task_remain_not_comparable(self):
        self.assertEqual(
            classify_comparison("SIMULATED_UNAVAILABLE", "NOT_ATTEMPTED_RESOURCE_GUARD"),
            "NOT_COMPARABLE_NOT_RUN"
        )

    def test_real_success_can_disprove_simulator_assumption(self):
        self.assertEqual(
            classify_comparison("SIMULATED_UNAVAILABLE", "PASS"),
            "REAL_TASK_SUCCEEDED_DESPITE_SIMULATOR_ASSUMPTION"
        )

if __name__ == "__main__":
    unittest.main()
