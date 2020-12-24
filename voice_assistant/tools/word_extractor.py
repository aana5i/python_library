# -*- coding: utf-8 -*-
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *


def get_words_list(sentence):
    """
    文中の名詞を抽出する。
    :param sentence: string
    :return: list of string
    """
    result_list = []
    stop_words = ["あそこ","あっ","あの","あのかた","あの人","あり","あります","ある","あれ","い","いう","います","いる","う","うち","え","お","および","おり","おります","か","かつて","から","が","き","ここ","こちら","こと","この","これ","これら","さ","さらに","し","しかし","する","ず","せ","せる","そこ","そして","その","その他","その後","それ","それぞれ","それで","た","ただし","たち","ため","たり","だ","だっ","だれ","つ","て","で","でき","できる","です","では","でも","と","という","といった","とき","ところ","として","とともに","とも","と共に","どこ","どの","な","ない","なお","なかっ","ながら","なく","なっ","など","なに","なら","なり","なる","なん","に","において","における","について","にて","によって","により","による","に対して","に対する","に関する","の","ので","のみ","は","ば","へ","ほか","ほとんど","ほど","ます","また","または","まで","も","もの","ものの","や","よう","より","ら","られ","られる","れ","れる","を","ん","何","及び","彼","彼女","我々","特に","私","私達","貴方","貴方方"]
    for word in stop_words:
        sentence = sentence.replace(word, '')

    char_filters = [UnicodeNormalizeCharFilter(),
                    RegexReplaceCharFilter('<.*?>', '')]

    token_filters = [POSKeepFilter(['名詞']), LowerCaseFilter(), ExtractAttributeFilter('surface')]# 名詞のみを抽出。

    a = Analyzer(char_filters=char_filters, token_filters=token_filters)

    for token in a.analyze(sentence):
        result_list.append(token)

    if len(result_list) == 4:# クックパッドで'クック'と'パッド'に分解される問題。
        result_list[0] = result_list[0] + result_list[1]# result_list[0]とresult_list[1]を連結。
        result_list.pop(1)# 空いたresult_list[1]を削除。

    return result_list

# usage--このファイルの使い方--
"""
USAGE

s = 'youtubeでカメラの作り方'
words_list = get_words_list(s)
words_list = ["youtube", "カメラ", "作り方"]

"""
# s = 'クックパッドでカメラの作り方'
# get_words_list(s)