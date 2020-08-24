import os


def hierarchy_initializer(depth):
    # assuming that n is a positive integer or 0
    if depth >= 1:
        if not os.path.exists(depth):
            os.makedirs(str(depth))
            f = open(f'{str(depth)}/path.txt', 'a')
            f.write(os.path.relpath(str(depth)))
            f.close()
        return depth * hierarchy_initializer(depth - 1)
    else:
        return 1


for depth in range(5):
    print(f'{depth}! =', hierarchy_initializer(depth+1) // (hierarchy_initializer(depth+1) // (depth+1)) if depth > 0 else 1)

