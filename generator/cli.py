import textwrap
import pyperclip
import argparse

from generator.config import load_config, save_config, reset_config
from generator.generator import generate, generate_from_type, generate_pronounceable


def confirm(message):
    inp = input(message + " (Y/n) ")
    inp = inp.strip()
    return inp != 'n' and inp != 'N'


def gen(args, config):
    try:
        if args.pattern:
            password = generate(config, args.pattern)
        elif args.type == "pronounceable":
            password = generate_pronounceable(args.length)
        else:
            password = generate_from_type(config, args.type)
        if args.copy:
            pyperclip.copy(password)
            print("Password copied to clipboard.")
        else:
            print(password)
    except ValueError as e:
        print(e)


def save(args, config):
    try:
        if args.pattern:
            generate(config, args.pattern)
            config.set_type(args.name, args.pattern)
            print("Pattern '{}' saved as type '{}'.".format(args.pattern, args.name))
        else:
            if args.name not in config.types:
                raise ValueError("No type named {}.".format(args.name))
            if confirm("Delete type with name {}?".format(args.name)):
                config.remove_type(args.name)
                print("Type {} deleted.".format(args.name))
        save_config(config)
    except ValueError as e:
        print(e)


def reset(*_):
    if confirm("Reset all custom types?"):
        reset_config()
        print("Types reset.")


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
    group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        '-c', '--copy',
        action='store_true',
        help="copy password to clipboard and don\'t display"
    )
    group.add_argument(
        '-p', '--pattern',
        type=str, default=None,
        help="pattern to generate password from"
    )
    group.add_argument(
        '-t', '--type',
        type=str, default="default",
        help="named type of password to generate"
    )
    parser.add_argument(
        '-l', '--length',
        type=int, default=14,
        help="length of variable-length types"
    )
    parser.set_defaults(func=gen)

    subparsers = parser.add_subparsers()

    save_parser = subparsers.add_parser(
        'save', help="save a pattern as a type",
        description="Save a pattern for later use."
    )
    save_parser.add_argument(
        'name', type=str,
        help="name of the type to save"
    )
    save_parser.add_argument(
        'pattern', type=str, nargs='?',
        help="pattern to save"
    )
    save_parser.set_defaults(func=save)

    reset_parser = subparsers.add_parser(
        'reset', help="reset default types",
        description="Reset default types."
    )
    reset_parser.set_defaults(func=reset)

    args = parser.parse_args()
    config = load_config()
    args.func(args, config)
