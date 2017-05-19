import json
import iso8601

from .exceptions import InvalidJSONException, ValidationException, SuggestionException


def expect(expected, message, func, *args, **kwargs):
    raised = None

    try:
        func(*args, **kwargs)
    except expected as e:
        raised = e

    if not raised:
        return False

    if raised.message != message:
        print "Got message: %s expected: %s" % (raised.message, message)
        return False

    return True


HUB_TYPE_REQUIRED = "type required for hub"


def validate_hub_type(hub):
    """
    >>> hub = {"type": "WebSub"}
    >>> assert validate_hub_type(hub) is True
    >>> hub = {}
    >>> assert expect(ValidationException, HUB_TYPE_REQUIRED, validate_hub_type, hub) is True
    """

    _type = hub.get('type')
    if not _type:
        raise ValidationException(HUB_TYPE_REQUIRED)

    return True


HUB_URL_REQUIRED = "url required for hub"


def validate_hub_url(hub):
    """
    >>> hub = {"url": "http://example.org"}
    >>> assert validate_hub_url(hub) is True
    >>> hub = {}
    >>> assert expect(ValidationException, HUB_URL_REQUIRED, validate_hub_url, hub) is True
    """

    url = hub.get('url')
    if not url:
        raise ValidationException(HUB_URL_REQUIRED)

    return True


ATTACHMENT_URL_REQUIRED = "url required for attachment"


def validate_attachment_url(attachment):
    """
    >>> attachment = {"url": "http://example.org"}
    >>> assert validate_attachment_url(attachment) is True
    >>> assert expect(ValidationException, ATTACHMENT_URL_REQUIRED, validate_attachment_url, {}) is True
    """

    url = attachment.get('url')
    if not url:
        raise ValidationException(ATTACHMENT_URL_REQUIRED)

    return True

ATTACHMENT_MIME_TYPE_REQUIRED = "mime_type required for attachment"


def validate_attachment_mime_type(attachment):
    """
    >>> attachment = {"mime_type": "application/json"}
    >>> assert validate_attachment_mime_type(attachment) is True
    >>> assert expect(ValidationException, ATTACHMENT_MIME_TYPE_REQUIRED, validate_attachment_mime_type, {}) is True
    """

    mime_type = attachment.get('mime_type')
    if not mime_type:
        raise ValidationException(ATTACHMENT_MIME_TYPE_REQUIRED)

    return True


ATTACHMENT_DURATION_IN_SECONDS_MUST_BE_INTEGER = "duration_in_seconds must be an integer"


def validate_attachment_duration_in_seconds(attachment):
    """
    >>> attachment = {}
    >>> assert validate_attachment_duration_in_seconds(attachment) is True
    >>> attachment = {"duration_in_seconds": 10}
    >>> assert validate_attachment_duration_in_seconds(attachment) is True
    >>> attachment = {"duration_in_seconds": 'a'}
    >>> assert expect(ValidationException, ATTACHMENT_DURATION_IN_SECONDS_MUST_BE_INTEGER,
    ... validate_attachment_duration_in_seconds, attachment) is True
    """

    duration_in_seconds = attachment.get('duration_in_seconds')
    if not duration_in_seconds:
        return True

    if isinstance(duration_in_seconds, int):
        return True

    raise ValidationException(ATTACHMENT_DURATION_IN_SECONDS_MUST_BE_INTEGER)


ATTACHMENT_SIZE_IN_BYTES_MUST_BE_INTEGER = "size_in_bytes must be an integer"


def validate_attachment_size_in_bytes(attachment):
    """
    >>> attachment = {}
    >>> assert validate_attachment_size_in_bytes(attachment) is True
    >>> attachment = {"size_in_bytes": 10}
    >>> assert validate_attachment_size_in_bytes(attachment) is True
    >>> attachment = {"size_in_bytes": 'a'}
    >>> assert expect(ValidationException, ATTACHMENT_SIZE_IN_BYTES_MUST_BE_INTEGER,
    ... validate_attachment_size_in_bytes, attachment) is True
    """

    size_in_bytes = attachment.get('size_in_bytes')
    if not size_in_bytes:
        return True

    if isinstance(size_in_bytes, int):
        return True

    raise ValidationException(ATTACHMENT_SIZE_IN_BYTES_MUST_BE_INTEGER)

ITEM_ID_REQUIRED = "item must have an id"


def validate_item_id(item):
    """
    >>> item = {"id": "1234"}
    >>> assert validate_item_id(item) is True
    >>> assert expect(ValidationException, ITEM_ID_REQUIRED, validate_item_id, {}) is True
    """

    _id = item.get('id')
    if not _id:
        raise ValidationException(ITEM_ID_REQUIRED)

    return True


ITEM_DATE_PUBSLISHED_FORMAT = "date_published must be formatted as ISO8601 date"


def validate_item_date_published(item):
    """
    >>> item = {}
    >>> assert validate_item_date_published(item) is True
    >>> item = {"date_published": "Tuesday"}
    >>> assert expect(ValidationException, ITEM_DATE_PUBSLISHED_FORMAT, validate_item_date_published, item) is True
    """

    date_published = item.get('date_published')
    if not date_published:
        return True

    try:
        iso8601.parse_date(date_published)
    except iso8601.ParseError as e:
        raise ValidationException(ITEM_DATE_PUBSLISHED_FORMAT)

    return True


ITEM_DATE_MODIFIED_FORMAT = "date_modified must be formatted as ISO8601 date"


def validate_item_date_modified(item):
    """
    >>> item = {}
    >>> assert validate_item_date_modified(item) is True
    >>> item = {"date_modified": "Tuesday"}
    >>> assert expect(ValidationException, ITEM_DATE_MODIFIED_FORMAT, validate_item_date_modified, item) is True
    """

    date_modified = item.get('date_modified')
    if not date_modified:
        return True

    try:
        iso8601.parse_date(date_modified)
    except iso8601.ParseError as e:
        raise ValidationException(ITEM_DATE_MODIFIED_FORMAT)

    return True

ITEM_MUST_HAVE_ONE_CONTENT = "item must have one or both of content_html or content_text"


def validate_item_content(item):
    """
    >>> item = {"content_html": "html"}
    >>> assert validate_item_content(item) is True
    >>> item = {"content_text": "text"}
    >>> assert validate_item_content(item) is True
    >>> item = {"content_text": "text", "content_html": "html"}
    >>> assert validate_item_content(item) is True
    >>> item = {}
    >>> assert expect(ValidationException, ITEM_MUST_HAVE_ONE_CONTENT, validate_item_content, item) is True
    """

    has_content_html = item.get('content_html')
    has_content_text = item.get('content_text')
    if any([has_content_html, has_content_text]):
        return True

    raise ValidationException(ITEM_MUST_HAVE_ONE_CONTENT)


VERSION_MUST_BE_INCLUDED = "feed must have version"
VERSION_MUST_BE_CORRECT = "version must be https://jsonfeed.org/version/1"


def validate_version(feed):
    """
    >>> feed = {"version": "https://jsonfeed.org/version/1"}
    >>> assert validate_version(feed) is True
    >>> feed = {}
    >>> assert expect(ValidationException, VERSION_MUST_BE_INCLUDED, validate_version, {}) is True
    >>> feed = {"version": "blah"}
    >>> assert expect(ValidationException, VERSION_MUST_BE_CORRECT, validate_version, feed) is True
    """
    version = feed.get('version')
    if not version:
        raise ValidationException(VERSION_MUST_BE_INCLUDED)

    if version != "https://jsonfeed.org/version/1":
        raise ValidationException(VERSION_MUST_BE_CORRECT)

    return True


TITLE_REQUIRED = "feed must have a title"


def validate_title(feed):
    """
    >>> feed = {"title": "This is a great title"}
    >>> assert validate_title(feed) is True
    >>> feed = {}
    >>> assert expect(ValidationException, TITLE_REQUIRED, validate_title, {}) is True
    >>> feed = {"title": ""}
    >>> assert expect(ValidationException, TITLE_REQUIRED, validate_title, feed) is True
    """
    title = feed.get('title')
    if not title:
        raise ValidationException(TITLE_REQUIRED)

    return True

feed_validators = [
    validate_version,
    validate_title
]

attachment_validators = [
    validate_attachment_url,
    validate_attachment_mime_type,
]

item_validators = [
    validate_item_id,
    validate_item_date_published,
    validate_item_date_modified,
    validate_item_content,
]

item_hub = [

]

def validate_hub(hub):
    error_tree = {}
    attachment_errors = []
    attachment_suggestions = []

    for validator in attachment_validators:
        try:
            validator(attachment)
        except ValidationException as e:
            attachment_errors += [e.message]
        except SuggestionException as e:
            attachment_suggestions += [e.message]

    if attachment_errors or attachment_suggestions:
        error_tree['attachment'] = {
            'errors': attachment_errors,
            'suggestions': attachment_suggestions
        }

    return error_tree

def validate_attachment(attachment):
    error_tree = {}
    attachment_errors = []
    attachment_suggestions = []

    for validator in attachment_validators:
        try:
            validator(attachment)
        except ValidationException as e:
            attachment_errors += [e.message]
        except SuggestionException as e:
            attachment_suggestions += [e.message]

    if attachment_errors or attachment_suggestions:
        error_tree['attachment'] = {
            'errors': attachment_errors,
            'suggestions': attachment_suggestions
        }

    return error_tree


def validate_item(item):
    error_tree = {}
    item_errors = []
    item_suggestions = []

    for validator in item_validators:
        try:
            validator(item)
        except ValidationException as e:
            item_errors += [e.message]
        except SuggestionException as e:
            item_suggestions += [e.message]

    if item_errors or item_suggestions:
        error_tree['item'] = {
            'errors': item_errors,
            'suggestions': item_suggestions
        }

    if 'attachments' not in item:
        return error_tree

    for i, attachment in enumerate(item['attachments']):
        errors = validate_attachment(attachment)
        if not errors:
            continue

        if 'attachments' not in error_tree:
            error_tree['attachments'] = {}

        error_tree['attachments'][i] = errors

    return error_tree


def validate_feed(feed):
    error_tree = {}
    feed_errors = []
    feed_suggestions = []

    for validator in feed_validators:
        try:
            validator(feed)
        except ValidationException as e:
            feed_errors += [e.message]
        except SuggestionException as e:
            feed_suggestions += [e.message]

    if feed_errors or feed_suggestions:
        error_tree['feed'] = {
            "errors": feed_errors,
            "suggestions": feed_suggestions
        }

    for i, item in enumerate(feed.get('items', [])):
        errors = validate_item(item)
        if not errors:
            continue

        if 'items' not in error_tree:
            error_tree['items'] = {}

        error_tree['items'][i] = errors

    for i, hub in enumerate(feed.get('hubs', [])):
        errors = validate_hub(item)
        if not errors:
            continue

        if 'items' not in error_tree:
            error_tree['items'] = {}

        error_tree['items'][i] = errors

    return error_tree


def validate_str(json_str):
    try:
        data = json.loads(json_str)
    except ValueError:
        raise InvalidJSONException("Passed JSON is invalid")

    return validate_feed(data)
