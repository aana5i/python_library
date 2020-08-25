import os
import argparse


class HierarchyInitializer:
    def __init__(self, depth):
        self.depth = depth
        self.hierarchy_initializer()

    @staticmethod
    def create_folder(path):
        """
        create folder from path if not exist
        :param path:
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)
            # create folders and files
            f = open(f'{path}/path.txt', 'a')
            f.write(os.path.relpath(path))
            f.close()

    def folder_counter(self):
        """
        count the number of folder to create
        :return:
        """
        counter = 1
        result = []
        for num in range(self.depth+1):
            res = (num+1) * counter

            result.append(res)
            counter = res

        return sum(result)

    def hierarchy_initializer(self):
        """
        Create a folder/file hierarchy
        :return:
        """
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
                self.create_folder(str(level_0_path))

            else:
                # print('2:', 'else')
                # find the past level subfolder
                for subfolder in [x[0] for x in os.walk(str(0))]:
                    # print('4:', 'sub loop')
                    # take only the subfolder of this level
                    if len(subfolder.split('\\')) == level:
                        # for each past level
                        for current_level in range(level+1):
                            print(current_level)
                            # print('subfolders: ', subfolder, 'len(subfolders.split())', len(subfolder.split('\\')), 'folder', l)
                            tmp_path = os.path.join(path, subfolder)  # concatenate root path and subfolder
                            level_path = os.path.join(tmp_path, str(current_level))  # # then with new folder
                            print(level_path)
                            # print('path1: ', tmp_path)
                            # create folder if not exist
                            self.create_folder(str(level_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hierarchy initializer.')
    parser.add_argument('--depth', '-d', type=int, help='Depth number', required=True)

    args = parser.parse_args()
    hi = HierarchyInitializer(args.depth)
