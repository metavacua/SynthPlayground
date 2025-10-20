"""
A standardized client for interacting with external agent APIs.
"""

import os
import json
import requests


class ExternalApiClient:
    def __init__(self, api_name, api_key_env_var):
        self.api_name = api_name
        self.api_key = os.environ.get(api_key_env_var)
        self.base_url = self._get_base_url()

    def _get_base_url(self):
        """
        Retrieves the base URL for the API from the external API registry.
        """
        registry_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "knowledge_core",
            "external_api_registry.json",
        )
        with open(registry_path, "r") as f:
            registry = json.load(f)
        return registry[self.api_name]["endpoint"]

    def post(self, endpoint, data):
        """
        Sends a POST request to the specified endpoint.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint, params=None):
        """
        Sends a GET request to the specified endpoint.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
