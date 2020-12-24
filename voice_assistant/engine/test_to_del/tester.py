# coding: utf-8

from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *


def analyser(keep_filter):
    char_filters = [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(u'蛇の目', u'janome')]
    tokenizer = Tokenizer()
    token_filters = [CompoundNounFilter(), POSKeepFilter(keep_filter), LowerCaseFilter()]
    return Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)


def get_sentence(a, text):
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

a = analyser('名詞')

text = 'わたしは猫の画像を探しました。'
print(get_sentence(a, text))
print()
print()

text = '犬と猫の画像を探したいです。'
print(get_sentence(a, text))

print()
print()

text = 'lofi hip hop radio - beats to relax/study toを見せてください'
print(get_sentence(a, text))

# わたし  名詞,代名詞,一般,*,*,*,わたし,ワタシ,ワタシ
# ('名詞,代名詞,一般,*', '*', '*', 'わたし', 'ワタシ', 'ワタシ')
# 猫      名詞,一般,*,*,*,*,猫,ネコ,ネコ
# ('名詞,一般,*,*', '*', '*', '猫', 'ネコ', 'ネコ')
# 画像    名詞,一般,*,*,*,*,画像,ガゾウ,ガゾー
# ('名詞,一般,*,*', '*', '*', '画像', 'ガゾウ', 'ガゾー')
# ['base_form', 'extra', 'node', 'surface']
