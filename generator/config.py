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
        self._basic_char_classes = {
            'l': 'abcdefgehijklmnopqrstuvwxyz',
            'u': 'ABCDEFGEHIJKLMNOPQRSTUVWXYZ',
            'n': '0123456789',
            'N': '123456789',
            's': '!$%^&*@#;:?+=_-,.',
            'x': '"£()[]{}~\'/\\<>`|',
            'h': '0123456789abcdef',
            'H': '0123456789ABCDEF',
            'b': '01'
        }
        self._compound_char_classes = {
            'S': ['s', 'x'],
            'a': ['l', 'u'],
            'A': ['l', 'u', 'n'],
            'c': ['l', 'u', 'n', 's'],
            'C': ['l', 'u', 'n', 's', 'x']
        }
        self.munge_subst_factor = 0.25
        self.munge_caps_factor = 0.35

    def set_type(self, name, pattern):
        self.types[name] = pattern

    def remove_type(self, name):
        if name == "default":
            self.types[name] = "c{12-14}"
        else:
            del self.types[name]

    def char_class(self, ch):
        if ch in self._basic_char_classes:
            return self._basic_char_classes[ch]
        if ch in self._compound_char_classes:
            basic_classes = self._compound_char_classes[ch]
            chars = [self._basic_char_classes[x] for x in basic_classes]
            return ''.join(chars)
        return None

    def add_chars_to_class(self, ch, s):
        try:
            for c in s:
                if c not in self._basic_char_classes[ch]:
                    self._basic_char_classes[ch] += c
        except KeyError:
            raise ValueError("'{}' is not a basic character class.".format(ch))

    def remove_chars_from_class(self, ch, s):
        try:
            for c in s:
                if c in self._basic_char_classes[ch]:
                    self._basic_char_classes[ch] = self._basic_char_classes[ch].replace(c, '')
        except KeyError:
            raise ValueError("'{}' is not a basic character class.".format(ch))


def _config_path():
    return os.path.join(os.path.dirname(__file__), config_path)


def reset_config():
    config = Config()
    save_config(config)
    return config


def save_config(config):
    with open(_config_path(), 'wb') as f:
        pickle.dump(config, f)


def load_config():
    path = _config_path()
    if os.path.isfile(path):
        with open(_config_path(), 'rb') as f:
            return pickle.load(f)
    return reset_config()
