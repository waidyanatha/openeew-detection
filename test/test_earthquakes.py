from unittest import TestCase
from unittest.mock import patch

from test_utils import is_content_equals


class SaveEarthquakeTest(TestCase):
    @patch('time_utils.get_current_timestamp')
    @patch('db.execute_statement')
    def test_earthquake_is_persisted(self, mock_execute_statement, mock_get_current_timestamp):
        mock_get_current_timestamp.return_value = 1598032700
        from earthquakes import save_earthquake
        input = {
            'event_id': 'foo',
            'time_of_event': 1598031978,
            'intensity': 51,
            'latitude': -33.09947,
            'longitude': -33.19141,
            'sensor_ids': 79,
        }
        save_earthquake(input)
        mock_execute_statement.assert_called_once()
        expected_statement = '''
            INSERT INTO eew_output (
                event_id,
                time_of_event,
                intensity,
                latitude,
                longitude,
                sensor_ids,
                time_entered
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        expected_parameters = ('foo', 1598031978, 51, -33.09947, -33.19141, 79, 1598032700)
        actual_statement = mock_execute_statement.call_args[0][0]
        actual_parameters = mock_execute_statement.call_args[0][1]
        self.assertTrue(is_content_equals(expected_statement, actual_statement))
        self.assertEqual(expected_parameters, actual_parameters)
