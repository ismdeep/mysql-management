import json
import os


def load_data_path():
    return os.path.expanduser('~') + '/.mysql-management'


def load_config():
    config_file_path = load_data_path() + '/config.json'
    data = json.load(open(config_file_path, 'r'))
    return data
