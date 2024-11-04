# Assistant Process Trigger Example

Simple example demonstrates how to create an Assistant UI that triggers a Control Room process with input parameters.

## Prerequisites

* Global variables `DOMAIN` and `SECRET_NAME` updated in `tasks.py` file to match your use case
* Target process created to the Control Room
* Vault secret containing:
  ```json
  {
    "workspace_id": "your-workspace-id",
    "process_id": "your-process-id",
    "api_key": "your-api-key"
  }
  ```