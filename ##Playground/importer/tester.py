import re
from importer_saver import from_text, to_pickle, from_pickle
from janome.tokenizer import Tokenizer


def preprocess():
    _original = from_text('wagahaiwa_nekodearu.txt')

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

    processed_words = [
        t.tokenize(sentence, wakati=True) for sentence in processed_list
    ]


print(from_pickle('wagahai.pickle'))
