from db import execute_statement
from time_utils import get_current_timestamp


def save_earthquake(earthquake):
    statement = '''
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
    parameters = (
        earthquake['event_id'],
        earthquake['time_of_event'],
        earthquake['intensity'],
        earthquake['latitude'],
        earthquake['longitude'],
        earthquake['sensor_ids'],
        get_current_timestamp()
    )
    execute_statement(statement, parameters)
