# -*- coding: utf-8 -*-

import sys

import requests

import constants

class NbaRequest:

    def __init__(self, endpoint=None, params=None):
        self._headers = {'user-agent': 'nba-mongo'}
        self._params = params
        self._url = (constants.NBA_BASE_URL + endpoint) if endpoint else constants.NBA_BASE_URL

    def send(self):
        response = None
        try:
            request = requests.get(self._url, headers=self._headers, params=self._params)
            response = request.json()
        except requests.exceptions.RequestException as err:
            print("Request error: {0}".format(err))
        except ValueError as err:
            print("JSON decoding error: {0}".format(err))
        except:
            print("Unexpected error: ", sys.exc_info()[0])

        if request.status_code != 200:
            request.raise_for_status()

        return response
