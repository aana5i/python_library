# -*- coding: utf-8 -*-

from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *


def get_words_list(sentence):
    """
    get list of name words
    :param sentence: string
    :return: list of string
    """
    words_list = []
    char_filters = [UnicodeNormalizeCharFilter(),
                    RegexReplaceCharFilter('<.*?>', '')]

    token_filters = [POSKeepFilter(['名詞']),
                     LowerCaseFilter(),
                     ExtractAttributeFilter('surface')]

    a = Analyzer(char_filters=char_filters, token_filters=token_filters)

    for token in a.analyze(sentence):
        words_list.append(token)

    # japanese words can be split in 2 different words
    if len(words_list) == 4:
        words_list[0] = words_list[0] + words_list[1]
        words_list.pop(1)

    return words_list


"""
USAGE

s = 'youtubeでカメラの作り方'
words_list = get_words_list(s)
"""
