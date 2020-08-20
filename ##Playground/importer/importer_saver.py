import pickle


# loader
def from_text(path, mode='r', encoding='utf-8'):
    _encoding = ['utf-8', 'shift_jis']
    with open(path, mode=mode, encoding=[_encoding[encoding] if isinstance(encoding, int) else encoding][0]) as f:
        result = f.read()  # str
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


# saver
def to_pickle(path, filename, mode='wb'):
    with open(path, mode=mode) as f:
        pickle.dump(filename, f)



