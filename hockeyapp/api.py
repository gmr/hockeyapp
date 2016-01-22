"""
Extended by all API classes for communicating with the hockeyapp API

"""
import logging
import re
import requests

LOGGER = logging.getLogger(__name__)


class APIError(Exception):
    """Raised when the Hockeyapp API returns an error for a request"""

    def __repr__(self):
        """Return a representation of the exception

        :rtype: str

        """
        return '<%s [%s]>' % (self.__class__.__name__,
                              ', '.join(sorted(self.args[0].keys())))

    def __str__(self):
        """ Format exception data

        :returns: the string representation of the error

        """
        return ', '.join(sorted(['[%s]: %s' %
                          (key, self.args[0][key])
                          for key in self.args[0]]))


class APIRequest(object):
    """Base class for all API requests. Set Class.KEY to the part of the path
    specific to the request.

    """
    SERVER = 'rink.hockeyapp.net'
    BASE_URI = '/api/2'
    TOKEN_PATTERN = re.compile('[a-f0-9]{32}')
    KEY = 'override_me'

    def __init__(self, token):
        """Construct the APIRequestObject

        :param str token: The API token for the request

        """
        if not self.TOKEN_PATTERN.match(token):
            raise ValueError('The API token should be a 32 char hex digest')
        self.headers = {'Accept': 'application/json; text/plain;',
                        'X-HockeyAppToken': token}

    def _build_uri(self, path_parts):
        """Return the URI for the request

        :rtype: str

        """
        return 'https://%s%s/%s' % (self.SERVER, self.BASE_URI,
                                    '/'.join(path_parts))

    def _delete(self, uri_parts, data=None):
        """Delete data from the API

        :param list uri_parts: Parts of the URI to compose the URI
        :param dict data: Optional query parameters for the DELETE
        :rtype: list or dict

        """
        uri = self._build_uri(uri_parts) if uri_parts else self._uri
        LOGGER.debug('Performing HTTP DELETE to %s', uri)
        return self._response(requests.delete(uri,
                                              headers=self.headers,
                                              data=data))

    def _get(self, uri_parts, data=None):
        """Post data to the API

        :param list uri_parts: Parts of the URI to compose the URI
        :param dict data: Optional query parameters for the GET
        :rtype: list or dict

        """
        uri = self._build_uri(uri_parts) if uri_parts else self._uri
        LOGGER.debug('Performing HTTP GET to %s', uri)
        return self._response(requests.get(uri,
                                           headers=self.headers,
                                           data=data))

    def _post(self, uri_parts=None, data=None, files=None):
        """Get data from the API

        :param list uri_parts: Parts of the URI to compose the URI
        :param dict data: Optional query parameters for the POST
        :param dict files: A dictionary of field name and open file handles
        :rtype: list or dict

        """
        uri = self._build_uri(uri_parts) if uri_parts else self._uri
        LOGGER.debug('Performing HTTP POST to %s', uri)
        return self._response(requests.post(uri,
                                            headers=self.headers,
                                            data=data,
                                            files=files))

    def _response(self, response):
        """Process the API response

        :param requests.Response response: The request response
        :rtype: list
        :raise: hockeyapp.app.APIError

        """
        LOGGER.debug('Response status code: %s', response.status_code)
        LOGGER.debug('Headers: %r', response.headers)
        if 200 <= response.status_code <= 300:
            if 'application/json' in response.headers['Content-Type']:
                return response.json()
            return response.content
        if response.status_code == 404:
            raise APIError({'404': 'URL Not Found: %s' % response.url})
        if 'application/json' in response.headers['Content-Type']:
            raise APIError(response.json().get('errors'))
        LOGGER.debug(response.content)
        raise APIError('Not JSON')

    @property
    def _uri(self):
        """Return the URI for the request

        :rtype: str

        """
        return 'https://%s%s/%s' % (self.SERVER, self.BASE_URI, self.KEY)
