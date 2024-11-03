from robocorp import workitems
from robocorp.tasks import task


@task
def control_room_process():
    for item in workitems.inputs:
        first_name = item.payload["first_name"]
        last_name = item.payload["last_name"]
        print(f"First name: {first_name} - Last name: {last_name}")
        item.done()
