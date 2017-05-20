import requests
import pprint


data = requests.get("http://json.schemastore.org/feed")
schema = data.json()
schema = pprint.pformat(schema)
formatted_string = "SCHEMA = %s" % (schema)

print formatted_string
