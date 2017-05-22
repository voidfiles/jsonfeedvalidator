import json
import re

from collections import defaultdict

from jsonschema import Draft4Validator
from jsonschema.exceptions import relevance

from jsonfeedvalidator.schema import SCHEMA

json_schema_validator = Draft4Validator(SCHEMA)


class Unset(object):
    """
    An as-of-yet unset attribute or unprovided default parameter.
    """

    def __repr__(self):
        return "<unset>"

_unset = Unset()


class ErrorTree(object):
    """
    ErrorTrees make it easier to check which validations failed.
    """

    _instance = _unset

    def __init__(self, errors=()):
        self.errors = defaultdict(list)
        self._contents = defaultdict(self.__class__)

        for error in errors:
            container = self
            for element in error.path:
                container = container[element]
            container.errors[error.validator] += [error]

            container._instance = error.instance

    def __contains__(self, index):
        """
        Check whether ``instance[index]`` has any errors.
        """

        return index in self._contents

    def __getitem__(self, index):
        """
        Retrieve the child tree one level down at the given ``index``.
        If the index is not in the instance that this tree corresponds to and
        is not known by this tree, whatever error would be raised by
        ``instance.__getitem__`` will be propagated (usually this is some
        subclass of :class:`LookupError`.
        """

        if self._instance is not _unset and index not in self:
            self._instance[index]

        return self._contents[index]

    def __setitem__(self, index, value):
        self._contents[index] = value

    def __iter__(self):
        """
        Iterate (non-recursively) over the indices in the instance with errors.
        """

        return iter(self._contents)

    def __repr__(self):
        return "<%s (%s total errors)>" % (self.__class__.__name__, len(self))


def validate_feed(feed):
    errors = json_schema_validator.iter_errors(feed)
    errors = sorted(errors, key=relevance, reverse=True)
    errors = (error for error in errors if not error.context)

    return list(errors)


def validate_str(json_str):
    data = json.loads(json_str)
    validate_feed(data)


def path_to_shape(path, value):

    container = {
        path.pop(): value
    }

    for part in reversed(path):
        _container = {
            part: container
        }
        container = _container

    return container

REQUIRED_PARSER = re.compile(r"u'(.*)' is a required property")


def format_message(error):
    if error.validator == 'required':
        key = REQUIRED_PARSER.match(error.message).items[0]
        return "A feed must %s is a required property" % (key)


def format_errors(instance, error_tree):
    context = {}

    if isinstance(instance, dict):
        for key, val in instance.items():
            if key in error_tree:
                context[key] = format_errors(val, error_tree[key])
    else:
        for i, val in enumerate(instance):
            if i in error_tree:
                context[i] = format_errors(val, error_tree[i])

    if error_tree.errors:
        context["errors"] = {
            key: [e.message for e in val] for key, val in error_tree.errors.items()
        }

    return context
