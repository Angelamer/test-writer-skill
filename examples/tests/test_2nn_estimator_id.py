import importlib.util
import unittest
from pathlib import Path
from unittest import mock

import numpy as np


SOURCE = Path(__file__).parents[1] / "2nn_estimator_id.py"
SPEC = importlib.util.spec_from_file_location("two_nn_estimator", SOURCE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TestCompute2NNID(unittest.TestCase):
    def test_returns_none_for_too_few_valid_neighbors(self):
        points = np.arange(20, dtype=float).reshape(-1, 1)
        self.assertIsNone(MODULE.compute_2nn_id(points))

    def test_returns_finite_fit_for_non_degenerate_samples(self):
        points = np.random.default_rng(7).normal(size=(200, 3))
        dimension, x, y = MODULE.compute_2nn_id(points)
        self.assertTrue(np.isfinite(dimension))
        self.assertTrue(np.all(np.isfinite(x)))
        self.assertTrue(np.all(np.isfinite(y)))
        self.assertGreater(dimension, 0)


class TestMain(unittest.TestCase):
    def test_rejects_configuration_with_no_selected_dataset(self):
        bundle = {"Z_sim": np.ones((60, 2)), "Z_roi": np.ones((60, 2))}
        with mock.patch.object(
            MODULE.joblib, "load", return_value=bundle
        ), mock.patch.object(MODULE, "USE_SIMULATED", False), mock.patch.object(
            MODULE, "USE_EXPERIMENTAL", False
        ):
            with self.assertRaisesRegex(RuntimeError, "No dataset selected"):
                MODULE.main()

    def test_requires_roi_data_when_roi_mode_is_selected(self):
        bundle = {"Z_sim": np.ones((60, 2)), "Z_roi": None}
        with mock.patch.object(
            MODULE.joblib, "load", return_value=bundle
        ), mock.patch.object(MODULE, "USE_SIMULATED", False), mock.patch.object(
            MODULE, "USE_EXPERIMENTAL", True
        ), mock.patch.object(
            MODULE, "USE_ROI_ONLY", True
        ):
            with self.assertRaisesRegex(RuntimeError, "Z_exp_roi not found"):
                MODULE.main()


if __name__ == "__main__":
    unittest.main()
