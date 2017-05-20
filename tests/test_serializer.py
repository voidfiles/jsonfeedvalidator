import pytest

from jsonfeedvalidator.validator import validate_feed
from jsonschema import ValidationError

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
    assert validate_feed(GOOD_DATA) is None


def test_validate_bad_feed():
    with pytest.raises(ValidationError):
        validate_feed(BAD_DATA)
