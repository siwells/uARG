import os
import uarg 
import unittest

class API_Root(unittest.TestCase):

    def test_root(self):
        self.app = uarg.app.test_client()
        out = self.app.get('/')
        assert '200 OK' in out.status
        assert 'charset=utf-8' in out.content_type
        assert 'text/html' in out.content_type


class API_Dialogues(unittest.TestCase):

    def test_dialogues(self):
        self.app = uarg.app.test_client()
        out = self.app.get('/api/dialogues')
        assert '200 OK' in out.status
        assert 'application/json' in out.content_type




if __name__ == "__main__":
    
    unittest.main()
