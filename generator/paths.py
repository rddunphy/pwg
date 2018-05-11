import os

ROOT = "../"
CONFIG_PATH = "config.p"
NGRAMS_PATH = "data/ngrams"
DICTIONARY_PATH = "data/words"


def absolute_path(root_rel_path):
    rel_path = os.path.join(os.path.dirname(__file__), ROOT, root_rel_path)
    return os.path.abspath(rel_path)


def config_path():
    return absolute_path(CONFIG_PATH)


def ngrams_dir_path():
    return absolute_path(NGRAMS_PATH)


def dictionary_path(word_type):
    dir_path = absolute_path(DICTIONARY_PATH)
    return os.path.join(dir_path, "{}.txt".format(word_type))
