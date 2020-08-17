from openeew.db import execute_statement


def save_device(device):
    statement = '''
        INSERT INTO devices (
            device_id,
            latitude,
            longitude,
            firmware_version,
            device_type,
            time_entered
        ) VALUES (?, ?, ?, ?, ?, ?)
    '''
    parameters = (
        device['device_id'],
        device['latitude'],
        device['longitude'],
        device['firmware_version'],
        device['device_type'],
        device['time_entered'],
    )
    execute_statement(statement, parameters)
