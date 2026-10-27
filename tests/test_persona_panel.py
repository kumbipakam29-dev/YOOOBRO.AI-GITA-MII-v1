import unittest
from miilab.persona_panel import build_panel


class PersonaPanelTests(unittest.TestCase):
    def setUp(self):
        self.panel = build_panel()

    def test_eight_public_work_inspired_lenses_and_eight_challenges(self):
        self.assertEqual(self.panel["persona_count"], 8)
        self.assertEqual(self.panel["challenge_task_count"], 8)
        self.assertEqual(self.panel["review_count"], 64)

    def test_one_million_iq_is_not_claimed_as_a_real_metric(self):
        self.assertFalse(self.panel["iq_claimed"])
        self.assertIsNone(self.panel["perspective_reviews"][0]["iq_estimate"])
        self.assertIn("fictional gamification", self.panel["label_disclaimer"])

    def test_not_a_real_person_replica(self):
        self.assertFalse(self.panel["actual_people_recreated"])
        self.assertTrue(all(not row["named_person_is_actually_participating"] for row in self.panel["perspective_reviews"]))
        self.assertTrue(all(not row["personal_voice_or_private_thoughts_recreated"] for row in self.panel["perspective_reviews"]))
        self.assertTrue(all(not row["invented_person_quote"] for row in self.panel["perspective_reviews"]))

    def test_persona_panel_does_not_claim_to_solve_the_challenges(self):
        self.assertFalse(self.panel["solutions_claimed"])
        self.assertTrue(all(row["status"] == "PERSPECTIVE_SIMULATION_NOT_SOLVED" for row in self.panel["perspective_reviews"]))

    def test_scaled_panel_stress_aggregates_counts_without_faking_iq(self):
        from miilab.persona_panel import run_scaled_panel_stress
        result = run_scaled_panel_stress(panel_count=100)
        self.assertEqual(result["panels_processed"], 100)
        self.assertEqual(result["virtual_review_cell_equivalents"], 6_400)
        self.assertEqual(result["coverage_check"], "PASS")
        self.assertEqual(result["review_cells_individually_materialized"], 0)
        self.assertFalse(result["iq_claimed"])
        self.assertEqual(result["generative_model_inference_calls"], 0)

    def test_scaled_panel_stress_caps_workload(self):
        from miilab.persona_panel import run_scaled_panel_stress
        with self.assertRaises(ValueError):
            run_scaled_panel_stress(panel_count=10_000_001)

    def test_known_public_person_lenses_are_present(self):
        people = {row["public_person_reference"] for row in self.panel["perspective_reviews"]}
        self.assertIn("Albert Einstein", people)
        self.assertIn("Srinivasa Ramanujan", people)
        self.assertIn("Ada Lovelace", people)


if __name__ == "__main__":
    unittest.main()
