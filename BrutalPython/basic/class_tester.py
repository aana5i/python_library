from class_train import Person


def person_tester(_age, _gender):
    risa = Person('Risa', _age, 'lady', 'osaka kitaku kyuuhouji')
    # print(risa.age)
    assert risa.age == _age, f'actual: {risa.age} excepted: {_age}'
    assert risa.gender == _gender, f'actual: {risa.gender} excepted: {_gender}'
    # print(risa.gender)
    # print(risa.address)
    # alfe = Person('Alfe', 19, 'boy', 'wakayama momoyamacyou')
    # print(alfe.age)
    # print(alfe.gender)
    # print(alfe.address)

# for i in range(20, 25):
#     try:
#         person_tester(22, i, 'Risachan')
#     except AssertionError as a:
#         print(a)

person_tester(22, 'Risachan')