''' Module containing the app's error classes '''

class AppError(Exception):
    def __init__(self, error_type="AppError", description="Unhandled Error", logger_output=None):
        super().__init__(description)
        self._error_type = error_type
        self._description = description
        self._logger_output = logger_output
        
    def to_string(self):
        return f"{self._error_type}: {self._description}"

    def get_logger_output(self):
        return self._logger_output

class AppLoadError(AppError):
    def __init__(self, description, logger_output=None):
        super().__init__("AppLoadError", description, logger_output)

class LoadModelFailedError(AppError):
    def __init__(self, description, logger_output=None):
        super().__init__("LoadModelFailedError", description, logger_output)

class TrainModelFailedError(AppError):
    def __init__(self, description, logger_output=None):
        super().__init__("TrainModelFailedError", description, logger_output)

class TrainingFileLoadError(AppError):
    def __init__(self, description, logger_output=None):
        super().__init__("TrainingFileLoadError", description, logger_output)


