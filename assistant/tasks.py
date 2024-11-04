import requests
from typing import Dict, Any
from robocorp import vault
from robocorp.tasks import task
from RPA.Assistant import Assistant
from RPA.Assistant.types import WindowLocation

DOMAIN = "cloud.robocorp.com"  # In SSO organization change domain to e.g. company.robocorp.com
SECRET_NAME = "AssistantSecrets"  # Control Room Vault name


def get_process_config(secret_name: str = SECRET_NAME) -> Dict[str, str]:
    """Get process configuration from vault secrets."""
    return vault.get_secret(secret_name)


class ProcessTriggerUI:
    """UI management for process trigger assistant."""

    def __init__(self):
        self.assistant = Assistant()
        self.config = get_process_config()

    def trigger_process_run(self, first_name: str, last_name: str) -> Dict[str, Any]:
        """Trigger a Control Room process run with the given parameters."""
        try:
            response = requests.post(
                f"https://{DOMAIN}/api/v1/workspaces/{self.config['workspace_id']}/processes/{self.config['process_id']}/process-runs",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"RC-WSKEY {self.config['api_key']}",
                },
                json={
                    "type": "with_payloads",
                    "payloads": [{"first_name": first_name, "last_name": last_name}],
                },
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to trigger process: {str(e)}"}

    def show_input_form(self) -> None:
        """Display the input form for user data."""
        self.assistant.clear_dialog()
        self.assistant.add_heading("Enter Information")
        self.assistant.add_text_input(
            name="first_name", label="First Name", placeholder="Enter first name"
        )
        self.assistant.add_text_input(
            name="last_name", label="Last Name", placeholder="Enter last name"
        )
        self.assistant.add_next_ui_button(
            "Submit and trigger the process", self.handle_submit
        )

    def show_results(self, result: Dict[str, Any]) -> None:
        """Display the results of the process trigger."""
        self.assistant.clear_dialog()
        self.assistant.add_heading("Submitted Data")

        if "error" in result:
            self.assistant.add_text("Error occurred:")
            self.assistant.add_text(result["error"], "error")
        else:
            self.assistant.add_text("The following process run has been triggered:")
            self.assistant.add_text(str(result))

        self.assistant.add_next_ui_button("Back to Form", self.back_to_form)
        self.assistant.refresh_dialog()

    def handle_submit(self, form_data: Dict[str, str]) -> None:
        """Handle form submission and trigger the process."""
        result = self.trigger_process_run(
            form_data["first_name"], form_data["last_name"]
        )
        self.show_results(result)

    def back_to_form(self, _: Dict) -> None:
        """Return to the input form."""
        self.show_input_form()
        self.assistant.refresh_dialog()

    def run(self) -> None:
        """Run the assistant dialog."""
        self.show_input_form()
        self.assistant.run_dialog(
            timeout=600,
            title="Trigger a process",
            location=WindowLocation.Center,
        )


@task
def assistant_trigger_process() -> None:
    """Main task to run the process trigger assistant."""
    ui = ProcessTriggerUI()
    ui.run()
