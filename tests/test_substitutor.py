import unittest

from generator.config import Config
from generator.substitutor import substitute


class SubstitutorTest(unittest.TestCase):

    def test_basic(self):
        password = "arbitrarytext"
        munged = substitute(password, Config())
        self.assertGreaterEqual(len(munged), len(password))
        self.assertNotEqual(password, munged)

    def test_case_change(self):
        password = "xxxxxxxx"
        munged = substitute(password, Config())
        self.assertTrue('x' in munged)
        self.assertTrue('X' in munged)
        password = "XXXXXXXX"
        munged = substitute(password, Config())
        self.assertTrue('x' in munged)
        self.assertTrue('X' in munged)

    def test_character_substitution(self):
        password = "xxxxxxxx"
        munged = substitute(password, Config())
        self.assertTrue('%' in munged)
        password = "eeeeeeee"
        munged = substitute(password, Config())
        self.assertTrue('3' in munged)

    def test_unsubstitutable_character(self):
        password = "uuuuuuuu"
        munged = substitute(password, Config())
        self.assertTrue('u' in munged)
        self.assertTrue('U' in munged)
        self.assertEqual(len(password), len(munged))
