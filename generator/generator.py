import re
import random

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

char_classes = {
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
    'c': cs_basic,
    'C': cs_ext
}


class IllegalPatternException(Exception):

    def __init__(self, message):
        self.message = "Illegal pattern: " + message


def _generate_char(c):
    if c in char_classes:
        char_class = char_classes[c]
        return char_class[random.randrange(len(char_class))]
    return ''


def _shuffle_chars(s):
    chars = list(s)
    random.shuffle(chars)
    return ''.join(chars)


def _match_descriptor(pattern):
    regexp = '.(\?|(\{[0-9]+(-[0-9]+)?\}))?'
    match = re.match(regexp, pattern)
    descriptor = match.group(0)
    min_length = max_length = 1
    if len(descriptor) > 1:
        if descriptor[1] == '?':
            min_length = 0
        else:
            regexp = '[0-9]+'
            matches = re.findall(regexp, descriptor)
            min_length = int(matches[0])
            if len(matches) > 1:
                max_length = int(matches[1])
                if max_length < min_length:
                    raise IllegalPatternException("Max range less than min range")
            else:
                max_length = min_length
    char_class = descriptor[0]
    return char_class, min_length, max_length, pattern[len(descriptor):]


def generate(pattern):
    ordered = False
    if pattern[0] == 'o':
        ordered = True
        pattern = pattern[1:]
    password = ''
    while pattern:
        char_class, min_length, max_length, pattern = _match_descriptor(pattern)
        if char_class not in char_classes:
            raise IllegalPatternException("Illegal character class '" + char_class + "'")
        n = random.randint(min_length, max_length)
        for i in range(n):
            password += _generate_char(char_class)
    if not ordered:
        password = _shuffle_chars(password)
    return password
