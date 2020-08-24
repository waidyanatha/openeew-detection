from unittest import TestCase
from unittest.mock import patch


class SaveDeviceTest(TestCase):
    @patch('db.execute_statement')
    def test_device_is_persisted(self, mock_execute_statement):
        from devices import save_device
        input = {
            'device_id': '2351n2x55',
            'latitude': 19.35,
            'longitude': -99.14,
            'firmware_version': 1.2,
            'device_type': 'esp32',
            'time_entered': 1597685615,
        }
        save_device(input)
        mock_execute_statement.assert_called_once()
