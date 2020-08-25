# -*- coding: utf-8 -*-

import os


def create_folder(path):
    """
    フォルダー・ファイルを作成する
    :param path: str
    """
    # パスがすでに存在するかどうかを確認 // check if path already exist
    if not os.path.exists(path):
        # フォルダーを作る // create folder
        os.makedirs(path)
        # ファイルを作成する // create file
        f = open(f'{path}/path.txt', 'a')
        f.write(os.path.relpath(path))
        f.close()


def hierarchy_initializer(depth):
    """
    フォルダー・ファイル階層を作る (かいそう)  // create the folder/file hierarchy
    :param depth: int
    :return: int
    """
    # ルートパスを保持する (ほじ)  // get the root pass
    path = os.getcwd()

    # レベルのリスト（int）に深度数を変換する (しんど すう へんかん) // convert depth number to a list (int) of levels
    for level in range(depth+1):

        # 最初のレベルのみ // for first level only
        if level == 0:
            # パスを取得 (しゅとく) // build path
            level_0_path = os.path.join(path, str(level))
            # フォルダー・ファイルを作成する // create folder/file
            create_folder(str(level_0_path))
        else:
            # サブフォルダを取得 (しゅとく) // loop on subfolder  **
            for subfolder in [x[0] for x in os.walk(str(0))]:
                # only get the current level subfolder **
                if len(subfolder.split('\\')) == level:
                    # for each folder in this level **
                    for current_level in range(level+1):
                        # パスを取得 (しゅとく) // build path
                        tmp_path = os.path.join(path, subfolder)
                        level_path = os.path.join(tmp_path, str(current_level))
                        # フォルダー・ファイルを作成する // create folder/file
                        create_folder(str(level_path))


hierarchy_initializer(5)
