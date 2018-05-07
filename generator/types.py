import os

types_path = "../types.txt"


class TypeFileFormatException(Exception):

    def __init__(self, message):
        self.message = "Invalid type file format: " + message


def load_types():
    path = os.path.join(os.path.dirname(__file__), types_path)
    types = {}
    with open(path) as f:
        lines = f.readlines()
        for l, line in enumerate(lines):
            line = line.strip()
            if len(line) > 0:
                words = line.split()
                if len(words) != 2:
                    raise TypeFileFormatException("Wrong number of words on line {}.".format(l))
                name = words[0]
                pattern = words[1]
                types[name] = pattern
    return types


def get_type_pattern(type_name):
    type_name = type_name.lower()
    types = load_types()
    if type_name not in types:
        raise ValueError("No type named {} defined.".format(type_name))
    return types[type_name]
