from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from generator.cli import create_parser, gen, confirm, munge, reset, add_chars, remove_chars, save, pronounceable


class CLITest(TestCase):

    def setUp(self):
        self.parser = create_parser()

    @patch("builtins.input", side_effect=['n', 'N'])
    def test_confirm_no(self, _):
        answer = confirm("yes?")
        self.assertFalse(answer)
        answer = confirm("yes?")
        self.assertFalse(answer)

    @patch("builtins.input", side_effect=['y', ''])
    def test_confirm_yes(self, _):
        answer = confirm("yes?")
        self.assertTrue(answer)
        answer = confirm("yes?")
        self.assertTrue(answer)

    @patch("sys.stdout", new_callable=StringIO)
    def test_gen(self, mock_stdout):
        args = self.parser.parse_args(["-p", "xxx"])
        gen(args)
        result = mock_stdout.getvalue().strip()
        self.assertEqual(len(result), 3)

    @patch("pyperclip.copy")
    @patch("sys.stdout", new_callable=StringIO)
    def test_gen_copy(self, mock_stdout, _):
        args = self.parser.parse_args(["-c", "-p", "xxx"])
        gen(args)
        result = mock_stdout.getvalue().strip()
        self.assertEqual(result, "Password copied to clipboard.")

    @patch("sys.stdout", new_callable=StringIO)
    def test_pronounceable(self, mock_stdout):
        args = self.parser.parse_args(["pronounceable", "-l", "8"])
        pronounceable(args)
        result = mock_stdout.getvalue().strip()
        self.assertEqual(len(result), 8)


class ParserTest(TestCase):

    def setUp(self):
        self.parser = create_parser()

    def test_no_args(self):
        args = self.parser.parse_args([])
        self.assertEqual(args.func, gen)
        self.assertFalse(args.copy)
        self.assertIsNone(args.pattern)
        self.assertEqual(args.type, 'default')
        self.assertFalse(args.munge)

    def test_pattern_args(self):
        args = self.parser.parse_args(["-c", "-p", "xxx"])
        self.assertEqual(args.func, gen)
        self.assertTrue(args.copy)
        self.assertEqual(args.pattern, "xxx")
        self.assertEqual(args.type, 'default')
        self.assertFalse(args.munge)

    def test_type_args(self):
        args = self.parser.parse_args(["-m", "-t", "pin"])
        self.assertEqual(args.func, gen)
        self.assertFalse(args.copy)
        self.assertIsNone(args.pattern)
        self.assertEqual(args.type, 'pin')
        self.assertTrue(args.munge)

    def test_munge(self):
        args = self.parser.parse_args(["munge", "mypassword"])
        self.assertEqual(args.func, munge)
        self.assertEqual(args.string, "mypassword")

    def test_reset(self):
        args = self.parser.parse_args(["reset"])
        self.assertEqual(args.func, reset)

    def test_add_chars(self):
        args = self.parser.parse_args(["add_chars", "n", "xyz"])
        self.assertEqual(args.func, add_chars)
        self.assertEqual(args.cls, "n")
        self.assertEqual(args.chars, "xyz")

    def test_remove_chars(self):
        args = self.parser.parse_args(["remove_chars", "n", "xyz"])
        self.assertEqual(args.func, remove_chars)
        self.assertEqual(args.cls, "n")
        self.assertEqual(args.chars, "xyz")

    def test_save(self):
        args = self.parser.parse_args(["save", "mytype", "xxx"])
        self.assertEqual(args.func, save)
        self.assertEqual(args.name, "mytype")
        self.assertEqual(args.pattern, "xxx")
