from rest_framework.renderers import JSONRenderer as OldJSONRenderer
from rest_framework.utils import encoders
from bson import ObjectId


class MyJSONEncoder(encoders.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


class JSONRenderer(OldJSONRenderer):
    encoder_class = MyJSONEncoder
