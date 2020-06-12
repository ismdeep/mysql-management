import json


def load_config():
    config_file_path = 'config.json'
    data = json.load(open(config_file_path, 'r'))
    return data
