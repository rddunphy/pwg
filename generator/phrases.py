import random

import re
from enum import Enum

import nltk

from generator.paths import dictionary_path


class Word(Enum):
    ANY = 0
    NOUN = 1
    VERB = 2
    ADJ = 3


def _clean(word, regex):
    return regex.sub('', word.lower())


def _build_dict_file(fdist, word_type, min_length):
    words = list(fdist[word_type])
    words = [w for w in words if len(w) > min_length - 1]
    with open(dictionary_path(word_type.name), 'w') as f:
        f.write('\n'.join(words))


def build_dictionary():
    nltk.download("brown")
    regex = re.compile('[^a-z]')
    words = nltk.corpus.brown.tagged_words(tagset="universal")
    fdist = nltk.ConditionalFreqDist((t, _clean(w, regex)) for w, t in words)
    min_length = 4
    _build_dict_file(fdist, Word.NOUN, min_length)
    _build_dict_file(fdist, Word.VERB, min_length)
    _build_dict_file(fdist, Word.ADJ, min_length)


def _load_words(word_type):
    words = []
    with open(dictionary_path(word_type.name), 'r') as f:
        for line in f.readlines():
            words.append(line.strip())
    return words


def load_dictionary():
    d = {
        Word.VERB: _load_words(Word.VERB),
        Word.NOUN: _load_words(Word.NOUN),
        Word.ADJ: _load_words(Word.ADJ)
    }
    d[Word.ANY] = list(set(d[Word.VERB] + d[Word.NOUN] + d[Word.ADJ]))
    return d


def _choose_word(d, word_type):
    return random.choice(d[word_type]).title()


def generate_phrase(pattern="nvan"):
    d = load_dictionary()
    pattern = pattern.lower()
    phrase = ""
    for ch in pattern:
        if ch == 'v':
            word_type = Word.VERB
        elif ch == 'a':
            word_type = Word.ADJ
        elif ch == 'n':
            word_type = Word.NOUN
        else:
            word_type = Word.ANY
        phrase += _choose_word(d, word_type)
    return phrase
