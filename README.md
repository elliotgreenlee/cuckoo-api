# cuckoo_api_python_interface

Simple Python interface for the Cuckoo Sandbox API found here http://docs.cuckoosandbox.org/en/latest/usage/api/#.
"Cuckoo provides a simple and lightweight REST API server that is under the hood implemented using FLASK." The server is
started by simply typing cuckoo api. This interface is intended to be a simple starting place for those controlling
Cuckoo through Python.

## POST
* /tasks/create/file	Adds a file to the list of pending tasks to be processed and analyzed.
* /tasks/create/url	Adds an URL to the list of pending tasks to be processed and analyzed.
* /tasks/create/submit	Adds one or more files and/or files embedded in archives to the list of pending tasks.

## GET
* /tasks/list	Returns the list of tasks stored in the internal Cuckoo database. You can optionally specify a limit of entries to return.
* /tasks/view	Returns the details on the task assigned to the specified ID.
* /tasks/reschedule	Reschedule a task assigned to the specified ID.
* /tasks/delete	Removes the given task from the database and deletes the results.
* /tasks/report	Returns the report generated out of the analysis of the task associated with the specified ID. You can optionally specify which report format to return, if none is specified the JSON report will be returned.
* /tasks/screenshots	Retrieves one or all screenshots associated with a given analysis task ID.
* /tasks/rereport	Re-run reporting for task associated with a given analysis task ID.
* /tasks/reboot	Reboot a given analysis task ID.
* /memory/list	Returns a list of memory dump files associated with a given analysis task ID.
* /memory/get	Retrieves one memory dump file associated with a given analysis task ID.
* /files/view	Search the analyzed binaries by MD5 hash, SHA256 hash or internal ID (referenced by the tasks details).
* /files/get	Returns the content of the binary with the specified SHA256 hash.
* /pcap/get	Returns the content of the PCAP associated with the given task.
* /machines/list	Returns the list of analysis machines available to Cuckoo.
* /machines/view	Returns details on the analysis machine associated with the specified name.
* /cuckoo/status	Returns the basic cuckoo status, including version and tasks overview.
* /vpn/status	Returns VPN status.
* /exit	Shuts down the API server.

### Error Codes
Error codes are not standard between resources, so each one is declared in the appropriate function.

### URLs
The REST URL is also included in each function separately. They can also be used through curl.
The default base is 'http://localhost:8090', but this can be changed using the --host or -H and --port and -p options.







