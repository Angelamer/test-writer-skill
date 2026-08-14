# Test Report: `2nn_estimator_id.py`

## Result

| Field | Value |
|---|---|
| Status | **PASS** |
| Exit code | `0` |
| Run at | `2026-08-14T11:36:19+00:00` |
| Source SHA-256 | `e6ef38414315` |
| Test SHA-256 | `2bc8a698d663` |
| Target source coverage | 57.1% (42/71 lines) |
| HTML coverage | [Open annotated source](https://angelamer.github.io/test-writer-skill/) |
| Commit | `5052bf341f21` |
| CI | local run |

## Target Source Coverage Details

- **Covered lines:** 1, 3-6, 9, 11-13, 16-19, 21-24, 26-28, 30, 34-35, 37-41, 44-48, 50, 54-58, 67-68, 91
- **Missing lines:** 31-32, 51-52, 59, 61-65, 70-75, 77-88, 92
- **Missing branches:** 30 -> 31, 50 -> 51, 55 -> 61, 57 -> 59, 63 -> 64, 63 -> 65, 67 -> 70, 73 -> 74, 73 -> 77, 91 -> 92

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
