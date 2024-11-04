from typing import Dict, Optional, Tuple
from robocorp import workitems
from robocorp.tasks import task


def extract_person_data(payload: Dict) -> Optional[Tuple[str, str]]:
    """Extract first and last name from payload."""
    try:
        return payload["first_name"], payload["last_name"]
    except KeyError as e:
        print(f"Error: Missing required field {e}")
        return None


def process_work_item(item: workitems.Input) -> None:
    """Process a single work item."""
    try:
        if person_data := extract_person_data(item.payload):
            first_name, last_name = person_data
            print(f"First name: {first_name} - Last name: {last_name}")
            item.done()
        else:
            item.fail(
                exception_type="ValueError",
                code="INVALID_PAYLOAD",
                message="Missing required person data fields",
            )
    except Exception as e:
        item.fail(exception_type=type(e).__name__, message=str(e))


@task
def control_room_process() -> None:
    """Process work items containing person information."""
    for item in workitems.inputs:
        process_work_item(item)
