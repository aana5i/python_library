# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
import numpy as np
import pandas as pd
from pprint import pprint
from japanese_parser import JpParser


with open('db.txt', 'r', encoding='utf-8') as f:
    content = f.readlines()


print(content[0])
# Create the Dictionary and Corpus
mydict = corpora.Dictionary(content[0])

# # Show the Word Weights in Corpus
# for doc in corpus:
#     print([[mydict[id], freq] for id, freq in doc])



# # Create the TF-IDF model
# tfidf = models.TfidfModel(corpus, smartirs='ntc')
#
# # Show the TF-IDF weights
# for doc in tfidf[corpus]:
#     print([[mydict[id], np.around(freq, decimals=2)] for id, freq in doc])


keyword = 'サッカー'
feature_cnt = len(mydict.token2id)
corpus = [mydict.doc2bow(text) for text in content[0]]
tfidf = models.TfidfModel(corpus)
kw_vector = mydict.doc2bow(keyword)
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = feature_cnt)
sim = index[tfidf[kw_vector]]
for i in range(len(sim)):
    print('keyword is similar to text%d: %.2f' % (i + 1, sim[i]))
