import requests
import json

class API (object):
    DEFAULT_HEADERS = {
        'Accept': 'application/json',
        'Content-typt': 'application/json',
    }
    DEFAULT_AUTH = ('email@organization.org', 'password')
    DEFAULT_HOST = 'organization.harvestapp.com'

    def __init__(self, session_info=None):
        session_info = session_info or self.make_session_info()
        self.hostname, self.session = session_info

    @classmethod
    def make_session_info(cls, hostname='', auth=(), headers={}):
        session = requests.Session()
        session.auth = auth or cls.DEFAULT_AUTH
        session.headers.update(headers or cls.DEFAULT_HEADERS)
        
        return (
            hostname or cls.DEFAULT_HOST,
            session,
        )

    def get(self, path):
        url = 'https://' + self.hostname + path
        response = self.session.get(url)
#        import pdb; pdb.set_trace()
        data = json.loads(response.text)
        return data

    __projects = None
    def projects(self):
        if self.__projects is None:
            data = self.get('/daily')
            self.__projects = data['projects']
        return self.__projects

    def entries(self, for_date=None):
        datepath = for_date.strftime('/%j/%Y') if for_date else ''
        data = self.get('/daily' + datepath)
        return data['day_entries']

    def add_entry(self, started_at=None, ended_at=None, notes=None, 
                  project_id=None, task_id=None, spent_at=None):
        url = 'https://' + self.hostname + '/daily/add'
        entry_data = {
            'project_id': project_id,
            'task_id': task_id}
        if started_at and ended_at:
            entry_data['started_at'] = started_at.strftime('%I:%M%p').lower()
            entry_data['ended_at'] = ended_at.strftime('%I:%M%p').lower()
            entry_data['hours'] = (ended_at - started_at).total_seconds()/3600
        if spent_at:
            entry_data['spent_at'] = spent_at.strftime('%a, %d %b %Y')
        if notes:
            entry_data['notes'] = notes
        response = self.session.post(url, data=json.dumps(entry_data))
        data = json.loads(response.text)
        return data
