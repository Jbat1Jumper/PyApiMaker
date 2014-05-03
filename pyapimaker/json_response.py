from json import dumps as json_encode
from json import loads as json_decode
from .json_encoder import ObjectJsonEncoder


class JsonResponse(str):

    def __new__(self, had_errors=False, content=None,
                error_code=0, error_desc=""):
        rDict = {}
        rDict["had_errors"] = had_errors
        rDict["content"] = content
        rDict["error_code"] = error_code
        rDict["error_desc"] = error_desc
        self.result = rDict
        self.json = json_encode(rDict, sort_keys=True, indent=4,
                                cls=ObjectJsonEncoder)
        return self.json


class ErrorResponse(JsonResponse):

    def __new__(self, error_code=0, error_desc=""):
        return JsonResponse(had_errors=True, error_code=error_code,
                            error_desc=error_desc)


class GoodResponse(JsonResponse):

    def __new__(self, content=None):
        return JsonResponse(content=content, error_desc="OK")


class RemoteResponse():

    def __init__(self, data):
        try:
            self._fill_self(data)
        except Exception as e:
            self._fill_errorstate(e)

    def _fill_self(self, data):
        d = json_decode(data)
        self.had_errors = d["had_errors"]
        self.content = d["content"]
        self.error_code = d["error_code"]
        self.error_desc = d["error_desc"]

    def _fill_errorstate(self, e):
        self.content = None
        self.had_errors = True
        self.error_code = 6
        self.error_desc = repr(e)
