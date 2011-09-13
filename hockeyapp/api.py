"""
Base API Class and Request Functionality

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2011-09-12'

import json
import logging
import httplib
import urllib
import urlparse

SERVER = 'rink.hockeyapp.net'
BASE_URI = '/api/2/'


def _request(api_key, uri, parameters):
    """Make a request to the Hockeyapp API server

    :param api_key: The API Key for the request
    :type api_key: str
    :param uri: The URI to make a request for
    :type uri: str
    :param parameters: URL parameters
    :type parameters: dict
    :returns: tuple of headers dict and json decoded response data

    """
    logger = logging.getLogger('hockeyapp.api')
    headers = {'X-HockeyAppToken': api_key, 'Accept': '*/*'}
    if parameters:
        logger.debug('Encoding parameters: %r', parameters)
        params = urllib.urlencode(parameters)
    else:
        params = None
    logger.debug('Requesting: %s?%s with headers: %r', uri, params, headers)
    connection = httplib.HTTPSConnection(SERVER)
    connection.request("GET", uri, params, headers)

    # Get the response
    response = connection.getresponse()
    logger.debug('Return Response: %i %s %r',
                 response.status, response.reason, response.getheaders())

    if response.status == 302:
        connection.close()
        location = response.getheader('location')
        logger.debug('Making new request to %s', location)
        parts = urlparse.urlparse(location)
        if parts.scheme == 'http':
            connection = httplib.HTTPConnection(parts.netloc)
        elif parts.scheme == 'https':
            connection = httplib.HTTPSConnection(parts.netloc)
        else:
            raise NotImplementedError('Unspported protocol scheme: %s',
                                      parts.scheme)

        logger.debug('%s', parts)

        headers = {'Accept': '*/*'}
        if parts.hostname.find('hockeyapp.net') > -1:
            headers['X-HockeyAppToken'] = api_key

        connection.request('GET', parts.path, parts.params, headers)
        response = connection.getresponse()
        logger.debug('Return Response: %i %s %r',
                     response.status, response.reason, response.getheaders())



    # If we don't have a 200, return the status and None
    if response.status != 200:
        connection.close()
        return response.status, None

    # Read in the data from the response
    data = response.read()
    connection.close()

    # If we have data, json decode it
    if data and response.getheader('content-type') == 'application/json':
        data = json.loads(data)

    return response.status, data


class APIRequest(object):
    """Base Hockeyapp APIRequest Object"""
    def __init__(self, api_key):
        """Construct the APIRequestObject

        :param api_key: The API Key for the request
        :type api_key: str

        """
        self._logger = logging.getLogger(__name__)
        self._api_key = api_key
        self._key = None
        self._logger.debug('Initialized an %s instance with the api key: %s',
                           self.__class__.__name__, self._api_key)

    def execute(self):
        """Execute the API request. If parameters are provided, join them as
        a URI.

        :returns: an iterable or None

        """
        status, data = _request(self._api_key, self.path, self.parameters)
        if status == 200:
            if isinstance(data, dict) and self._key:
                return data[self._key]
            return data

        return None

    @property
    def parameters(self):
        """Returns the request parameters

        :returns: dict or None

        """
        return None

    @property
    def path(self):
        """Returns the request path

        :returns: str

        """
        return BASE_URI
