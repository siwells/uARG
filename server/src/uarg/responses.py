
# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

def build_response(msg, status='ok', code=200, data=[], errors=[], _links={}):
    """
    Build a response dict to return from the API
    """
    response = {}
    response['status'] = status
    response['code'] = code
    response['message'] = msg
    response['data'] = data
    response['_links'] = _links
    response['errors'] = errors
    return response


def get_error(message, logref=None, _links=None):
    """
    Return a dict representing a single error to report in the response doc
    """
    error = {}
    error['message'] = message
    error['logref'] = logref
    error['_links'] = _links

    return error


def assemble_links(links=[]):
    """
    Construct a HAL compliant _links dict for inclusion in a response doc

    Return a HAL compliant _links dict for inclusion in a response doc
    """
    _links = {}
    for link in links:
        for key in link:
            _links[key] = link[key]

    return _links


def get_link(name, url):
    """
    Construct a HAL compliant link for inclusion in _links dict
    """
    href = {}
    href['href'] = url

    link = {}
    link[name] = href
    return link
