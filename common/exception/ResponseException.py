
import exceptions


class ResponseException(BaseException):

    def __init__(self, response):
        super(ResponseException, self).__init__()
        self.response = response
