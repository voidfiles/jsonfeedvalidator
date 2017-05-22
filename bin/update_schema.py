import requests
import pprint


data = requests.get("http://json.schemastore.org/feed")
schema = data.json()


def coerce_key(data):
    if isinstance(data, dict):
        return {str(key): coerce_key(val) for key, val in data.items()}

    if isinstance(data, list):
        return [coerce_key(x) for x in data]

    if isinstance(data, basestring):
        return str(data.encode('utf-8'))

    return data

schema = coerce_key(schema)
schema = pprint.pformat(schema)
formatted_string = "SCHEMA = %s" % (schema)

print formatted_string
