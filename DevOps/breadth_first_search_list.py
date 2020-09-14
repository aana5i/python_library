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
        root_path = os.getcwd()

        # create the past level path list
        past_level_path = []

        # for each step/deep
        for level in range(self.depth+1):

            # create the folder 0
            if level == 0:
                # set path for folder 0 only
                level_0_path = os.path.join(root_path, str(level))
                # create folder if not exist, save the current level path in the path list
                past_level_path = [self.create_folder(str(level_0_path))]

            else:
                # create a temporary to save all the current level paths
                current_level_path = []
                # find the past level subfolder, take only the subfolder of this level
                for subfolder in past_level_path:
                    # concatenate root path and subfolder
                    current_subfolder_path = os.path.join(root_path, subfolder)
                    # for each past level
                    for current_level in range(level+1):
                        # concatenate subfolder and current level new folder
                        level_path = os.path.join(current_subfolder_path, str(current_level))
                        # create folder if not exist, save the current level path
                        current_level_path.append(self.create_folder(str(level_path)))
                # create a new path list the last level path
                past_level_path = current_level_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hierarchy initializer.')
    parser.add_argument('--depth', '-d', type=int, help='Depth number', required=True)

    args = parser.parse_args()
    hi = HierarchyInitializer(args.depth)

    # count the number of folder who need to be created
    print(f'Total: {hi.folder_counter()} folder created')
