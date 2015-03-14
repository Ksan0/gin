import json
from django.http import HttpResponse


def render_to_json(data):
    return HttpResponse(json.dumps(data), content_type="application/json")


class AjaxStatus(object):
    def __init__(self, status):
        self.status = status

    def json(self):
        return {
            "status": self.status
        }


class AjaxPostErrors(object):
    NONE = AjaxStatus("OK")
    BAD_METHOD = AjaxStatus("BAD_METHOD")
    BAD_FORM = AjaxStatus("BAD_FORM")
    BAD_SESSION = AjaxStatus("BAD_SESSION")
    BAD_LOGIN_OR_PASSWORD = AjaxStatus("BAD_LOGIN_OR_PASSWORD")
    INTERNAL_ERROR = AjaxStatus("INTERNAL_ERROR")