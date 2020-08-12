# -*- coding: utf-8 -*-

import pickle

from gensim.models import word2vec
import numpy as np


## FIELD: useful functions
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

print(model.wv.most_similar("猫"))  # 最も似ている単語 / most similar word

a = model.wv.__getitem__("猫")
b = model.wv.__getitem__("人間")
# caculer la racine carree de la somme des carres (norme)
cos_sim = np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b)  # linalg.normで二乗和の平方根（ノルム）を計算
print(cos_sim)
