# coding: utf-8

from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *


class TextAnalyser:
    def __init__(self):
        pass

    def analyser(self, keep_filter):
        char_filters = [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(u'蛇の目', u'janome')]
        tokenizer = Tokenizer()
        token_filters = [CompoundNounFilter(), POSKeepFilter(keep_filter), LowerCaseFilter()]
        return Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)

    def get_sentence(self, a, text):
        sentence = ''
        for token in a.analyze(text):
            text_to_test = [char for char in token.base_form]
            for letter in text_to_test:
                if len(letter.encode('utf-8')) > 1:
                    if '代名詞' not in token.extra[0]:
                        sentence += 'と' + token.surface if len(sentence) > 0 else token.surface
                        break
                else:
                    sentence += ' ' + token.surface if len(sentence) > 0 else token.surface
                    break

        return sentence
