import pickle


# LOADER
def from_text(path, mode='r', encoding='utf-8'):
    """
    get all line from a text file
    :param path: str
    :param mode: str
    :param encoding: str
    :return: list
    """
    _encoding = ['utf-8', 'shift_jis']
    with open(path, mode=mode, encoding=[_encoding[encoding] if isinstance(encoding, int) else encoding][0]) as f:
        result = f.read()
        f.close()
    return result


def from_pickle(path, mode='rb'):
    with open(path, mode=mode) as f:
        result = []
        while 1:
            try:
                result.append(pickle.load(f))
            except EOFError:
                break

    return result


# SAVER
def to_pickle(path, filename, mode='wb'):
    with open(path, mode=mode) as f:
        pickle.dump(filename, f)


def to_text(path, data, mode='a', encoding='utf-8'):
    """
    write one line in a text file
    :param path: str
    :param data: str
    :param mode: str
    :param encoding: str
    """
    _encoding = ['utf-8', 'shift_jis']
    with open(path, mode, encoding=[_encoding[encoding] if isinstance(encoding, int) else encoding][0]) as f:
        f.write(f'{data}\r')
        f.close()

