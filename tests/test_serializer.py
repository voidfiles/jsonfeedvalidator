from jsonfeedvalidator.validator import validate_feed

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

BAD_OUTPUT = {
    'feed': {
        'errors': [
            'feed must have version',
            'feed must have a title'
        ],
        'suggestions': []
    },
    'items': {
        0: {
            'item': {
                'errors': [
                    'item must have an id',
                    'item must have one or both of content_html or content_text'
                ],
                'suggestions': []
            },
            'attachments': {
                0: {
                    'attachment': {
                        'errors': ['mime_type required for attachment'],
                        'suggestions': []
                    }
                }
            }
        }
    }
}


ERRORS = {
    'items': [
        {0: 'Item must have one or both of content_text or content_html'}
    ],
    'version': ['This field is required'],
    'title': ['This field is required'],
}


def test_validate_good_feed():
    assert validate_feed(GOOD_DATA) == {}


def test_validate_bad_feed():
    assert validate_feed(BAD_DATA) == BAD_OUTPUT
