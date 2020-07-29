from paho.mqtt.client import Client as MqttClient
from time import sleep
from json import dumps as json_dumps
from argparse import ArgumentParser
from os import listdir
from os.path import dirname, realpath, isdir, isfile, join as join_paths, splitext

input_directory = f'{dirname(realpath(__file__))}/../input'


def create_client(host, port, username, password):
    client = MqttClient()
    if username and password:
        client.username_pw_set(username=username, password=password)
    client.connect(host=host, port=port)
    return client


def build_sensors(earthquake_directory, provide_sensor_client):
    sensors = []
    for sensor_id in listdir(path=earthquake_directory):
        sensor_directory = join_paths(earthquake_directory, sensor_id)
        if isdir(sensor_directory):
            data_files = []
            for data_file in listdir(path=sensor_directory):
                data_file_path = join_paths(sensor_directory, data_file)
                if isfile(path=data_file_path):
                    data_files.append({
                        'path': data_file_path,
                        'index': int(splitext(data_file)[0]),
                    })
            data_files.sort(key=lambda data_file_to_sort: data_file_to_sort['index'])
            sensor = {
                'id': sensor_id,
                'client': provide_sensor_client(),
                'data_files': data_files,
            }
            sensors.append(sensor)
    sensors.sort(key=lambda sensor_to_sort: sensor_to_sort['id'])
    return sensors


def get_next_index(sensors):
    next_index = None
    for sensor in sensors:
        if sensor['data_files']:
            data_file_index = sensor['data_files'][0]['index']
            if not next_index or data_file_index < next_index:
                next_index = data_file_index
    return next_index


def remove_index(sensors, index_to_remove):
    for sensor in sensors:
        new_data_files = [data_file for data_file in sensor['data_files'] if data_file['index'] != index_to_remove]
        sensor['data_files'] = new_data_files


def send_next_line(sensor, file):
    line = file.readline()
    if line:
        json_line = json_dumps(line)
        client = sensor['client']
        client.loop_start()
        client.publish('/traces', json_line)
        return True
    return False


def open_files(sensors, index):
    opened_files = []
    for sensor in sensors:
        index_data_files = [data_file for data_file in sensor['data_files'] if data_file['index'] == index]
        for index_data_file in index_data_files:
            opened_files.append({
                'sensor': sensor,
                'file': open(file=index_data_file['path'], mode='r'),
            })
    return opened_files


def run():
    parser = ArgumentParser()
    parser.add_argument("--username", help="MQTT username")
    parser.add_argument("--password", help="MQTT password")
    parser.add_argument("--port", help="MQTT port", nargs="?", type=int, const=1883, default=1883)
    parser.add_argument("--earthquake", help="Earthquake directory")
    parser.add_argument("--frequency", help="Frequency in seconds between each signal", type=int, default=1)
    arguments = parser.parse_args()

    def provide_sensor_client():
        return create_client("localhost", arguments.port, arguments.username, arguments.password)

    earthquake_directory = join_paths(input_directory, arguments.earthquake)
    sensors = build_sensors(earthquake_directory=earthquake_directory, provide_sensor_client=provide_sensor_client)
    print(f'📻 Found {len(sensors)} sensors for the {arguments.earthquake} earthquake')

    try:
        index = get_next_index(sensors=sensors)
        while index is not None:
            print(f'🚀 Sending files with index {index}')
            opened_files = open_files(sensors=sensors, index=index)
            try:
                while opened_files:
                    for opened_file in opened_files:
                        sensor = opened_file['sensor']
                        file = opened_file['file']
                        if not send_next_line(sensor, file):
                            file.close()
                            opened_files.remove(opened_file)
                            print(f'✅ File {index} from sensor {opened_file["sensor"]["id"]} sent')
                    sleep(arguments.frequency)
            finally:
                for opened_file in opened_files:
                    try:
                        opened_file['file'].close()
                    except Exception as exception:
                        print(exception)
            remove_index(sensors=sensors, index_to_remove=index)
            print(f'✅ Index {index} sent')
            index = get_next_index(sensors=sensors)
    finally:
        for sensor in sensors:
            try:
                sensor['client'].disconnect()
            except Exception as exception:
                print(exception)


run()
