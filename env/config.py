import json


class Config(object):
    def __init__(self, config_file_path, mode):
        with open(config_file_path, 'r') as content:
            data = json.load(content)

            if mode in data:
                self.__dict__ = data[mode]
            else:
                raise ValueError('Env {} not found in env.json'.format(mode))
