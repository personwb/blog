
import exceptions


class CodeMsgException(BaseException):

    def __init__(self, code, message):
        super(CodeMsgException, self).__init__()
        self.code = code
        self.message = message


class CodeMsgEmptyException(CodeMsgException):

    def __init__(self, message):
        super(CodeMsgEmptyException, self).__init__('1001', message)