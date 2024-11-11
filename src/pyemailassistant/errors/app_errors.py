''' Module containing the app's error classes '''

class AppError(Exception):
    
    ''' 
        Base class for application errors

        Attributes:
            error_type (str)
            description (str)
            logger_output (str)
    '''

    def __init__(self, error_type="AppError", description="Unhandled Error", logger_output=None):
        super().__init__(description)
        self._error_type = error_type
        self._logger_output = logger_output
        
    def to_string(self):
        return f"{self._error_type}: {self.args[0]}"

    def get_logger_output(self):
        return self._logger_output

class AppLoadError(AppError):
    def __init__(self, description, logger_output=None):
        super().__init__("AppLoadError", description, logger_output)

class InputValidationError(AppError):
    def __init__(self, description, logger_output=None):
        super().__init__("InputValidationError", description, logger_output)

class ModelLoadError(AppError):
    def __init__(self, description, logger_output=None):
        super().__init__("ModelLoadError", description, logger_output)

class ModelPredictionError(AppError):
    def __init__(self, description, logger_output=None):
        super().__init__("ModelPredictionError", description, logger_output)

class TrainingFileLoadError(AppError):
    def __init__(self, description, logger_output=None):
        super().__init__("TrainingFileLoadError", description, logger_output)


