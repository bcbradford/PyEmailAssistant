''' Module containing the app's error class definitions '''

class AppError(Exception):
    def __init__(self, error_type: str, error_description: str, logger_output=None):
        super().__init__(description)
        self.__error_type = error_type
        self.__error_description = error_description
        self.__logger_output = logger_output

    def to_dict(self):
        error_info = {
                "type": self.__error_type,
                "description": self.__error_description
        }

        return error_info

    def get_logger_output(self):
        return self.__logger_output
