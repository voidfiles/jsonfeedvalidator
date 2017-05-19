import requests
from jsonfeedvalidator import validate_feed

resp = requests.get("https://daringfireball.net/feeds/json")

errors = validate_feed(resp.json())

print errors  # {}
