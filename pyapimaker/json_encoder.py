import json


class ObjectJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return obj.to_json()
        return json.JSONEncoder.default(obj)
