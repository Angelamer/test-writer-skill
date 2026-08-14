import importlib.util
import unittest
from pathlib import Path
from unittest import mock

import requests


SOURCE = Path(__file__).parents[1] / "src" / "user_client.py"
SPEC = importlib.util.spec_from_file_location("user_client", SOURCE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
UserClient = MODULE.UserClient


class TestUserClientInitialization(unittest.TestCase):
    def test_normalizes_trailing_slashes_and_preserves_timeout(self):
        client = UserClient("https://api.example.test///", timeout=2.5)
        self.assertEqual(client.base_url, "https://api.example.test")
        self.assertEqual(client.timeout, 2.5)

    def test_rejects_empty_base_url(self):
        with self.assertRaisesRegex(ValueError, "base_url is required"):
            UserClient("")

    def test_rejects_non_positive_timeout(self):
        for timeout in (0, -0.1):
            with self.subTest(timeout=timeout):
                with self.assertRaisesRegex(ValueError, "timeout must be positive"):
                    UserClient("https://api.example.test", timeout=timeout)


class TestGetUser(unittest.TestCase):
    def setUp(self):
        self.client = UserClient("https://api.example.test/", timeout=3.0)

    @mock.patch.object(MODULE.requests, "get")
    def test_returns_valid_user_and_uses_configured_request(self, get):
        expected = {"id": 42, "name": "Ada"}
        response = get.return_value
        response.json.return_value = expected

        result = self.client.get_user(42)

        self.assertIs(result, expected)
        get.assert_called_once_with("https://api.example.test/users/42", timeout=3.0)
        response.raise_for_status.assert_called_once_with()
        response.json.assert_called_once_with()

    @mock.patch.object(MODULE.requests, "get")
    def test_rejects_non_positive_user_id_without_network_call(self, get):
        for user_id in (0, -1):
            with self.subTest(user_id=user_id):
                with self.assertRaisesRegex(ValueError, "user_id must be positive"):
                    self.client.get_user(user_id)
        get.assert_not_called()

    @mock.patch.object(MODULE.requests, "get")
    def test_propagates_http_error_before_reading_json(self, get):
        response = get.return_value
        response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

        with self.assertRaises(requests.HTTPError):
            self.client.get_user(99)

        response.json.assert_not_called()

    @mock.patch.object(MODULE.requests, "get")
    def test_propagates_json_decoding_error(self, get):
        get.return_value.json.side_effect = ValueError("invalid JSON")

        with self.assertRaisesRegex(ValueError, "invalid JSON"):
            self.client.get_user(1)

    @mock.patch.object(MODULE.requests, "get")
    def test_rejects_non_object_response(self, get):
        get.return_value.json.return_value = [{"id": 1, "name": "Ada"}]

        with self.assertRaisesRegex(ValueError, "invalid response format"):
            self.client.get_user(1)

    @mock.patch.object(MODULE.requests, "get")
    def test_rejects_missing_required_fields(self, get):
        for payload in ({"id": 1}, {"name": "Ada"}, {}):
            with self.subTest(payload=payload):
                get.return_value.json.return_value = payload
                with self.assertRaisesRegex(ValueError, "missing required user fields"):
                    self.client.get_user(1)


if __name__ == "__main__":
    unittest.main()
