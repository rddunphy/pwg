import unittest

from generator.config import Config


class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.config = Config()

    def test_set_type(self):
        self.config.set_type("mytype", "xxx")
        self.assertEqual(self.config.types["mytype"], "xxx")

    def test_remove_type(self):
        self.config.set_type("mytype", "xxx")
        self.assertTrue("mytype" in self.config.types)
        self.config.remove_type("mytype")
        self.assertFalse("mytype" in self.config.types)

    def test_remove_default(self):
        default = self.config.types["default"]
        self.config.set_type("default", "xxx")
        self.assertEqual(self.config.types["default"], "xxx")
        self.config.remove_type("default")
        self.assertEqual(self.config.types["default"], default)

    def test_add_chars_to_class(self):
        original = self.config.char_class('n')
        self.config.add_chars_to_class('n', "xyz123")
        self.assertEqual(self.config.char_class('n'), original + "xyz")

    def test_add_to_invalid_class(self):
        with self.assertRaises(ValueError):
            self.config.add_chars_to_class('y', "xyz")

    def test_remove_chars_from_class(self):
        self.config.remove_chars_from_class('n', "xyz123")
        self.assertEqual(self.config.char_class('n'), "0456789")

    def test_remove_from_invalid_class(self):
        with self.assertRaises(ValueError):
            self.config.remove_chars_from_class('y', "xyz")
