import csv
import numpy
import os
import random
import re

from generator.paths import ngrams_dir_path


def _generate_char(ch, config):
    char_class = config.char_class(ch)
    if not char_class:
        raise ValueError("Illegal character class '{}'.".format(ch))
    return random.choice(char_class)


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
                    raise ValueError("Max range less than min range")
            else:
                max_length = min_length
    char_class = descriptor[0]
    return char_class, min_length, max_length, pattern[len(descriptor):]


def _choose_ngram_char(d, s):
    start = s if len(s) == 1 else s[-2:]
    ngrams = {}
    for ch in "abcdefghijklmnopqrstuvwxyz":
        ngram = start + ch
        if ngram in d:
            ngrams[ngram] = d[ngram]
        else:
            ngrams[ngram] = 0
    return _weighted_random(ngrams)[-1]


def _weighted_random(d):
    population = []
    weights = []
    for k, v in d.items():
        population.append(k)
        weights.append(v)
    total = sum(weights)
    if total == 0:  # This shouldn't happen
        return random.choice(population)
    weights = [x / total for x in weights]
    return numpy.random.choice(population, p=weights)


def _load_ngrams(file_name):
    path = os.path.join(os.path.dirname(__file__), ngrams_dir_path())
    path = os.path.join(path, file_name)
    d = {}
    with open(path, 'r') as f:
        r = csv.reader(f)
        for row in r:
            try:
                d[row[0]] = int(row[1])
            except ValueError:
                pass
    return d


def generate_pronounceable(length):
    if length < 4:
        raise ValueError("Pronounceable passwords must be at least four characters long.")
    s = _weighted_random(_load_ngrams('ngrams1_start.csv'))
    s += _choose_ngram_char(_load_ngrams('ngrams2_start.csv'), s)
    s += _choose_ngram_char(_load_ngrams('ngrams3_start.csv'), s)
    d = _load_ngrams('ngrams3.csv')
    for i in range(length - 4):
        s += _choose_ngram_char(d, s)
    s += _choose_ngram_char(_load_ngrams('ngrams3_end.csv'), s)
    return s


def generate(config, pattern):
    pattern = pattern.strip()
    ordered = False
    if pattern[0].lower() == 'o':
        ordered = True
        pattern = pattern[1:]
    password = ''
    while pattern:
        char_class, min_length, max_length, pattern = _match_descriptor(pattern)
        n = random.randint(min_length, max_length)
        for i in range(n):
            password += _generate_char(char_class, config)
    if not ordered:
        password = _shuffle_chars(password)
    return password


def generate_from_type(config, type_name):
    try:
        pattern = config.types[type_name]
        return generate(config, pattern)
    except KeyError:
        raise ValueError("No type named {} defined.".format(type_name))
