# Test Report: `2nn_estimator_id.py`

## Result

| Field | Value |
|---|---|
| Status | **FAIL** |
| Exit code | `1` |
| Run at | `2026-08-14T10:24:11+00:00` |
| Source SHA-256 | `9e585b6ff6eb` |
| Test SHA-256 | `2bc8a698d663` |

## Command

```text
python -m unittest -v examples/tests/test_2nn_estimator_id.py
```

## Test output

```text
Too few samples for reliable 2NN.
Using ROI experimental data
test_returns_finite_fit_for_non_degenerate_samples (examples.tests.test_2nn_estimator_id.TestCompute2NNID.test_returns_finite_fit_for_non_degenerate_samples) ... /Users/kikizhang/project/python_unittests/test-writer-skill/examples/2nn_estimator_id.py:38: RuntimeWarning: divide by zero encountered in log
  y = -np.log(1 - empirical_cdf)
FAIL
test_returns_none_for_too_few_valid_neighbors (examples.tests.test_2nn_estimator_id.TestCompute2NNID.test_returns_none_for_too_few_valid_neighbors) ... ok
test_rejects_configuration_with_no_selected_dataset (examples.tests.test_2nn_estimator_id.TestMain.test_rejects_configuration_with_no_selected_dataset) ... ok
test_requires_roi_data_when_roi_mode_is_selected (examples.tests.test_2nn_estimator_id.TestMain.test_requires_roi_data_when_roi_mode_is_selected) ... ok

======================================================================
FAIL: test_returns_finite_fit_for_non_degenerate_samples (examples.tests.test_2nn_estimator_id.TestCompute2NNID.test_returns_finite_fit_for_non_degenerate_samples)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/kikizhang/project/python_unittests/test-writer-skill/examples/tests/test_2nn_estimator_id.py", line 23, in test_returns_finite_fit_for_non_degenerate_samples
    self.assertTrue(np.isfinite(dimension))
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: np.False_ is not true

----------------------------------------------------------------------
Ran 4 tests in 0.002s

FAILED (failures=1)
```

## Assessment

Three behaviors pass: insufficient samples return `None`, an empty dataset selection is rejected, and missing ROI data is rejected. The normal numerical path fails because `empirical_cdf` includes exactly `1.0`; consequently, `-log(1 - empirical_cdf)` evaluates to infinity for its final element. `numpy.polyfit` then returns a non-finite dimension.

The production code should use a plotting position strictly below one (for example, ranks divided by `N + 1`) or exclude the terminal CDF point before the logarithm and fit. Add validation for input shape and minimum sample count before requesting three neighbors as a follow-up hardening step.
