

class JSONFeedValidationException(Exception):
    pass


class InvalidJSONException(JSONFeedValidationException):
    pass


class ValidationException(JSONFeedValidationException):
    pass


class SuggestionException(JSONFeedValidationException):
    pass
