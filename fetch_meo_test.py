import unittest
from unittest.mock import Mock
from unittest.mock import patch
import fetch_meo
import responses
import constants
import json
import logging
logging.basicConfig(level = logging.DEBUG)

class testMEOFetch(unittest.TestCase):
    
    

    @responses.activate
    def test_s3_bucket_update(self):
        mock_url = "http://www.meo.pt"
        con = Mock()
        s3 = Mock()
        string_io = Mock()

        responses.add(responses.POST, mock_url,json=json.loads(constants.example_json), status=200)
        string_io.getvalue.return_value = "test_value"

        fetch_meo.fetch_and_parse_MEO(mock_url, con, s3, string_io)
        
        s3.Bucket.assert_called_with('www.cinefilopobre.com')
        s3.Bucket('www.cinefilopobre.com').put_object.assert_called_with(Key='out.csv', Body="test_value")

    @responses.activate
    def test_insert_postgres_called_for_each_program_and_channel(self):
        mock_url = "http://www.meo.pt"
        con = Mock()
        s3 = Mock()
        string_io = Mock()

        responses.add(responses.POST, mock_url,json=json.loads(constants.example_json), status=200)

        fetch_meo.fetch_and_parse_MEO(mock_url, con, s3, string_io)
        assert con.cursor().execute.call_count == len(constants.channels) + 1 # +1 for the truncate

    def test_db_truncate(self):
        con = Mock()
        fetch_meo.truncate_db(con)
        con.cursor().execute.assert_called_with("TRUNCATE TABLE tv")

    def test_write_to_postgres(self):
        con = Mock()
        channelName = "testChannel"
        progDate = "testDate"
        progName = "testProgram"
        fetch_meo.write_to_postgres(con, channelName, progDate, progName)
        con.cursor().execute.assert_called_with('INSERT INTO tv (title, channel, time) values (\'testProgram\', \'testChannel\', \'testDate\')')

if __name__ == '__main__':
    unittest.main()
