import json, tempfile, unittest
from pathlib import Path
from miilab.trainer import read_rows, train, predict
from miilab.simulation import PROFILES, simulate

class PipelineTests(unittest.TestCase):
    def test_dataset_has_seven_principle_labels(self):
        rows = read_rows("datasets/principle_intents.jsonl")
        self.assertEqual(len(rows), 28)
        self.assertEqual(len({r["label"] for r in rows}), 7)

    def test_training_produces_classifier_not_llm(self):
        rows = read_rows("datasets/principle_intents.jsonl")
        model = train(rows)
        self.assertEqual(model["algorithm"], "multinomial_naive_bayes")
        self.assertEqual(model["document_count"], 28)
        self.assertNotIn("weights", model)

    def test_prediction_is_a_known_label(self):
        model = train(read_rows("datasets/principle_intents.jsonl"))
        result = predict(model, "verify the evidence and admit uncertainty")
        self.assertIn(result, model["labels"])

    def test_simulation_is_explicitly_not_physical_hardware(self):
        for name in PROFILES:
            result = simulate(name, jobs=12, seed=42)
            self.assertEqual(result["evidence_class"], "SIMULATION")
            self.assertFalse(result["physical_hardware_provisioned"])
            self.assertGreater(result["simulated_ticks"], 0)

    def test_infinity_is_a_simulation_profile_not_infinite_speed(self):
        p = PROFILES["infinity_space_server"]
        self.assertIsNone(p["slots"])
        self.assertEqual(p["units_per_tick"], 1000)

if __name__ == "__main__":
    unittest.main()
