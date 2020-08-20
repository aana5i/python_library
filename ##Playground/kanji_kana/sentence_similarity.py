# -*- coding: utf-8 -*-

import pickle
from gensim.models import word2vec
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument


## FIELD: useful functions
def from_text(path, mode, encoding='utf-8'):
    _encoding = ['utf-8', 'shift_jis']
    with open(path, mode=mode, encoding=[_encoding[encoding] if isinstance(encoding, int) else encoding][0]) as f:
        result = f.read()  # str
    return result


def save_pickle(path, data, mode='wb'):
    with open(path, mode=mode) as f:  # pickleに保存
        pickle.dump(data, f)


def from_pickle(path, mode='rb'):
    with open(path, mode=mode) as f:
        result = pickle.load(f)
    return result


## PROCESS
wagahai_words = from_pickle('data/wagahai_words.pickle')

tagged_documents = []
for i, sentence in enumerate(wagahai_words):
    tagged_documents.append(TaggedDocument(sentence, [i]))  # TaggedDocument型のオブジェクトをリストに格納

# size：分散表現の次元数
# window：対象単語を中心とした前後の単語数
# min_count：学習に使う単語の最低出現回数
# epochs:epochs数
# dm：学習モデル=DBOW（デフォルトはdm=1で、学習モデルはDM）
model = Doc2Vec(documents=tagged_documents,
                vector_size=100,
                min_count=5,
                window=5,
                epochs=20,
                dm=0)

print(wagahai_words[0])  # 最初の文章を表示 / first sentence
print('0')
print(model.docvecs[0])  # 最初の文章のベクトル / first sentence vector
print('1')
print(model.docvecs.most_similar(0))
print('2')
for p in model.docvecs.most_similar(0):
    print(''.join(wagahai_words[p[0]]))
