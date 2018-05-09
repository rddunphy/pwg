import unittest

from generator.generator import generate, generate_pronounceable, generate_from_type
from generator.config import Config


class GeneratorTest(unittest.TestCase):

    def test_basic(self):
        pattern = "lunNsxSaAhHbcC"
        password = generate(Config(), pattern)
        self.assertEqual(len(password), 14)

    def test_length_descriptor(self):
        pattern = "a{10}"
        password = generate(Config(), pattern)
        self.assertEqual(len(password), 10)

    def test_range_descriptor(self):
        pattern = "h{5-6}"
        password = generate(Config(), pattern)
        self.assertGreaterEqual(len(password), 5)
        self.assertLessEqual(len(password), 6)

    def test_optional_descriptor(self):
        pattern = "nN?"
        password = generate(Config(), pattern)
        self.assertGreaterEqual(len(password), 1)
        self.assertLessEqual(len(password), 2)

    def test_ordered(self):
        pattern = "onu{20}n"
        password = generate(Config(), pattern)
        self.assertEqual(len(password), 22)
        try:
            int(password[0])
            int(password[21])
        except ValueError:
            self.fail("Numerals not at expected indices")

    def test_illegal_character_class(self):
        pattern = "nay"
        with self.assertRaises(ValueError):
            generate(Config(), pattern)

    def test_illegal_ordered_placement(self):
        pattern = "no"
        with self.assertRaises(ValueError):
            generate(Config(), pattern)

    def test_illegal_descriptor_range(self):
        pattern = "n{20-10}"
        with self.assertRaises(ValueError):
            generate(Config(), pattern)

    def test_descriptor_range_syntax_error(self):
        pattern = "n{10-20"
        with self.assertRaises(ValueError):
            generate(Config(), pattern)

    def test_pronounceable(self):
        password = generate_pronounceable(10)
        self.assertEqual(len(password), 10)

    def test_pronounceable_length(self):
        password = generate_pronounceable(4)
        self.assertEqual(len(password), 4)
        with self.assertRaises(ValueError):
            generate_pronounceable(3)

    def test_generate_from_type(self):
        password = generate_from_type(Config(), 'pin')
        try:
            int(password)
        except ValueError:
            self.fail("PIN password contains non-numerals")
        self.assertEqual(len(password), 4)
