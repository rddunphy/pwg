import random

substitutions = {
    'a': ['@', '4'],
    'b': ['8', '6'],
    'c': ['(', '<'],
    'd': ['6'],
    'e': ['3'],
    'f': ['#'],
    'g': ['9'],
    'h': ['#'],
    'i': ['1', '!'],
    'k': ['<', '/<'],
    'l': ['1', '/'],
    'n': ['^'],
    'o': ['0', '*'],
    'q': ['9'],
    's': ['$', '5'],
    't': ['+'],
    'v': ['<', '>'],
    'w': ['uu', '2u'],
    'x': ['%'],
    'y': ['?'],
    'z': ['2']
}


def _toggle_case(ch):
    if ch == ch.lower():
        return ch.upper()
    return ch.lower()


def _substitute_char(ch):
    ch = ch.lower()
    if ch in substitutions:
        return random.choice(substitutions[ch])
    else:
        return _toggle_case(ch)


def substitute(string, config):
    length = len(string)
    n_subst = round(length * config.munge_subst_factor)
    n_caps = round(length * config.munge_caps_factor)
    subst_chars = random.sample(range(length), n_subst)
    caps_pop = [x for x in range(length) if x not in subst_chars]
    caps_chars = random.sample(caps_pop, n_caps)
    result = ""
    for i, ch in enumerate(string):
        if i in subst_chars:
            result += _substitute_char(ch)
        elif i in caps_chars:
            result += _toggle_case(ch)
        else:
            result += ch
    return result
