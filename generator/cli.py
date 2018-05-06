import textwrap
import pyperclip
import argparse

from generator.generator import generate, generate_from_type
from generator.types import IllegalTypeException


def run():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Generate passwords.",
        epilog=textwrap.dedent("""
            Patterns are sequences of character classes specified as follows:

              l - lower case
              u - upper case
              n - numeral
              N - numeral without 0
              s - basic special
              x - extended special
              S - any special
              a - alphabetic
              A - alphanumeric
              h - hexadecimal
              H - upper case hexadecimal
              b - binary
              c - alphanumeric or basic special character
              C - any character
              ? - make previous character class optional
              {3} - repeat previous character class 3 times
              {3-5} - repeat previous character class 3 to 5 times
              o - (at start of pattern) preserve pattern order
        """)
    )
    parser.add_argument(
        '-c', '--copy',
        action='store_true',
        help="copy password to clipboard and don\'t display"
    )
    parser.add_argument(
        '-p', '--pattern',
        type=str, default=None,
        help="pattern to generate password from"
    )
    parser.add_argument(
        '-t', '--type',
        type=str, default="default",
        help="named type of password to generate"
    )

    args = parser.parse_args()

    try:
        if args.pattern:
            password = generate(args.pattern)
        else:
            password = generate_from_type(args.type)

        if args.copy:
            pyperclip.copy(password)
            print("Password copied to clipboard.")
        else:
            print(password)
    except IllegalTypeException as e:
        print(e.message)
