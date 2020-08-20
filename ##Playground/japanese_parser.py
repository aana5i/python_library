# -*- coding: utf-8 -*-
import re
from pprint import pprint
import json

from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenizer import Tokenizer as JanomeTokenizer  # sumyのTokenizerと名前が被るため
from janome.tokenfilter import POSKeepFilter, ExtractAttributeFilter

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words

import gensim.corpora as corpora
import gensim
from gensim.models import TfidfModel, LdaModel, Phrases, CoherenceModel
from gensim.utils import simple_preprocess
from multiprocessing import freeze_support


# noinspection PyAttributeOutsideInit
class JpParser:
    def __init__(self, doc):
        self.doc = doc
        self.profile = []
        self.text = ''
        self.set_analyzer()

    def open_doc(self):
        with open(self.doc, "r", encoding='utf-8', newline="") as f:
            reader = json.load(f)

        for k, v in reader.items():
            tmp = [v['club'], v['work_info'], v['presentation']]
            for k2, v2 in v.items():
                if 'interview' in k2:
                    tmp.append(v2[0])
                    tmp.append(v2[1])

            self.profile.append('。'.join(tmp))

            self.text = self.profile[0]

    def set_analyzer(self):
        # 形態素解析器を作る
        self.analyzer = Analyzer(
            [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(r'[(\)「」、。]', ' ')],  # ()「」、。は全てスペースに置き換える
            JanomeTokenizer(),
            [POSKeepFilter(['名詞', '形容詞', '副詞', '動詞']), ExtractAttributeFilter('base_form')]  # 名詞・形容詞・副詞・動詞の原型のみ
        )

    def prepare_corpus(self):
        stop_words = ['する', 'れる', 'いる', 'こと', 'なる', 'よう', 'ある', 'られる', 'もの', 'ない', 'の', 'ため', 'これ',
                      'それ', 'これら', 'それぞれ', '%', 'うち', '"', '私', 'さらに', 'せる', 'ん', 'できる', '一', '-', '[', ']',
                      '#', '$', '%', '^', ',']

        self.open_doc()

        # print([t for t in self.profile])
        # 抽出された単語をスペースで連結
        # 末尾の'。'は、この後使うtinysegmenterで文として分離させるため。
        corpus = [
            [
                s
                for s in self.analyzer.analyze(profile)
                if s not in stop_words and s not in get_stop_words('japanese')
            ]
            for profile in self.profile
        ]

        with open('db.txt', 'w', encoding='utf-8') as f:
            for item in corpus:
                f.write(f"{item}\n")

        return corpus


# jp = JpParser("db2.json")
# corpus = jp.prepare_corpus()
# print(corpus)
