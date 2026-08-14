# Test Report: `2nn_estimator_id.py`

## Result

| Field | Value |
|---|---|
| Status | **PASS** |
| Exit code | `0` |
| Run at | `2026-08-14T10:37:31+00:00` |
| Source SHA-256 | `e6ef38414315` |
| Test SHA-256 | `2bc8a698d663` |

## Command

```text
python -m unittest -v examples/tests/test_2nn_estimator_id.py
```

## Test output

```text
Too few samples for reliable 2NN.
Using ROI experimental data
test_returns_finite_fit_for_non_degenerate_samples (examples.tests.test_2nn_estimator_id.TestCompute2NNID.test_returns_finite_fit_for_non_degenerate_samples) ... ok
test_returns_none_for_too_few_valid_neighbors (examples.tests.test_2nn_estimator_id.TestCompute2NNID.test_returns_none_for_too_few_valid_neighbors) ... ok
test_rejects_configuration_with_no_selected_dataset (examples.tests.test_2nn_estimator_id.TestMain.test_rejects_configuration_with_no_selected_dataset) ... ok
test_requires_roi_data_when_roi_mode_is_selected (examples.tests.test_2nn_estimator_id.TestMain.test_requires_roi_data_when_roi_mode_is_selected) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.002s

OK
```
