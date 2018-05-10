import random


def _toggle_case(ch):
    if ch == ch.lower():
        return ch.upper()
    return ch.lower()


def _substitute_char(ch, substitutions):
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
            result += _substitute_char(ch, config.substitutions)
        elif i in caps_chars:
            result += _toggle_case(ch)
        else:
            result += ch
    return result
