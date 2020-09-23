# -*- coding: utf-8 -*-

import os


def create_folder(path):
    """
    フォルダー・ファイルを作成する
    :param path: str
    :return: str
    """
    # パスがすでに存在するかどうかを確認 // check if path already exist
    if not os.path.exists(path):
        # フォルダーを作る // create folder
        os.makedirs(path)
        # ファイルを作成する // create file
        f = open(f'{path}/path.txt', 'a')
        f.write(os.path.relpath(path))
        f.close()

    return path


def hierarchy_initializer(depth):
    """
    フォルダー・ファイル階層を作る (かいそう)  // create the folder/file hierarchy
    :param depth: int
    :return: int
    """
    # ルートパスを保持する (ほじ)  // get the root pass
    path = os.getcwd()
    # 過去のレベルパスリストを作成 (かこ) // create the past level path list
    _path = []

    # レベルのリスト（int）に深度数を変換する (しんど すう へんかん) // convert depth number to a list (int) of levels
    for level in range(depth+1):

        # 最初のレベルのみ // for first level only
        if level == 0:
            # パスを取得 (しゅとく) // build path
            level_0_path = os.path.join(path, str(level))
            # フォルダー・ファイルを作成する と 現在のすべてのレベルパスを保存する // create folder/file and save the current level path
            _path = [create_folder(str(level_0_path))]
            # save the current level path in the path list
        else:
            # 現在のすべてのレベルパスを保存する // create a temporary list to save all the current level paths
            _tmp_path = []
            # サブフォルダを取得 (しゅとく) // loop on subfolder  **  only get the current level subfolder
            for subfolder in _path:
                # このレベルの各フォルダ // for each folder in this level
                for current_level in range(level+1):
                    # パスを取得 (しゅとく) // build path
                    tmp_path = os.path.join(path, subfolder)
                    level_path = os.path.join(tmp_path, str(current_level))
                    # フォルダー・ファイルを作成する と 現在のすべてのレベルパスを保存する  // create folder/file and save the current level path
                    _tmp_path.append(create_folder(str(level_path)))

            # 現在のレベルのパスを保存する // save the last level paths
            _path = _tmp_path


hierarchy_initializer(4)
