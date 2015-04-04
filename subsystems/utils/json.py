import json
from django.http import HttpResponse


def render_to_json(data):
    return HttpResponse(json.dumps(data), content_type="application/json")