"""This module contains custom exceptions."""

class APIError(BaseException):
    """Thsi exception raised when an API call fails."""
    def __init__(self, response):
        route = response.request.url
        method = response.request.method
        status_code = response.status_code
        message = response.text

        self.message = (f"API call to {route} with method {method} failed with "
                        f"status code {status_code} and message: {message}.\n"
                        f"Request data: {response.request.body}")
        super().__init__(self.message)

class ConfigurationError(BaseException):
    """This exception is raised when the configuration file is not properly set up."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
