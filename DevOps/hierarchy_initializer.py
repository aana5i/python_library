import os


def hierarchy_initializer(depth):
    # get root path
    path = os.getcwd()

    # for each step/deep
    for level in range(depth+1):
        print('\n1:', 'current Level: ', level)

        # create the folder 0
        if level == 0:
            # set path for folder 0 only
            level_0_path = os.path.join(path, str(level))
            print('1.5:', 'path0:', level_0_path)
            # create folder if not exist
            if not os.path.exists(level_0_path):
                os.makedirs(level_0_path)
                f = open(f'{level_0_path}/path.txt', 'a')
                f.write(os.path.relpath(str(level_0_path)))
                f.close()
        else:
            print('2:', 'else')
            # find all subfolders
            subfolders = []
            for levels in range(level):
                subfolders.extend([x[0] for x in os.walk(str(levels))])
            print('3:', subfolders, level, subfolders[0])

            # find the current level subfolders
            for subfolder in subfolders[level-1:]:
                print('4:', 'sub loop')
                # for each past level
                for l in range(level+1):
                    # print('subfolders: ', subfolder, 'len(subfolders.split())', len(subfolder.split('\\')), 'folder', l)
                    # take only the subfolder of this level
                    if len(subfolder.split('\\')) == level:
                        tt_path = os.path.join(path, subfolder)  # concatenate root path and subfolder
                        tmp_path = os.path.join(tt_path, str(l))  # concatenate tmp path new folder
                        print('path1: ', tmp_path)
                        # create folder if not exist
                        if not os.path.exists(tmp_path):
                            os.makedirs(tmp_path)
                            # create folders and files
                            f = open(f'{tmp_path}/path.txt', 'a')
                            f.write(os.path.relpath(str(tmp_path)))
                            f.close()


hierarchy_initializer(3)
