# -*- coding: utf-8 -*-

import re
import pickle

from janome.tokenizer import Tokenizer


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


# text_tokenize('data/wagahaiwa_nekodearu.txt', 'wagahai_words.pickle')
