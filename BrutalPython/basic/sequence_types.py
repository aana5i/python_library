l = [1, [1, 'a'], 3]  # ordered  mutable
t = (1, [1, 'a'], 3)  # ordered  unmutable
s = {1, 'a', 3}  # unordered  unmutable

def catch_ordered():
    [print(e) for e in l]
    [print(e) for e in t]
    [print(e) for e in s]

# catch_ordered()

def catch_type_error(object, slice, operation):
    try:
        object[slice] = operation  # error
        print(object)
    except TypeError as e:
        print(e)


catch_type_error(t, 0, 100)
catch_type_error(t[1], 0, 100)

