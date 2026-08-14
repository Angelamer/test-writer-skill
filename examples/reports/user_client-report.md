# Test Report: `user_client.py`

## Result

| Field | Value |
|---|---|
| Status | **PASS** |
| Exit code | `0` |
| Run at | `2026-08-14T12:30:26+00:00` |
| Source SHA-256 | `8861dc932f0c` |
| Test SHA-256 | `d0ffd939f9f7` |
| Target source coverage | 100.0% (20/20 lines) |
| HTML coverage | [Open annotated source](https://angelamer.github.io/test-writer-skill/) |
| Commit | `b423338e075a` |
| CI | local run |

## Target Source Coverage Details

- **Covered lines:** 3, 6-9, 11-12, 14-15, 17-19, 21, 26, 28, 30-31, 33-34, 36
- **Missing lines:** none
- **Missing branches:** none

## Command

```text
python -m unittest -v examples/tests/test_user_client.py
```

## Test output

```text
test_propagates_http_error_before_reading_json (examples.tests.test_user_client.TestGetUser.test_propagates_http_error_before_reading_json) ... ok
test_propagates_json_decoding_error (examples.tests.test_user_client.TestGetUser.test_propagates_json_decoding_error) ... ok
test_rejects_missing_required_fields (examples.tests.test_user_client.TestGetUser.test_rejects_missing_required_fields) ... ok
test_rejects_non_object_response (examples.tests.test_user_client.TestGetUser.test_rejects_non_object_response) ... ok
test_rejects_non_positive_user_id_without_network_call (examples.tests.test_user_client.TestGetUser.test_rejects_non_positive_user_id_without_network_call) ... ok
test_returns_valid_user_and_uses_configured_request (examples.tests.test_user_client.TestGetUser.test_returns_valid_user_and_uses_configured_request) ... ok
test_normalizes_trailing_slashes_and_preserves_timeout (examples.tests.test_user_client.TestUserClientInitialization.test_normalizes_trailing_slashes_and_preserves_timeout) ... ok
test_rejects_empty_base_url (examples.tests.test_user_client.TestUserClientInitialization.test_rejects_empty_base_url) ... ok
test_rejects_non_positive_timeout (examples.tests.test_user_client.TestUserClientInitialization.test_rejects_non_positive_timeout) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.002s

OK
```
