# Elliot Greenlee

from cuckoo_api_python_interface import *

# Initialize with lowest logging level
api = APIServer(logging_level=logging.DEBUG)

# Retrieve information about Cuckoo
tasks, diskspace, version, hostname, machines = api.cuckoo_status()
print("Cuckoo Status")
print("Tasks:")
print(tasks)
print("Diskspace:")
print(diskspace)
print("Version:")
print(version)
print("Hostname:")
print(hostname)
print("Machines:")
print(machines)
print()

# Retrieve information about the tasks
tasks = api.tasks_list()
print("Tasks List")
print("Tasks:")
print(tasks)
print()

# Retrieve information about the machines
machines = api.machines_list()
print("Machines List")
print("Machines:")
print(machines)
print()

task_id = api.tasks_create_file(file_path="cuckoo_project/Windows7x64/cmd.exe")
print("Task ID")
print(task_id)

# Exit the server api
api.exit()
