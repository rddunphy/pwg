import unittest

from generator.phrases import generate_phrase


class PhrasesTest(unittest.TestCase):

    @staticmethod
    def _count_upper(phrase):
        return sum(1 for c in phrase if c.isupper())

    def test_basic(self):
        phrase = generate_phrase("n")
        self.assertGreater(len(phrase), 3)
        self.assertEqual(self._count_upper(phrase), 1)

    def test_all_types(self):
        phrase = generate_phrase("navw")
        self.assertGreater(len(phrase), 3)
        self.assertEqual(self._count_upper(phrase), 4)

    def test_no_pattern(self):
        phrase = generate_phrase("")
        self.assertEqual(phrase, "")
