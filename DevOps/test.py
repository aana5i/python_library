import os
import argparse


class HierarchyInitializer:
    def __init__(self, depth):
        self.depth = depth

    def folder_counter(self):
        # count the number of folder who need to be created
        counter = 1
        result = []
        for num in range(self.depth+1):
            res = (num+1) * counter

            result.append(res)
            counter = res

        return sum(result)

    def hierarchy_initializer(self):
        # get root path
        path = os.getcwd()

        # count the number of folder who need to be created
        print(f'number of folder to create: {self.folder_counter()}')

        # for each step/deep
        for level in range(self.depth+1):
            # print('\n1:', 'current Level: ', level)

            # create the folder 0
            if level == 0:
                # set path for folder 0 only
                level_0_path = os.path.join(path, str(level))
                # print('1.5:', 'path0:', level_0_path)
                # create folder if not exist
                if not os.path.exists(level_0_path):
                    os.makedirs(level_0_path)
                    f = open(f'{level_0_path}/path.txt', 'a')
                    f.write(os.path.relpath(str(level_0_path)))
                    f.close()
            else:
                # print('2:', 'else')
                # find all subfolders
                subfolders = []
                for levels in range(level):
                    subfolders.extend([x[0] for x in os.walk(str(levels))])
                # print('3:', subfolders, level, subfolders[0])

                # find the current level subfolders
                for subfolder in subfolders[level-1:]:
                    # print('4:', 'sub loop')
                    # for each past level
                    for l in range(level+1):
                        # print('subfolders: ', subfolder, 'len(subfolders.split())', len(subfolder.split('\\')), 'folder', l)
                        # take only the subfolder of this level
                        if len(subfolder.split('\\')) == level:
                            tt_path = os.path.join(path, subfolder)  # concatenate root path and subfolder
                            tmp_path = os.path.join(tt_path, str(l))  # concatenate tmp path new folder
                            # print('path1: ', tmp_path)
                            # create folder if not exist
                            if not os.path.exists(tmp_path):
                                os.makedirs(tmp_path)
                                # create folders and files
                                f = open(f'{tmp_path}/path.txt', 'a')
                                f.write(os.path.relpath(str(tmp_path)))
                                f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hierarchy initializer.')
    parser.add_argument('--depth', '-d', type=int, help='Depth number')

    args = parser.parse_args()
    hi = HierarchyInitializer(args.depth)
    hi.hierarchy_initializer()
