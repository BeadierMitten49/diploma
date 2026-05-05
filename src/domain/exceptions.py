class TaskError(Exception):
    pass


class InvalidTaskStatusError(TaskError):
    pass


class EmployeePermissionError(TaskError):
    pass
