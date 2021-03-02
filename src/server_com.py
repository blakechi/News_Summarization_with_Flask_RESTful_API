import json


class ServerCom():
    """
    A simple container for server related infomation.
    """
    def __init__(self, url=None, query=None):
        with open('./server.json') as f:
            """
            news_summarization/server.json:
            
            {
                "url": "your/server/url/for/query"
            }
            """

            data = json.load(f)
        self._url = url if url is not None else data['url']
        self._query = query

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, q):
        self._url = q

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, q):
        self._query = q
