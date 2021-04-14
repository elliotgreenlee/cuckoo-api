# Elliot Greenlee
# June 24, 2017
# Oak Ridge National Laboratory

# To Do Board: Place future to dos here.
# TODO: Test functions
# TODO: Test the returns of the internal functions by printing, and especially the "nothing" ones

import requests
import logging


class APIServer:
    OPTIONAL = None

    def __init__(self, host="localhost", port="8090", logging_level=logging.WARNING):
        self.host = host
        self.port = port

        logging.basicConfig(level=logging_level)

    def build_url(self, resource):
        url = "http://{0}:{1}{2}".format(self.host, self.port, resource)
        return url

    @staticmethod
    def none_check(variable, variable_name, function_name):

        # Check variable for NoneType
        try:
            if variable is None:
                raise TypeError
        except TypeError:
            logging.warning("The {0} returned by {1} is None".format(variable_name, function_name))

        return

    # Arguments:
    # file_path TEXT: path to the sample file
    # package TEXT: analysis package to be used for the analysis
    # timeout INTEGER (in seconds): analysis timeout
    # priority INTEGER (1-3): priority to assign to the task
    # options TEXT: options to pass to the analysis package
    # machine TEXT: label of the analysis machine to use for the analysis
    # platform TEXT (e.g. "windows"): name of the platform to select the analysis machine from
    # tags TEXT: define machine to start by tags. Platform must be set to use that. Tags are comma separated
    # custom TEXT: custom string to pass over the analysis and the processing/reporting modules
    # owner TEXT: task owner in case multiple users can submit files to the same cuckoo instance
    # clock TEXT (format %m-%d-%Y %H:%M:%S): set the virtual machine clock
    # memory: enable the creation of a full memory dump of the analysis machine
    # unique: only submit samples that have not been analyzed before
    # enforce_timeout: enable to enforce the execution for the full timeout value
    #
    # Returns:
    # task_id INTEGER: id of the created task
    def tasks_create_file(self, file_path, package=OPTIONAL, timeout=OPTIONAL, priority=OPTIONAL, options=OPTIONAL,
                          machine=OPTIONAL, platform=OPTIONAL, tags=OPTIONAL, custom=OPTIONAL, owner=OPTIONAL,
                          clock=OPTIONAL, memory=OPTIONAL, unique=OPTIONAL, enforce_timeout=OPTIONAL):

        # Convert file_path to a multipart encoded file
        files = {'file': open(file_path, 'rb')}

        # Create form-encoded data of Cuckoo form parameters
        data = {
            'package': package,
            'timeout': timeout,
            'priority': priority,
            'options': options,
            'machine': machine,
            'platform': platform,
            'tags': tags,
            'custom': custom,
            'owner': owner,
            'clock': clock,
            'memory': memory,
            'unique': unique,
            'enforce_timeout': enforce_timeout
        }

        # Make the request and check status codes
        response = self.post_tasks_create_file(files, data)

        logging.debug(response.text)

        # Return created task_id
        task_id = response.json()['task_id']

        # Check returned variables for NoneType
        self.none_check(task_id, "task_id", "post_tasks_create_file()")

        return task_id

    # Arguments:
    # url TEXT: URL to analyze,
    # package TEXT: analysis package to be used for the analysis
    # timeout INTEGER (in seconds): analysis timeout
    # priority INTEGER (1-3): priority to assign to the task
    # options TEXT: options to pass to the analysis package
    # machine TEXT: label of the analysis machine to use for the analysis
    # platform TEXT (e.g. "windows"): name of the platform to select the analysis machine from
    # tags TEXT: define machine to start by tags. Platform must be set to use that. Tags are comma separated
    # custom TEXT: custom string to pass over the analysis and the processing/reporting modules
    # owner TEXT: task owner in case multiple users can submit files to the same cuckoo instance
    # memory: enable the creation of a full memory dump of the analysis machine
    # enforce_timeout: enable to enforce the execution for the full timeout value
    # clock TEXT (format %m-%d-%Y %H:%M:%S): set the virtual machine clock
    #
    # Returns:
    # task_id INTEGER: id of the created task
    def tasks_create_url(self, url, package=OPTIONAL, timeout=OPTIONAL, priority=OPTIONAL, options=OPTIONAL,
                         machine=OPTIONAL, platform=OPTIONAL, tags=OPTIONAL, custom=OPTIONAL, owner=OPTIONAL,
                         memory=OPTIONAL, enforce_timeout=OPTIONAL, clock=OPTIONAL):

        # Create form-encoded data of Cuckoo form parameters
        data = {
            'url': url,
            'package': package,
            'timeout': timeout,
            'priority': priority,
            'options': options,
            'machine': machine,
            'platform': platform,
            'tags': tags,
            'custom': custom,
            'owner': owner,
            'memory': memory,
            'enforce_timeout': enforce_timeout,
            'clock': clock
        }

        # Make the request and check status codes
        response = self.post_tasks_create_url(data)

        logging.debug(response.text)

        # Return created task_id
        task_id = response.json()['task_id']

        # Check returned variables for NoneType
        self.none_check(task_id, "task_id", "post_tasks_create_url()")

        return task_id

    # Arguments:
    # file_paths: LIST of TEXT: paths to samples to inspect and add to our pending queue
    # timeout INTEGER (in seconds): analysis timeout
    # priority INTEGER (1-3): priority to assign to the task
    # options TEXT: options to pass to the analysis package
    # tags TEXT: define machine to start by tags. Platform must be set to use that. Tags are comma separated
    # custom TEXT: custom string to pass over the analysis and the processing/reporting modules
    # owner TEXT: task owner in case multiple users can submit files to the same cuckoo instance
    # memory: enable the creation of a full memory dump of the analysis machine
    # enforce_timeout: enable to enforce the execution for the full timeout value
    # clock TEXT (format %m-%d-%Y %H:%M:%S): set the virtual machine clock
    #
    # Returns:
    # submit_id INTEGER: id of the created task group
    # tasks_ids LIST: ids of the submitted tasks
    # errors LIST: errors
    def tasks_create_submit(self, file_paths, timeout=OPTIONAL, priority=OPTIONAL, options=OPTIONAL, tags=OPTIONAL,
                            custom=OPTIONAL, owner=OPTIONAL, memory=OPTIONAL, enforce_timeout=OPTIONAL, clock=OPTIONAL):

        # Convert file_paths to multipart encoded files
        files = []
        for file_path in file_paths:
            files.append(('files', open(file_path, 'rb')))

        # Create form-encoded data of Cuckoo form parameters
        data = {
            'timeout': timeout,
            'priority': priority,
            'options': options,
            'tags': tags,
            'custom': custom,
            'owner': owner,
            'memory': memory,
            'enforce_timeout': enforce_timeout,
            'clock': clock
        }

        # Make the request and check status codes
        response = self.post_tasks_create_submit(files, data)

        logging.debug(response.text)

        submit_id = response.json()['submit_id']
        task_ids = response.json()['task_ids']
        errors = response.json()['errors']

        # Check returned variables for NoneType
        self.none_check(submit_id, "submit_id", "post_tasks_create_submit()")
        self.none_check(task_ids, "task_ids", "post_tasks_create_submit()")
        self.none_check(errors, "errors", "post_tasks_create_submit()")

        return submit_id, task_ids, errors

    # Arguments:
    # limit INTEGER: maximum number of returned tasks
    # offset INTEGER: data offset
    #
    # Returns:
    # tasks LIST of DICTIONARIES: information for each machine
    def tasks_list(self, limit=OPTIONAL, offset=OPTIONAL):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'limit': limit,
            'offset': offset
        }

        # Make the request and check status codes
        response = self.get_tasks_list(params)

        logging.debug(response.text)

        tasks = response.json()['tasks']

        # Check returned variables for NoneType
        self.none_check(tasks, "tasks", "get_tasks_list()")

        return tasks

    # Arguments:
    # id INTEGER: ID of the task to lookup
    #
    # Returns:
    # task DICTIONARY: information about the machine
    def tasks_view(self, id):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'id': id
        }

        # Make the request and check status codes
        response = self.get_tasks_view(params)

        logging.debug(response.text)

        task = response.json()['task']

        # Check returned variables for NoneType
        self.none_check(task, "task", "get_tasks_view()")

        return task

    # Arguments:
    # id INTEGER: ID of the task to reschedule
    # priority INTEGER: task priority
    #
    # Returns:
    # status TEXT: status
    def tasks_reschedule(self, id, priority=OPTIONAL):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'id': id,
            'priority': priority
        }

        # Make the request and check status codes
        response = self.get_tasks_reschedule(params)

        logging.debug(response.text)

        status = response.json()['status']

        # Check returned variables for NoneType
        self.none_check(status, "status", "get_tasks_reschedule()")

        return status

    # Arguments:
    # id INTEGER: ID of the task to delete
    #
    # Returns:
    def tasks_delete(self, id):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'id': id
        }

        # Make the request and check status codes
        response = self.get_tasks_delete(params)

        logging.debug(response.text)

        return

    # Arguments:
    # id INTEGER: ID of the task to get the report for
    # format TEXT: format of the report to retrieve [json/html/all/dropped/package_files]. If none is specified the
    #   JSON report will be returned. 'all' returns all the result files as tar.bz2, 'dropped' the dropped files as
    #   tar.bz2, 'package_files' files uploaded to host by analysis packages.
    #
    # Returns:
    def tasks_report(self, id, format=OPTIONAL):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'id': id,
            'format': format
        }

        # Make the request and check status codes
        response = self.get_tasks_report(params)

        logging.debug(response.text)

        return

    # Arguments:
    # id INTEGER: ID of the task to get the report for
    # screenshot TEXT (e.g. 0001, 0002): numerical identifier of a single screenshot
    #
    # Returns:
    def tasks_screenshots(self, id, screenshot=OPTIONAL):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'id': '{0}'.format(id),
            'screenshot': '{0}'.format(screenshot)
        }

        # Make the request and check status codes
        response = self.get_tasks_screenshots(params)

        logging.debug(response.text)

        return

    # Arguments:
    # id INTEGER: ID of the task to re-run report
    #
    # Returns:
    # success BOOLEAN: success
    def tasks_rereport(self, id):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'id': '{0}'.format(id)
        }

        # Make the request and check status codes
        response = self.get_tasks_rereport(params)

        logging.debug(response.text)

        success = response.json()['success']

        # Check returned variables for NoneType
        self.none_check(success, "success", "get_tasks_rereport()")

        return success

    # Arguments:
    # id INTEGER: ID of the task
    #
    # Returns:
    # task_id INTEGER: id of the original task
    # reboot_id INTEGER: id of the rebooted task
    def tasks_reboot(self, id):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'id': id
        }

        # Make the request and check status codes
        response = self.get_tasks_reboot(params)

        logging.debug(response.text)

        task_id = response.json()['task_id']
        reboot_id = response.json()['reboot_id']

        # Check returned variables for NoneType
        self.none_check(task_id, "task_id", "get_tasks_reboot()")
        self.none_check(reboot_id, "reboot_id", "get_tasks_reboot()")

        return task_id, reboot_id

    # Arguments:
    # id INTEGER: ID of the task to get the report for
    #
    # Returns:
    def memory_list(self, id):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'id': id
        }

        # Make the request and check status codes
        response = self.get_memory_list(params)

        logging.debug(response.text)

        return

    # Arguments:
    # id INTEGER: ID of the task to get the report for
    # pid TEXT (e.g. 205, 1908): numerical identifier (pid) of a single memory dump file
    #
    # Returns:
    def memory_get(self, id, pid):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'id': id,
            'pid': pid
        }

        # Make the request and check status codes
        response = self.get_memory_get(params)

        logging.debug(response.text)

        return

    # Arguments:
    # type TEXT (e.g. md5, sha256, id): type of identifier to use for selection
    # details TEXT: the identifier to pass on for matching
    #
    # Returns:
    def files_view(self, type, details):

        if type == "md5":
            self.files_view_md5(details)
        elif type == "sha256":
            self.files_view_sha256(details)
        elif type == "id":
            self.files_view_id(details)
        else:
            logging.error("The type passed to files_view was {0}, not 'md5', 'sha256', or 'id'. Try again."
                          .format(type))

        return

    # Arguments:
    # md5 TEXT: md5 hash to match
    #
    # Returns:
    # sample DICTIONARY: details on the matching file
    def files_view_md5(self, md5):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'md5': md5
        }

        # Make the request and check status codes
        response = self.get_files_view_md5(params)

        logging.debug(response.text)

        sample = response.json()['sample']

        # Check returned variables for NoneType
        self.none_check(sample, "sample", "files_view_md5()")

        return sample

    # Arguments:
    # sha256 TEXT: sha256 hash to match
    #
    # Returns:
    # sample DICTIONARY: details on the matching file
    def files_view_sha256(self, sha256):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'sha256': sha256
        }

        # Make the request and check status codes
        response = self.get_files_view_sha256(params)

        logging.debug(response.text)

        sample = response.json()['sample']

        # Check returned variables for NoneType
        self.none_check(sample, "sample", "files_view_sha256()")

        return sample

    # Arguments:
    # id INTEGER: id to match
    #
    # Returns:
    # sample DICTIONARY: details on the matching file
    def files_view_id(self, id):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'id': id
        }

        # Make the request and check status codes
        response = self.get_files_view_id(params)

        logging.debug(response.text)

        sample = response.json()['sample']

        # Check returned variables for NoneType
        self.none_check(sample, "sample", "files_view_id()")

        return sample

    # Arguments:
    # sha256 TEXT: sha256 hash to match
    #
    # Returns:
    def files_get(self, sha256):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'sha256': sha256
        }

        # Make the request and check status codes
        response = self.get_files_get(params)

        logging.debug(response.text)

        return

    # Arguments:
    # task INTEGER: ID for the task
    #
    # Returns:
    def pcap_get(self, task):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'task': task
        }

        # Make the request and check status codes
        response = self.get_pcap_get(params)

        logging.debug(response.text)

        return

    # Arguments:
    #
    # Returns:
    # machines LIST of DICTIONARIES: information about the machines
    def machines_list(self):

        # Make the request and check status codes
        response = self.get_machines_list()

        logging.debug(response.text)

        machines = response.json()['machines']

        # Check returned variables for NoneType
        self.none_check(machines, "machines", "machines_list()")

        return machines

    # Arguments:
    # name TEXT: name of the analysis machine
    #
    # Returns:
    # machine DICTIONARY: information about the machine
    def machines_view(self, name):

        # Create form-encoded data of Cuckoo form parameters
        params = {
            'name': name
        }

        # Make the request and check status codes
        response = self.get_machines_view(params)

        logging.debug(response.text)

        machine = response.json()['machine']

        # Check returned variables for NoneType
        self.none_check(machine, "machine", "machines_view()")

        return machine

    # Arguments:
    #
    # Returns:
    # tasks DICTIONARY: meta information about task completion
    # diskspace DICTIONARY OF DICTIONARIES: meta information about diskspace availability
    # version TEXT: version number
    # hostname TEXT: hostname
    # machines DICTIONARY: meta information about machine availability
    def cuckoo_status(self):

        # Make the request and check status codes
        response = self.get_cuckoo_status()

        logging.debug(response.text)

        tasks = response.json()['tasks']
        diskspace = response.json()['diskspace']
        version = response.json()['version']
        hostname = response.json()['hostname']
        machines = response.json()['machines']

        # Check returned variables for NoneType
        self.none_check(tasks, "tasks", "cuckoo_status()")
        self.none_check(diskspace, "diskspace", "cuckoo_status()")
        self.none_check(version, "version", "cuckoo_status()")
        self.none_check(hostname, "hostname", "cuckoo_status()")
        self.none_check(machines, "machines", "cuckoo_status()")

        return tasks, diskspace, version, hostname, machines

    # Arguments:
    #
    # Returns:
    def vpn_status(self):

        # Make the request and check status codes
        response = self.get_vpn_status()

        logging.debug(response.text)

        return

    # Arguments:
    #
    # Returns:
    def exit(self):

        # Make the request and check status codes
        response = self.get_exit()

        logging.debug(response.text)

        return

    # Adds a file to the list of pending tasks. Returns the ID of the newly created task.
    # POST /tasks/create/file
    # Returns the request response: a task id
    def post_tasks_create_file(self, files, data):

        # Status Codes
        NO_ERROR = 200
        DUPLICATED_FILE_DETECTED = 400

        # Build the REST URL
        rest_url = self.build_url("/tasks/create/file")

        # Make the request
        response = requests.post(rest_url, files=files, data=data)

        # Error checking for status_code
        if response.status_code == NO_ERROR:
            logging.info("The request from post_tasks_create_file() responded with status code {0}: "
                         "no error".format(response.status_code))
        elif response.status_code == DUPLICATED_FILE_DETECTED:
            logging.error("The request from post_tasks_create_file() responded with status code {0}: "
                          "duplicated file detected (when using unique option)".format(response.status_code))
        else:
            logging.error("The request from post_tasks_create_file() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Adds a file to the list of pending tasks. Returns the ID of the newly created task.
    # POST /tasks/create/url
    # Returns the request response: a task_id int
    def post_tasks_create_url(self, data):

        # Status Codes
        NO_ERROR = 200

        # Build the REST URL
        rest_url = self.build_url("/tasks/create/url")

        # Make the request
        response = requests.post(rest_url, data=data)

        # Error checking for status_code
        if response.status_code == NO_ERROR:
            logging.info("The request from post_tasks_create_url() responded with status code {0}: "
                         "no error".format(response.status_code))
        else:
            logging.error("The request from post_tasks_create_url() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Adds one or more files and/or files embedded in archives to the list of pending tasks. Returns the submit ID as
    # well as the task IDs of the newly create task(s).
    # POST /tasks/create/submit
    # Returns the request response: a submit_id int, a task_ids list of ints, and an errors list
    def post_tasks_create_submit(self, files, data):

        # Status Codes
        NO_ERROR = 200

        # Build REST URL
        rest_url = self.build_url("/tasks/create/submit")

        # Make the request
        response = requests.post(rest_url, files=files, data=data)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from post_tasks_create_submit() responded with status code {0}: "
                         "no error".format(response.status_code))
        else:
            logging.error("The request from post_tasks_create_submit() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns list of tasks
    # GET /tasks/list
    # Returns the request response: a tasks list of dictionaries
    def get_tasks_list(self, params):

        # Status codes:
        NO_ERROR = 200

        # Build REST URL
        resource = "/tasks/list"
        limit = params['limit']
        offset = params['offset']
        if limit is not None:
            resource += "/{0}".format(limit)
            if offset is not None:
                resource += "/{0}".format(offset)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_tasks_list() responded with status code {0}: "
                         "no error".format(response.status_code))
        else:
            logging.error("The request from get_tasks_list() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns details on the task associated with the specified ID.
    # GET /tasks/view
    # Returns the request response: a task dictionary
    def get_tasks_view(self, params):

        # Status codes:
        NO_ERROR = 200
        TASK_NOT_FOUND = 404

        # Build REST URL
        resource = "/tasks/view"
        id = params['id']
        resource += "/{0}".format(id)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_tasks_view() responded with status code {0}: "
                         "no error".format(response.status_code))
        elif response.status_code == TASK_NOT_FOUND:
            logging.error("The request from get_tasks_view() responded with status code {0}: "
                          "task not found".format(response.status_code))
        else:
            logging.error("The request from get_tasks_view() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Reschedule a task with the specified ID and priority (default priority is 1).
    # GET /tasks/reschedule
    # Returns the request response: a status string
    def get_tasks_reschedule(self, params):

        # Status codes:
        NO_ERROR = 200
        TASK_NOT_FOUND = 404

        # Build REST URL
        resource = "/tasks/reschedule"
        id = params['id']
        priority = params['priority']
        resource += "/{0}".format(id)
        if priority is not None:
            resource += "/{0}".format(priority)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_tasks_reschedule() responded with status code {0}: "
                         "no error".format(response.status_code))
        elif response.status_code == TASK_NOT_FOUND:
            logging.error("The request from get_tasks_reschedule() responded with status code {0}: "
                          "task not found".format(response.status_code))
        else:
            logging.error("The request from get_tasks_reschedule() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Removes the given task from the database and deletes the results.
    # GET /tasks/delete
    # Returns the request response: nothing
    def get_tasks_delete(self, params):

        # Status codes:
        NO_ERROR = 200
        TASK_NOT_FOUND = 404
        UNABLE_TO_DELETE_THE_TASK = 500

        # Build REST URL
        resource = "/tasks/delete"
        id = params['id']
        resource += "/{0}".format(id)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_tasks_delete() responded with status code {0}: "
                         "no error".format(response.status_code))
        elif response.status_code == TASK_NOT_FOUND:
            logging.error("The request from get_tasks_delete() responded with status code {0}: "
                          "task not found".format(response.status_code))
        elif response.status_code == UNABLE_TO_DELETE_THE_TASK:
            logging.error("The request from get_tasks_delete() responded with status code {0}: "
                          "unable to delete the task".format(response.status_code))
        else:
            logging.error("The request from get_tasks_delete() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns the report associate with the specified task ID.
    # GET /tasks/report
    # Returns the request response: nothing
    def get_tasks_report(self, params):

        # Status codes:
        NO_ERROR = 200
        INVALID_REPORT_FORMAT = 400
        REPORT_NOT_FOUND = 404

        # Build REST URL
        resource = "/tasks/report"
        id = params['id']
        format = params['format']
        resource += "/{0}".format(id)
        if format is not None:
            resource += "/{0}".format(format)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_tasks_report() responded with status code {0}: "
                         "no error".format(response.status_code))
        elif response.status_code == INVALID_REPORT_FORMAT:
            logging.error("The request from get_tasks_report() responded with status code {0}: "
                          "invalid report format".format(response.status_code))
        elif response.status_code == REPORT_NOT_FOUND:
            logging.error("The request from get_tasks_report() responded with status code {0}: "
                          "report not found".format(response.status_code))
        else:
            logging.error("The request from get_tasks_report() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns one or all screenshots associated with the specified task ID.
    # GET /tasks/screenshots
    # Returns the request response: nothing
    def get_tasks_screenshots(self, params):

        # Status codes:
        FILE_OR_FOLDER_NOT_FOUND = 404

        # Build REST URL
        resource = "/tasks/screenshots"
        id = params['id']
        screenshot = params['screenshot']
        resource += "/{0}".format(id)
        if screenshot is not None:
            resource += "/{0}".format(screenshot)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == FILE_OR_FOLDER_NOT_FOUND:
            logging.error("The request from get_tasks_screenshots() responded with status code {0}: "
                          "file or folder not found".format(response.status_code))
        else:
            logging.error("The request from get_tasks_screenshots() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Re-run reporting for task associated with the specified task ID.
    # GET /tasks/rereport
    # Returns the request response: a success boolean
    def get_tasks_rereport(self, params):

        # Status codes:
        NO_ERROR = 200
        TASK_NOT_FOUND = 404

        # Build REST URL
        resource = "/tasks/rereport"
        id = params['id']
        resource += "/{0}".format(id)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_tasks_rereport() responded with status code {0}: "
                         "no error".format(response.status_code))
        elif response.status_code == TASK_NOT_FOUND:
            logging.error("The request from get_tasks_rereport() responded with status code {0}: "
                          "task not found".format(response.status_code))
        else:
            logging.error("The request from get_tasks_rereport() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Add a reboot task to database from an existing analysis ID.
    # GET /tasks/reboot
    # Returns the request response: a task_id int and a reboot_id int
    def get_tasks_reboot(self, params):

        # Status codes:
        SUCCESS = 200
        ERROR_CREATING_REBOOT_TASK = 404

        # Build REST URL
        resource = "/tasks/reboot"
        id = params['id']
        resource += "/{0}".format(id)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == SUCCESS:
            logging.info("The request from get_tasks_reboot() responded with status code {0}: "
                         "success".format(response.status_code))
        elif response.status_code == ERROR_CREATING_REBOOT_TASK:
            logging.error("The request from get_tasks_reboot() responded with status code {0}: "
                          "error creating reboot task".format(response.status_code))
        else:
            logging.error("The request from get_tasks_reboot() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns a list of memory dump files or one memory dump file associated with the specified task ID.
    # GET /memory/list
    # Returns the request response: nothing
    def get_memory_list(self, params):

        # Status codes:
        FILE_OR_FOLDER_NOT_FOUND = 404

        # Build REST URL
        resource = "/memory/list"
        id = params['id']
        resource += "/{0}".format(id)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == FILE_OR_FOLDER_NOT_FOUND:
            logging.error("The request from get_memory_list() responded with status code {0}: "
                          "file or folder not found".format(response.status_code))
        else:
            logging.error("The request from get_memory_list() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns one memory dump file associated with the specified task ID.
    # GET /memory/get
    # Returns the request response: nothing
    def get_memory_get(self, params):

        # Status codes:
        FILE_OR_FOLDER_NOT_FOUND = 404

        # Build REST URL
        resource = "/memory/get"
        id = params['id']
        pid = params['pid']
        resource += "/{0}".format(id)
        resource += "/{0}".format(pid)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == FILE_OR_FOLDER_NOT_FOUND:
            logging.error("The request from get_memory_get() responded with status code {0}: "
                          "file or folder not found".format(response.status_code))
        else:
            logging.error("The request from get_memory_get() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns details on the file matching either the specified MD5 hash.
    # GET /files/view/md5
    # Returns the request response: a sample dictionary
    def get_files_view_md5(self, params):

        # Status codes:
        NO_ERROR = 200
        INVALID_LOOKUP_TERM = 400
        FILE_OR_FOLDER_NOT_FOUND = 404

        # Build REST URL
        resource = "/files/view/md5"
        md5 = params['md5']
        resource += "/{0}".format(md5)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_files_view_md5() responded with status code {0}: "
                         "no error".format(response.status_code))
        elif response.status_code == INVALID_LOOKUP_TERM:
            logging.error("The request from get_files_view_md5() responded with status code {0}: "
                          "invalid lookup term".format(response.status_code))
        elif response.status_code == FILE_OR_FOLDER_NOT_FOUND:
            logging.error("The request from get_files_view_md5() responded with status code {0}: "
                          "file or folder not found".format(response.status_code))
        else:
            logging.error("The request from get_files_view_md5() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns details on the file matching either the specified SHA256 hash.
    # GET /files/view/sha256
    # Returns the request response: a sample dictionary
    def get_files_view_sha256(self, params):

        # Status codes:
        NO_ERROR = 200
        INVALID_LOOKUP_TERM = 400
        FILE_OR_FOLDER_NOT_FOUND = 404

        # Build REST URL
        resource = "/files/view/sha256"
        sha256 = params['sha256']
        resource += "/{0}".format(sha256)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_files_view_sha256() responded with status code {0}: "
                         "no error".format(response.status_code))
        elif response.status_code == INVALID_LOOKUP_TERM:
            logging.error("The request from get_files_view_sha256() responded with status code {0}: "
                          "invalid lookup term".format(response.status_code))
        elif response.status_code == FILE_OR_FOLDER_NOT_FOUND:
            logging.error("The request from get_files_view_sha256() responded with status code {0}: "
                          "file or folder not found".format(response.status_code))
        else:
            logging.error("The request from get_files_view_sha256() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns details on the file matching either the specified ID.
    # GET /files/view/id
    # Returns the request response: a sample dictionary
    def get_files_view_id(self, params):

        # Status codes:
        NO_ERROR = 200
        INVALID_LOOKUP_TERM = 400
        FILE_OR_FOLDER_NOT_FOUND = 404

        # Build REST URL
        resource = "/files/view/id"
        id = params['id']
        resource += "/{0}".format(id)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_files_view_id() responded with status code {0}: "
                         "no error".format(response.status_code))
        elif response.status_code == INVALID_LOOKUP_TERM:
            logging.error("The request from get_files_view_id() responded with status code {0}: "
                          "invalid lookup term".format(response.status_code))
        elif response.status_code == FILE_OR_FOLDER_NOT_FOUND:
            logging.error("The request from get_files_view_id() responded with status code {0}: "
                          "file or folder not found".format(response.status_code))
        else:
            logging.error("The request from get_files_view_id() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns the binary content of the file matching the specified SHA256 hash.
    # GET /files/get
    # Returns the request response: nothing
    def get_files_get(self, params):

        # Status codes:
        NO_ERROR = 200
        FILE_NOT_FOUND = 404

        # Build REST URL
        resource = "/files/get"
        sha256 = params['sha256']
        resource += "/{0}".format(sha256)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_files_get() responded with status code {0}: "
                         "no error".format(response.status_code))
        elif response.status_code == FILE_NOT_FOUND:
            logging.error("The request from get_files_get() responded with status code {0}: "
                          "file not found".format(response.status_code))
        else:
            logging.error("The request from get_files_get() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns the content of the PCAP associate with the given task.
    # GET /pcap/get
    # Returns the request response: nothing
    def get_pcap_get(self, params):

        # Status codes:
        NO_ERROR = 200
        FILE_NOT_FOUND = 404

        # Build REST URL
        resource = "/pcap/get"
        task = params['task']
        resource += "/{0}".format(task)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_pcap_get() responded with status code {0}: "
                         "no error".format(response.status_code))
        elif response.status_code == FILE_NOT_FOUND:
            logging.error("The request from get_pcap_get() responded with status code {0}: "
                          "file not found".format(response.status_code))
        else:
            logging.error("The request from get_pcap_get() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns a list with details on the analysis machines available to Cuckoo.
    # GET /machines/list
    # Returns the request response: a machines list of dictionaries
    def get_machines_list(self):

        # Status codes:
        NO_ERROR = 200

        # Build REST URL
        rest_url = self.build_url("/machines/list")

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_machines_list() responded with status code {0}: "
                         "no error".format(response.status_code))
        else:
            logging.error("The request from get_machines_list() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns details on the analysis machine associate with the given name.
    # GET /machines/view
    # Returns the request response: a machine dictionary
    def get_machines_view(self, params):

        # Status codes:
        NO_ERROR = 200
        MACHINE_NOT_FOUND = 404

        # Build REST URL
        resource = "/machines/view"
        name = params['name']
        resource += "/{0}".format(name)
        rest_url = self.build_url(resource)

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_machines_view() responded with status code {0}: "
                         "no error".format(response.status_code))
        elif response.status_code == MACHINE_NOT_FOUND:
            logging.error("The request from get_machines_view() responded with status code {0}: "
                          "machine not found".format(response.status_code))
        else:
            logging.error("The request from get_machines_view() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns the status of the cuckoo server. ...
    # GET /cuckoo/status
    # Returns the request response: a tasks dictionary, a diskspace dictionary of dictionaries, a version string,
    # a protocol_version int, a hostname string, and a machines dictionary
    def get_cuckoo_status(self):

        # Status codes:
        NO_ERROR = 200
        MACHINE_NOT_FOUND = 404

        # Build REST URL
        rest_url = self.build_url("/cuckoo/status")

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == NO_ERROR:
            logging.info("The request from get_cuckoo_status() responded with status code {0}: "
                         "no error".format(response.status_code))
        elif response.status_code == MACHINE_NOT_FOUND:
            logging.error("The request from get_cuckoo_status() responded with status code {0}: "
                          "machine not found".format(response.status_code))
        else:
            logging.error("The request from get_cuckoo_status() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Returns VPN status.
    # GET /vpn/status
    # Returns the request response: nothing
    def get_vpn_status(self):

        # Status codes:
        SHOW_STATUS = 200
        NOT_AVAILABLE = 500

        # Build REST URL
        rest_url = self.build_url("/vpn/status")

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == SHOW_STATUS:
            logging.info("The request from get_vpn_status() responded with status code {0}: "
                         "show status".format(response.status_code))
        elif response.status_code == NOT_AVAILABLE:
            logging.error("The request from get_vpn_status() responded with status code {0}: "
                          "not available".format(response.status_code))
        else:
            logging.error("The request from get_vpn_status() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response

    # Shuts down the server if in debug mode and using the werkzeug server.
    # GET /exit
    # Returns the request response: nothing
    def get_exit(self):

        # Status codes:
        SUCCESS = 200
        DEBUG_MODE_REQUIRED = 403
        ERROR = 500

        # Build REST URL
        rest_url = self.build_url("/exit")

        # Make the request
        response = requests.get(rest_url)

        # Error checking for status_code.
        if response.status_code == SUCCESS:
            logging.info("The request from get_exit() responded with status code {0}: "
                         "success".format(response.status_code))
        elif response.status_code == DEBUG_MODE_REQUIRED:
            logging.error("The request from get_exit() responded with status code {0}: "
                          "this call can only be used in debug mode".format(response.status_code))
        elif response.status_code == ERROR:
            logging.error("The request from get_exit() responded with status code {0}: "
                          "error".format(response.status_code))
        else:
            logging.error("The request from get_exit() responded with status code {0}: "
                          "unknown status code".format(response.status_code))

        return response
