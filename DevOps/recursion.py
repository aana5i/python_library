import os
import argparse


class HierarchyInitializerRecursive:
    def __init__(self, depth):
        self.depth = depth
        self.hierarchy_initializer(self.depth)

    @staticmethod
    def create_folder(path):
        """
        create folder from path if not exist
        :param path: str
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

    def hierarchy_initializer(self, depth):
        """
        Create a folder/file hierarchy
        :param depth: int
        :return:
        """
        # get the root path
        path = os.getcwd()

        # recursive  // remove the 0 value
        if depほじth >= 1:
            # for each step/deep
            for level in range(depth+1):
                # create the folder 0
                if level == 0:
                    level_0_path = os.path.join(path, str(level))  # define path for folder 0 only
                    self.create_folder(str(level_0_path))  # create folder if not exist
                else:
                    # find the past level subfolder
                    for subfolder in [x[0] for x in os.walk(str(0))]:
                        # take only the subfolder of this level
                        if len(subfolder.split('\\')) == level:
                            # for each past level
                            for current_level in range(level+1):
                                print(current_level, level, depth)
                                tmp_path = os.path.join(path, subfolder)  # concatenate root path and subfolder
                                level_path = os.path.join(tmp_path, str(current_level))  # then with new folder
                                print(level_path)
                                self.create_folder(str(level_path))  # create folder if not exist

            # return the number of folder to create on the next level
            return depth * self.hierarchy_initializer(depth - 1)
        else:
            return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hierarchy initializer.')
    parser.add_argument('--depth', '-d', type=int, help='Depth number', required=True)

    args = parser.parse_args()

    hi = HierarchyInitializerRecursive(args.depth)

    # count the number of folder who need to be created
    print(f'{hi.folder_counter()} folder created')
