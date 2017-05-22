import pprint

from jsonfeedvalidator.validator import validate_feed, format_errors, ErrorTree

GOOD_DATA = {
    "version": "https://jsonfeed.org/version/1",
    "title": "My Example Feed",
    "home_page_url": "https://example.org/",
    "feed_url": "https://example.org/feed.json",
    "items": [
        {
            "id": "2",
            "content_text": "This is a second item.",
            "url": "https://example.org/second-item"
        },
        {
            "id": "1",
            "content_html": "<p>Hello, world!</p>",
            "url": "https://example.org/initial-post",
            "attachments": [{
                "url": "http://example.org",
                "mime_type": "text/html",
                "title": "This is an amazing website",
                "size_in_bytes": 1000,
                "duration_in_seconds": 10,
            }]
        }
    ]
}


BAD_DATA = {
    "home_page_url": "https://example.org/",
    "feed_url": "https://example.org/feed.json",
    "items": [
        {
            "blah": "awesome",
            "attachments": [{
                "url": "http://example.org",
            }]
        }
    ]
}


def test_validate_good_feed():
    assert validate_feed(GOOD_DATA) == []


def test_validate_bad_feed():
    errors = validate_feed(BAD_DATA)
    assert len(errors) > 0

def test_validate_format_feed_errors():
    errors = validate_feed(BAD_DATA)
    assert len(errors) > 0

    blah = format_errors(BAD_DATA, ErrorTree(errors))
    assert blah == {
        'items': {
            0: {
                'errors': {
                    'additionalProperties': [
                        "'blah' does not match any of the regexes: '^_[a-zA-Z]([^.]+)$'"
                    ],
                    'required': [
                        "'id' is a required property"
                    ]
                },
                'attachments': {
                    0: {
                        'errors': {
                            'required': [
                                "'mime_type' is a required property"
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
