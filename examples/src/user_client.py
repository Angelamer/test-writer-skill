# src/user_client.py

import requests


class UserClient:
    def __init__(self, base_url: str, timeout: float = 5.0):
        if not base_url:
            raise ValueError("base_url is required")

        if timeout <= 0:
            raise ValueError("timeout must be positive")

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_user(self, user_id: int) -> dict:
        if user_id <= 0:
            raise ValueError("user_id must be positive")

        response = requests.get(
            f"{self.base_url}/users/{user_id}",
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            raise ValueError("invalid response format")

        if "id" not in data or "name" not in data:
            raise ValueError("missing required user fields")

        return data
