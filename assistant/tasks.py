import requests
from robocorp import vault
from robocorp.tasks import task
from RPA.Assistant import Assistant
from RPA.Assistant.types import WindowLocation

assistant = Assistant()


def trigger_the_process_run(first_name, last_name):
    secrets = vault.get_secret("AssistantSecrets")
    result = requests.request(
        "post",
        f"https://cloud.robocorp.com/api/v1/workspaces/{secrets['workspace_id']}/processes/{secrets['process_id']}/process-runs",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"RC-WSKEY {secrets['api_key']}",
        },
        json={
            "type": "with_payloads",
            "payloads": [{"first_name": first_name, "last_name": last_name}],
        },
    )
    return result.json()


@task
def assistant_trigger_process():
    show_input_form()
    assistant.run_dialog(
        title="Trigger a process",
        location=WindowLocation.Center,
    )


def show_input_form():
    assistant.clear_dialog()
    assistant.add_heading("Enter Information")

    assistant.add_text_input(
        name="first_name", label="First Name", placeholder="Enter first name"
    )

    assistant.add_text_input(
        name="last_name", label="Last Name", placeholder="Enter last name"
    )

    assistant.add_next_ui_button("Submit and trigger the process", handle_submit)


def handle_submit(form_data: dict):
    result = trigger_the_process_run(form_data["first_name"], form_data["last_name"])
    show_results(result)


def back_to_form(data: dict):
    show_input_form()
    assistant.refresh_dialog()


def show_results(result):
    assistant.clear_dialog()
    assistant.add_heading("Submitted Data")
    assistant.add_text("The following process run has been triggererd:")
    assistant.add_text(result)

    assistant.add_next_ui_button("Back to Form", back_to_form)
    assistant.refresh_dialog()
