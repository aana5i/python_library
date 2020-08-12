# -*- coding: utf-8 -*-

import re
import pickle
from pprint import pprint
from janome.tokenizer import Tokenizer
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
def text_tokenize(from_file, to_file, encoding='utf-8'):
    """

    :param from_file:
    :param to_file:
    :param encoding:
    :return:
    """
    _original = from_text(from_file, mode='r', encoding=encoding)

    # remove useless characters
    _process = re.sub("《[^》]+》", "", _original)  # ルビの削除
    _process = re.sub("［[^］]+］", "", _process)  # 読みの注意の削除
    _process = re.sub("[｜ 　「」\n]", "", _process)  # | と全角半角スペース、「」と改行の削除

    # split in sentences
    seperator = "。"  # 。をセパレータに指定
    _process_list = _process.split(seperator)  # セパレーターを使って文章をリストに分割する
    _process_list.pop()  # 最後の要素は空の文字列になるので、削除 / erase the last element of the list because he's empty
    processed_list = [x+seperator for x in _process_list]  # 文章の最後に。を追加

    # Janome tokenize
    t = Tokenizer()

    processed_words = []
    for sentence in processed_list:
        processed_words.append(t.tokenize(sentence, wakati=True))   # 文章ごとに単語に分割し、リストに格納

    save_pickle(to_file, processed_words)


# text_tokenize('data/wagahaiwa_nekodearu.txt', 'data/wagahai_words.pickle')


def load_tokenize_data():
    return from_pickle('data/wagahai_words.pickle')


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

print(model.wv.vectors.shape)  # 分散表現の形状

print(len(model.wv.index2word))  # 語彙の数
print(model.wv.index2word[:10])  # 最初の10単語 /

print(model.wv.vectors[0])  # 最初のベクトル / first vector
print(model.wv.__getitem__("の"))  # 最初の単語「の」のベクトル / 'no' vector


