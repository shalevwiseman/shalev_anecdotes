import requests
from typing import Dict, List, Any

class Plugin:

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.auth_token = None

    def test_connectivity(self) -> bool:
        raise NotImplementedError("Subclasses must implement test_connectivity")

    def collect_evidence(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("Subclasses must implement collect_evidence")


class DummyJsonPlugin(Plugin):

    def test_connectivity(self) -> bool:

        url = f"{self.base_url}/auth/login"
        payload = {"username": self.username, "password": self.password}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            self.auth_token = data.get("accessToken")
            print("Connectivity test passed: Authentication successful.")
            return True
        except requests.RequestException as e:
            print(f"Connectivity test failed: {e}")
            return False