JSON Feed Validator
===================

This is a preview release of a JSON Feed validator


Example
-------

.. code-block:: python

    >>> import requests
    >>> from jsonschema import ValidationError
    >>> from jsonfeedvalidator import validate_feed
    >>> resp = requests.get("https://daringfireball.net/feeds/json")
    >>> validate_feed(resp.json())
    None
    >>> feed = {"items": [{"attachments": [{}]}]}
    >>> errors = None
    >>> try:
    ...     validate_feed(feed)
    ... except ValidationError as e:
    ...     handle_errors(e)
