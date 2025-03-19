import requests
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=f"plugin_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)
logger = logging.getLogger(__name__)

class Plugin:

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.auth_token: Optional[str] = None

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
            logger.info("Connectivity test passed: Authentication successful.")
            return True
        except requests.RequestException as e:
            logger.error(f"Connectivity test failed: {e}")
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
            logger.error(f"Error fetching {endpoint}: {e}")
            return {}

    def collect_evidence(self) -> List[Dict[str, Any]]:
        if not self.auth_token:
            logger.error("Cannot collect evidence: Not authenticated.")
            return []
        evidence = []
        try:
            # E1
            user_data = self._make_authenticated_request("/auth/me")
            evidence.append({"E1 - User Details": user_data})
            logger.info("Collected E1 - User Details")

            # E2
            posts_data = self._make_authenticated_request("/posts?limit=60")
            posts = posts_data.get("posts", [])
            if posts:
                evidence.append({"E2 - 60 Posts": posts})
                logger.info(f"Collected E2 - {len(posts)} Posts")

            # E3
            posts_with_comments = []
            posts = posts_data.get("posts", [])[:60]  # Use the same 60 posts
            for post in posts:
                post_id = post["id"]
                comments = self._make_authenticated_request(f"/posts/{post_id}/comments")
                post_with_comments = {**post, "comments": comments.get("comments", [])}
                posts_with_comments.append(post_with_comments)
            if posts_with_comments:
                evidence.append({"E3 - 60 Posts with Comments": posts_with_comments})
                logger.info(f"Collected E3 - {len(posts_with_comments)} Posts with Comments")
        except Exception as e:
            logger.error(f"Error during evidence collection: {e}")

        return evidence

def main():
    # Configuration
    base_url = "https://dummyjson.com"
    username = "emilys"
    password = "emilyspass"

    # Initialize plugin
    plugin = DummyJsonPlugin(base_url, username, password)

    # Test connectivity
    if not plugin.test_connectivity():
        print("Exiting due to connectivity failure.")
        return

    # Collect evidence
    evidence = plugin.collect_evidence()

    if not evidence:
        print("No evidence collected. Check logs for details.")
    else:
        for item in evidence:
            for key, value in item.items():
                if isinstance(value, list):
                    print(f"{key}: {len(value)} items")
                else:
                    print(f"{key}: {value}")

if __name__ == "__main__":
    main()