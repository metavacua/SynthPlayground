{
  "rules": [
    {
      "id": "FORBID_FILE_CREATION",
      "description": "Forbid file creation in this directory. This rule is for testing agent protocol adherence.",
      "effect": "deny",
      "tool_name": [
        "create_file_with_block"
      ]
    }
  ]
}