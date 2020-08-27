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
        save the current level path in the path list
        :param path:
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)
            # create folders and files
            f = open(f'{path}/path.txt', 'a')
            f.write(os.path.relpath(path))
            f.close()
        return path

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

        # create the past level path list
        _path = []

        # for each step/deep
        for level in range(self.depth+1):

            # create the folder 0
            if level == 0:
                # set path for folder 0 only
                level_0_path = os.path.join(path, str(level))
                # create folder if not exist, save the current level path in the path list
                _path = [self.create_folder(str(level_0_path))]

            else:
                # create a temporary to save all the current level paths
                _tmp_path = []
                # find the past level subfolder, take only the subfolder of this level
                for subfolder in _path:
                    # for each past level
                    for current_level in range(level+1):
                        tmp_path = os.path.join(path, subfolder)  # concatenate root path and subfolder
                        level_path = os.path.join(tmp_path, str(current_level))  # # then with new folder
                        # create folder if not exist, save the current level path
                        _tmp_path.append(self.create_folder(str(level_path)))
                # create a new path list the last level path
                _path = _tmp_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hierarchy initializer.')
    parser.add_argument('--depth', '-d', type=int, help='Depth number', required=True)

    args = parser.parse_args()
    hi = HierarchyInitializer(args.depth)

    # count the number of folder who need to be created
    print(f'Total: {hi.folder_counter()} folder created')
