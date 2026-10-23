import unittest

import numpy as np

from src.run_qkd_simulation import simulate_bb84


class TestBB84Simulation(unittest.TestCase):
    def test_ideal_channel_agrees_on_sifted_key(self):
        np.random.seed(17)
        qber, agreement = simulate_bb84(num_qubits=1000, num_trials=20)

        self.assertEqual(qber, 0.0)
        self.assertEqual(agreement, 1.0)

    def test_intercept_resend_exceeds_abort_threshold(self):
        np.random.seed(17)
        qber, agreement = simulate_bb84(
            num_qubits=1000,
            num_trials=100,
            eve_present=True,
        )

        self.assertGreater(qber, 0.10)
        self.assertLess(agreement, 1.0)


if __name__ == "__main__":
    unittest.main()
