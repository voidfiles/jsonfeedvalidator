JSON Feed Validator
===================

This is a preview release of a JSON Feed validator


Example
-------

.. code-block:: python

    >>> import requests
    >>> import pprint
    >>> from jsonfeedvalidator import validate_feed
    >>> resp = requests.get("https://daringfireball.net/feeds/json")
    >>> validate_feed(resp.json())
    {}
    >>> feed = {"items": [{"attachments": [{}]}]}
    >>> pprint.pprint(validate_feed(feed))
    {'feed': {'errors': ['feed must have version', 'feed must have a title'],
              'suggestions': []},
     'items': {0: {'attachments': {0: {'attachment': {'errors': ['url required for attachment',
                                                                 'mime_type required for attachment'],
                                                      'suggestions': []}}},
                   'item': {'errors': ['item must have an id',
                                       'item must have one or both of content_html or content_text'],
                            'suggestions': []}}}}
