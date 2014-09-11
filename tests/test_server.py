from unittest import TestCase
import json
from threading import Thread
import time
from urllib2 import urlopen

PORT = 5002

def _retreive_school_names(starting_letters = 'a'):
    url = 'http://localhost:{}/matches/{}'.format(PORT, starting_letters)        
    raw_data = urlopen(url).read().decode('utf-8').strip()
    raw_data = raw_data[raw_data.find('(')+1:]
    raw_data = raw_data[:-2]
    return json.loads(raw_data)

def go_retrive(expected_result):
    for i in range(10):
        r = _retreive_school_names()
        assert(r == expected_result)

class TestServer(TestCase):
    ''' testing server '''
    def test_retrieval_from_multiple_threads(self):
        expected_result = _retreive_school_names()
        running_threads = []
        for i in range(10):
            try:
                t = Thread(target=go_retrive, args=(expected_result,))
                t.start()
                running_threads.append(t)
            except:
               print "Error: unable to start thread"
        map( t.join(), running_threads)




