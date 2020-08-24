import os


def hierarchy_initializer(depth):
    path = os.getcwd()
    if depth >= 1:
        for levels in range(depth):
            if levels == 0:
                level_0_path = os.path.join(path, str(levels))
                if not os.path.exists(level_0_path):
                    print(f'makedir, case 0: ', level_0_path)
                    os.makedirs(str(level_0_path))
                    f = open(f'{level_0_path}/path.txt', 'a')
                    f.write(os.path.relpath(str(level_0_path)))
                    f.close()
            else:
                subfolders = []
                for level in range(levels):
                    subfolders.extend([x[0] for x in os.walk(str(level))])
                for subfolder in subfolders[level-1:]:
                    for l in range(level+1):
                        if len(subfolder.split('\\')) == level:
                            tt_path = os.path.join(path, subfolder)  # concatenate root path and subfolder
                            tmp_path = os.path.join(tt_path, str(l))  # concatenate tmp path new folder
                            # create folder if not exist
                            if not os.path.exists(tmp_path):
                                print(f'makedir: ', tmp_path)
                                os.makedirs(tmp_path)
                                # create folders and files
                                f = open(f'{tmp_path}/path.txt', 'a')
                                f.write(os.path.relpath(str(tmp_path)))
                                f.close()
        return depth * hierarchy_initializer(depth - 1)
    else:
        return 1


for depth in range(6):
    n = hierarchy_initializer(depth+1)

