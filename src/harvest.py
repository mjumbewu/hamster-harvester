import requests
import json

class API (object):
    DEFAULT_HEADERS = {
        'Accept': 'application/json',
        'Content-typt': 'application/json',
    }
    DEFAULT_AUTH = ('mpoe@openplans.org', 'I10veJ\'nia')
    DEFAULT_HOST = 'openplans.harvestapp.com'

    def __init__(self, hostname=DEFAULT_HOST, session=None):
        self.session = session or requests.session(headers=self.DEFAULT_HEADERS, auth=self.DEFAULT_AUTH)
        self.hostname = hostname

    def get(self, path):
        url = 'https://' + self.hostname + '/daily'
        response = self.session.get(url)
        data = json.loads(response.text)
        return data

    __projects = None
    def projects(self):
        if self.__projects is None:
            data = self.get('/daily')
            self.__projects = data['projects']
        return self.__projects
