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

    def _make_authenticated_request(self, endpoint: str) -> Dict[str, Any]:
        if not self.auth_token:
            raise ValueError("Not authenticated. Run test_connectivity first.")
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching {endpoint}: {e}")
            return {}

    def collect_evidence(self) -> List[Dict[str, Any]]:
        evidence = []

        # E1
        user_data = self._make_authenticated_request("/auth/me")
        evidence.append({"E1 - User Details": user_data})

        # E2
        posts_data = self._make_authenticated_request("/posts?limit=60")
        evidence.append({"E2 - 60 Posts": posts_data.get("posts", [])})

        # E3
        posts_with_comments = []
        posts = posts_data.get("posts", [])[:60]  # Use the same 60 posts
        for post in posts:
            post_id = post["id"]
            comments = self._make_authenticated_request(f"/posts/{post_id}/comments")
            post_with_comments = {**post, "comments": comments.get("comments", [])}
            posts_with_comments.append(post_with_comments)
        evidence.append({"E3 - 60 Posts with Comments": posts_with_comments})

        return evidence