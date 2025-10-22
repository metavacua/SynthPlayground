"""
A standardized client for interacting with external agent APIs.
"""

import os
import json
import requests
import subprocess


class ExternalApiClient:
    def __init__(self, api_name):
        self.api_name = api_name
        self._load_registry()

        api_type = self.api_config.get("type")
        if api_type == "command_line":
            self.command = self.api_config["command"]
        else:  # Assumes web API
            self.api_key_env_var = self.api_config.get("api_key_env_var")
            if self.api_key_env_var:
                self.api_key = os.environ.get(self.api_key_env_var)
            else:
                self.api_key = None
            self.base_url = self.api_config["endpoint"]

    def _load_registry(self):
        """
        Loads the external API registry and gets the config for this API.
        """
        registry_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "knowledge_core",
            "external_api_registry.json",
        )
        with open(registry_path, "r") as f:
            registry = json.load(f)
        self.api_config = registry[self.api_name]

    def post(self, endpoint, data):
        """
        Sends a POST request to the specified endpoint.
        """
        if self.api_config.get("type") == "command_line":
            raise NotImplementedError(
                "POST requests are not supported for command-line tools."
            )

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint, params=None):
        """
        Sends a GET request to the specified endpoint.
        """
        if self.api_config.get("type") == "command_line":
            raise NotImplementedError(
                "GET requests are not supported for command-line tools."
            )

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def execute(self, args):
        """
        Executes a command-line tool with the given arguments.
        """
        if self.api_config.get("type") != "command_line":
            raise NotImplementedError(
                "Execute is only supported for command-line tools."
            )

        full_command = self.command.split() + args
        result = subprocess.run(full_command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Command failed with error: {result.stderr}")
        return result.stdout
