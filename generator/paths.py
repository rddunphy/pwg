import os

ROOT = "../"
CONFIG_PATH = "config.p"
DATA_PATH = "data"


def absolute_path(root_rel_path):
    rel_path = os.path.join(os.path.dirname(__file__), ROOT, root_rel_path)
    return os.path.abspath(rel_path)


def config_path():
    return absolute_path(CONFIG_PATH)


def data_path():
    return absolute_path(DATA_PATH)
