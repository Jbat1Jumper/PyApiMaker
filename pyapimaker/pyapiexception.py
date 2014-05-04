

class PyApiException(Exception):

    def __init__(self, code, desc=""):
        super().__init__(self, desc)
        self.error_desc = desc
        self.error_code = code

    def __repr__(self):
        return "PyApiException {} {}".format(self.error_code, self.error_desc)
