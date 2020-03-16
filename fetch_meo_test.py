import unittest
from unittest.mock import Mock
import fetch_meo
import responses
import constants
import json

class testMEOFetch(unittest.TestCase):
    
    

    @responses.activate
    def test_abc(self):
        mock_url = "http://www.meo.pt"
        con = Mock()
        s3 = Mock()
        responses.add(responses.POST, mock_url,json=json.loads(constants.example_json), status=200)
        fetch_meo.fetch_and_parse_MEO(mock_url, con, s3)




if __name__ == '__main__':
    unittest.main()
