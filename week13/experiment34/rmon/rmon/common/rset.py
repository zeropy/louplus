
class RsetException(BaseException):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super(RsetException,self).__init__()


