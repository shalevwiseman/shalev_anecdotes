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