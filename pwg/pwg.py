import argparse
import textwrap
import pyperclip

cs_lower = 'abcdefgehijklmnopqrstuvwxyz'
cs_upper = 'ABCDEFGEHIJKLMNOPQRSTUVWXYZ'
cs_num = '0123456789'
cs_non_zero = '123456789'
cs_special = '!$%^&*@#;:?+=_-,.'
cs_ext_special = '"£()[]{}~\'/\\<>`|'
cs_all_special = cs_special + cs_ext_special
cs_alpha = cs_lower + cs_upper
cs_alphanumeric = cs_alpha + cs_num
cs_hex = cs_num + 'abcdef'
cs_upper_hex = cs_num + 'ABCDEF'
cs_bin = '01'
cs_basic = cs_alphanumeric + cs_special
cs_ext = cs_basic + cs_ext_special

charsets = {
    'l': cs_lower,
    'u': cs_upper,
    'n': cs_num,
    'N': cs_non_zero,
    's': cs_special,
    'x': cs_ext_special,
    'S': cs_all_special,
    'a': cs_alpha,
    'A': cs_alphanumeric,
    'h': cs_hex,
    'H': cs_upper_hex,
    'b': cs_bin,
    '+': cs_basic,
    '#': cs_ext
}


def generate(pattern):
    ordered = 'o' in pattern
    return pattern


def run():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description='Generate passwords.',
        epilog=textwrap.dedent('''
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
              + - alphanumeric or basic special
              # - any character
              ? - make previous character class optional
              {3} - repeat previous character class 3 times
              {3-5} - repeat previous character class 3 to 5 times
              o - preserve pattern order
        ''')
    )
    parser.add_argument('-c', '--copy', action='store_true', help='copy password to clipboard and don\'t display')
    parser.add_argument('-p', '--pattern', type=str, default='+{10-12}', help='pattern to generate password from')

    args = parser.parse_args()

    password = generate(args.pattern)

    if args.copy:
        pyperclip.copy(password)
        print("Password copied to clipboard.")
    else:
        print(password)


if __name__ == '__main__':
    run()
