from json import dumps as parse2json
from .json_encoder import ObjectJsonEncoder


class JsonResponse(str):
    def __new__(self, hadErrors=False, content=None,
                errorCode=0, errorDesc=""):
        rDict = {}
        rDict["hadErrors"] = hadErrors
        rDict["content"] = content
        rDict["errorCode"] = errorCode
        rDict["errorDesc"] = errorDesc
        self.result = rDict
        self.json = parse2json(rDict, sort_keys=True, indent=4,
                               cls=ObjectJsonEncoder)
        return self.json


class ErrorResponse(JsonResponse):
    def __new__(self, errorCode=0, errorDesc=""):
        # super().__init__(self, hadErrors=True, content=None,
        #                  errorCode=errorCode, errorDesc=errorDesc)
        return JsonResponse(hadErrors=True, errorCode=errorCode,
                            errorDesc=errorDesc)


class GoodResponse(JsonResponse):
    def __new__(self, content=None):
        # super().__init__(self, hadErrors=False, content=content,
        #                 errorCode=0, errorDesc="")
        return JsonResponse(content=content)
