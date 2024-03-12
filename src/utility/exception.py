""" this file contain import exception class created for internal use """


class SpacyError(Exception):
    """ base64 decode error exception """

    def __init__(self, value):
        Exception.__init__(self, value)
        self.msg = value

    def __str__(self):
        return repr(self.msg)


class APIError(Exception):
    """ base64 encode error exception """

    def __init__(self, value):
        Exception.__init__(self, value)
        self.msg = value

    def __str__(self):
        return repr(self.msg)

