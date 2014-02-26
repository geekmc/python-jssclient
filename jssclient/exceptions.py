#!/usr/bin/python
import json

class ClientException(Exception):
    """
    The base exception class for all exceptions this library raises.
    """
    def __init__(self, code, message=None, detail=None):
        self.code = code
        self.message = message or self.__class__.message
        self.detail = detail

    def __str__(self):
        if self.message:
            if self.detail:
                return  "%s %s (HTTP %s)" % (self.message,
                                             self.detail,
                                             self.code)
            return "%s (HTTP %s)" % (self.message, self.code)
        return "HTTP %s" % self.code

class CommandError(Exception):
    pass

class BadRequest(ClientException):
    """
    HTTP 400 - Bad request: you sent some malformed data.
    """
    http_status = 400
    message = "Bad request"


class Unauthorized(ClientException):
    """
    HTTP 401 - Unauthorized: bad credentials.
    """
    http_status = 401
    message = "Unauthorized"


class Forbidden(ClientException):
    """
    HTTP 403 - Forbidden: your credentials don't give you access to this
    resource.
    """
    http_status = 403
    message = "Forbidden"


class NotFound(ClientException):
    """
    HTTP 404 - Not found
    """
    http_status = 404
    message = "Not found"


class OverLimit(ClientException):
    """
    HTTP 413 - Over limit: you're over the API limits for this time period.
    """
    http_status = 413
    message = "Over limit"


# NotImplemented is a python keyword.
class HTTPNotImplemented(ClientException):
    """
    HTTP 501 - Not Implemented: the server does not support this operation.
    """
    http_status = 501
    message = "Not Implemented"


# In Python 2.4 Exception is old-style and thus doesn't have a __subclasses__()
# so we can do this:
#     _code_map = dict((c.http_status, c)
#                      for c in ClientException.__subclasses__())
#
# Instead, we have to hardcode it:
_code_map = dict((c.http_status, c) for c in [BadRequest, Unauthorized,
                   Forbidden, NotFound, OverLimit, HTTPNotImplemented])


def from_response(status, body):
    """
    Return an instance of an ClientException or subclass
    based on an httplib2 response.

    Usage::

        resp, body = http.request(...)
        if resp.status != 200:
            raise exception_from_response(resp, body)
    """
    cls = _code_map.get(status, ClientException)
    message = "n/a"
    detail = "n/a"
    print '###', status, body, type(body)
    try:
        body = json.loads(body)
    except:
        pass
    if body and isinstance(body, dict):
        message = body.get('code', None)
        detail = "%s (request-id: %s)" % (body.get('message', ''),
                              body.get('requestId', ''))
    return cls(code=status, message=message, detail=detail)
