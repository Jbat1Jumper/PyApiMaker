import json


class ObjectJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "toJson"):
            return obj.toJson()
        return json.JSONEncoder.default(obj)
