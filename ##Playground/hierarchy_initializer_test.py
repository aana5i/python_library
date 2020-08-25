import os


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        # create folders and files
        f = open(f'{path}/path.txt', 'a')
        f.write(os.path.relpath(path))
        f.close()


def hierarchy_initializer(depth):
    path = os.getcwd()
    for level in range(depth+1):
        if level == 0:
            level_0_path = os.path.join(path, str(level))
            create_folder(str(level_0_path))
        else:
            for subfolder in [x[0] for x in os.walk(str(0))]:
                if len(subfolder.split('\\')) == level:
                    for current_level in range(level+1):
                        tmp_path = os.path.join(path, subfolder)
                        level_path = os.path.join(tmp_path, str(current_level))
                        create_folder(str(level_path))


hierarchy_initializer(3)
