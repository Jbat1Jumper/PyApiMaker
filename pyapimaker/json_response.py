from json import dumps as parse2json
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
        self.json = parse2json(rDict, sort_keys=True, indent=4,
                               cls=ObjectJsonEncoder)
        return self.json


class ErrorResponse(JsonResponse):

    def __new__(self, error_code=0, error_desc=""):
        return JsonResponse(had_errors=True, error_code=error_code,
                            error_desc=error_desc)


class GoodResponse(JsonResponse):

    def __new__(self, content=None):
        return JsonResponse(content=content)
