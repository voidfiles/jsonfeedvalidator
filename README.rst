JSON Feed Validator
===================

This is a preview release of a JSON Feed validator


Example
-------

.. code-block:: python

    >>> import requests
    >>> from jsonfeedvalidator import validate_feed, format_errors, ErrorTree
    >>> resp = requests.get("https://daringfireball.net/feeds/json")
    >>> validate_feed(resp.json())
    []
    >>> feed = {"items": [{"attachments": [{}]}]}
    >>> errors = validate_feed(feed)
    >>> format_errors(feed, ErrorTree(errors))
    {
        'items': {
            0: {
                'errors': {
                    'required': [
                        "'id' is a required property"
                    ]
                },
                'attachments': {
                    0: {
                        'errors': {
                            'required': [
                                "'mime_type' is a required property",
                                "'url' is a required property"
                            ]
                        }
                    }
                }
            }
        },
        'errors': {
            'required': [
                "'title' is a required property",
                "'version' is a required property"
            ]
        }
    }
