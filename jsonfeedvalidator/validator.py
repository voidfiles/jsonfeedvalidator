import json

from jsonschema import validate

from jsonfeedvalidator.schema import SCHEMA


def validate_feed(feed):
    validate(feed, SCHEMA)


def validate_str(json_str):
    data = json.loads(json_str)
    validate_feed(data)
