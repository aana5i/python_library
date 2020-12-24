# coding: utf-8

import re
import sys
sys.path.append("../..")
from tools.text_analyser import TextAnalyser


def image(command):
    ta = TextAnalyser()
    if '画像' in command:
        reg_ex = re.search('(.*)画像(.*)', command)
        result = reg_ex.group(1)
        a = ta.analyser('名詞')
        if 'と' in result:
            reg_ex = re.search('(.*)(\Sと\S)(.*)', result)
            result = reg_ex.group(2)
        print(ta.get_sentence(a, result))


if __name__ == '__main__':

    # user = input('何をしたいか？\n')
    user_list = [
        'わたしは猫の画像を探しました。',
        '犬と猫の画像を探したいです。',
        'lofi hip hop radio - beats to relax/study toを見せてください画像'
    ]

    for user in user_list:
        image(user)
