# Elliot Greenlee

from cuckoo_api_python_interface import *

# Initialize with lowest logging level
api = APIServer(logging_level=logging.DEBUG)

print("\ntasks_create_file()")
api.tasks_create_file(file_path="cuckoo_project/Windows7x64/cmd.exe")

print("\ntasks_create_url()")
api.tasks_create_url(url="http://www.google.com")

print("\ntasks_create_submit()")
api.tasks_create_submit(file_paths=["cuckoo_project/Windows7x64/cmd.exe", "cuckoo_project/Windows7x64/cmd.exe"])

print("\ntasks_list()")
api.tasks_list()

print("\ntasks_view()")
api.tasks_view(id=1)

print("\ntasks_reschedule()")
api.tasks_reschedule(id=2)

print("\ntasks_delete()")
api.tasks_delete(id=3)

print("\ntasks_report()")
api.tasks_report(id=1)

print("\ntasks_screenshots()")
api.tasks_screenshots(id=1)

print("\ntasks_rereport()")
api.tasks_rereport(id=1)

print("\ntasks_reboot()")
api.tasks_reboot(id=2)

print("\nmemory_list()")
api.memory_list(id=1)

print("\nmemory_get()")
api.memory_get(id=1, pid=205)  # What is an actual pid to use

print("\nfiles_view()")
api.files_view(type="id", details=1)

print("\nfiles_get()")
api.files_get(sha256="")  # What is an actual sha256

print("\npcap_get()")
api.pcap_get(task=1)

print("\nmachines_list()")
api.machines_list()

print("\nmachines_view()")
api.machines_view(name="Windows7x64")  # What is the actual machine name

print("\ncuckoo_status()")
api.cuckoo_status()

print("\nvpn_status()")
api.vpn_status()

print("\nexit()")
api.exit()
