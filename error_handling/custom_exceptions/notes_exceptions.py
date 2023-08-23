class NotesDoesNotExist(Exception):
    default_message = "Notes does not exist"
    default_code = "Notes_does_not_exist"

    def __init__(self, specific_code=None, extra_information=None, message=None):
        self.specific_code = "10" if specific_code is None else specific_code
        self.extra_information = extra_information
        self.message = message

    def __str__(self):
        return self.default_message if self.message is None else self.message
    