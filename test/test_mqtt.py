from unittest import TestCase
from openeew.mqtt import parser_json


class ParserJsonTest(TestCase):
    def test_esp32_payload(self):
        payload = '''
            {
                "device_id": "foo",
                "cloud_t": 123,
                "traces": [
                    {
                        "x": [1, 2, 3],
                        "y": [1, 2, 3],
                        "z": [1, 2, 3],
                        "t": 4,
                        "sr": 5
                    }
                ]
            }
        '''
        expected = (
            'foo',
            123,
            {
                't': [
                    3.4,
                    3.6,
                    3.8000000000000003,
                    4.0,
                    4.200000000000001,
                    4.4,
                    4.600000000000001,
                ],
                'x': [1, 2, 3],
                'y': [1, 2, 3],
                'z': [1, 2, 3],
            },
            5,
        )
        actual = parser_json(payload)
        self.assertEqual(expected, actual)

    def test_rp_payload(self):
        payload = '''
            {
                "device_id": "foo",
                "cloud_t": 0,
                "x": [1],
                "y": [2],
                "z": [3],
                "t": [4],
                "device_t": 4,
                "sr": 1
            }
        '''
        expected = (
            'foo',
            0,
            {
                't': [3.0, 4.0, 5.0],
                'x': [1],
                'y': [2],
                'z': [3],
            },
            1,
        )
        actual = parser_json(payload)
        self.assertEqual(expected, actual)
