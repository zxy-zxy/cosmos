class BadResponseException(Exception):
    """A response from API is not correct"""


class RequiredFieldIsMissingException(Exception):
    def __init__(self, field_name):
        self.message = f'Response cannot be parsed properly:' \
                       f' field {field_name} is missing.'

    def __str__(self):
        return self.message