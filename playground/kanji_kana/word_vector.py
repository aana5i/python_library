# -*- coding: utf-8 -*-

import pickle
from gensim.models import word2vec


## FIELD: useful functions
def from_text(path, mode, encoding='utf-8'):
    _encoding = ['utf-8', 'shift_jis']
    with open(path, mode=mode, encoding=[_encoding[encoding] if isinstance(encoding, int) else encoding][0]) as f:
        result = f.read()  # str
    return result


def save_pickle(path, filename, mode='wb'):
    with open(path, mode=mode) as f:  # pickleに保存
        pickle.dump(filename, f)


def from_pickle(path, mode='rb'):
    with open(path, mode=mode) as f:
        result = pickle.load(f)
    return result


## PROCESS
def load_tokenize_data():
    result = from_pickle('data/wagahai_words.pickle')
    return result


wagahai_words = load_tokenize_data()
# size : 中間層のニューロン数 / number of neurones
# min_count : この値以下の出現回数の単語を無視 / ignore word who are present less than ...
# window : 対象単語を中心とした前後の単語数 / number of word before and after the current word
# iter : epochs数
# sg : skip-gramを使うかどうか 0:CBOW 1:skip-gram
model = word2vec.Word2Vec(wagahai_words,
                          size=100,
                          min_count=5,
                          window=5,
                          iter=20,
                          sg=0)

print(model.wv.most_similar(positive=["猫", "人間"]))  # search for more similar neko + ningen
print(model.wv.most_similar(positive=["人間", "猫"], negative=["夢"])) # search for more similar neko + ningen - yume
