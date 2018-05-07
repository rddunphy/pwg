import pickle
import os

config_path = "../config.p"


class Config:

    def __init__(self):
        self.types = {
            "default":  "c{12-14}",
            "basic":    "A{10-12}",
            "long":     "c{18-20}",
            "secure":   "lunsxC{15}",
            "pin":      "n{4}",
            "colour":   "h{6}"
        }


def _config_path():
    return os.path.join(os.path.dirname(__file__), config_path)


def save_config(config):
    with open(_config_path(), 'wb') as f:
        pickle.dump(config, f)


def load_config():
    path = _config_path()
    if os.path.isfile(path):
        with open(_config_path(), 'rb') as f:
            return pickle.load(f)
    config = Config()
    save_config(config)
    return config
