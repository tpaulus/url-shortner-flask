from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

_create_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "type": "object",
    "required": [
        "long_url",
    ],
    "properties": {
        "long_url": {
            "type": "string",
            "maxLength": 1024,
            "minLength": 1,
            "pattern": r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        },
        "expires": {
            "minProperties": 1,
            "properties": {
                "days": {
                    "type": "integer",
                    "minimum": 1,
                },
                "seconds": {
                    "type": "integer",
                    "minimum": 1,
                },
                "microseconds": {
                    "type": "integer",
                    "minimum": 1,
                },
                "milliseconds": {
                    "type": "integer",
                    "minimum": 1,
                },
                "minutes": {
                    "type": "integer",
                    "minimum": 1,
                },
                "hours": {
                    "type": "integer",
                    "minimum": 1,
                },
                "weeks": {
                    "type": "integer",
                    "minimum": 1,
                }
            },
            "additionalProperties": False
        }
    },
    "additionalProperties": False
}


class CreateShortUrlRequest(Inputs):
    json = [JsonSchema(schema=_create_schema)]


def validate_create(request):
    request = CreateShortUrlRequest(request)
    if request.validate():
        return None
    else:
        return request.errors
