# -*- coding: utf-8 -*-

from textblob import TextBlob


text = '日本語（にほんご、にっぽんご）は、主に日本国内や日本人同士の間で使用されている言語である。'
blob = TextBlob(text)


class Nlp:
    def __init__(self, text):
        self.get_sentence(text)

    def get_sentence(self, text):
        self.text = TextBlob(text)

    def detect_language(self):
        return self.text.detect_language()

    def words(self):
        return self.text.words

    def words_counts(self, word):
        return self.text.words.count(word)

    def tags(self):
        return self.text.tags

    def sentiment(self):
        return self.text.sentiment


# 言語抽出
analysis = "TextBlob sure looks like it has some interesting features"
nlp = Nlp(analysis)
print(nlp.detect_language())
print(nlp.words())
print(nlp.words_counts('it'))
print(nlp.tags())
print(nlp.sentiment())

"""
A refaire, juste utiliser textblob quand le phrase est en anglais pour les words, semntisation, counts ect. sinon utiliser janome
"""
