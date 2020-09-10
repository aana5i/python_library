class Person:
    def __init__(self, name, age, gender, address):
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        if age <= 18:
            raise ValueError('value2 must be greater than 18')
        else:
            self._age = age

    @property
    def gender(self):
        return self.name + self._gender

    @gender.setter
    def gender(self, gender):
        _gender = {
            'kun': ['boy', 'men', 'man'],
            'chan': ['girl', 'lady']
        }

        self._gender = [k for k, v in _gender.items() if gender in v][0]

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        keys = ['city', 'ward', 'street', 'number']
        values = address.split()

        [values.append('') for _ in range(len(keys) - len(values))]

        _address = dict(zip(keys, values))

        self._address = _address

# EXECUTION
# risa = Person('Risa', 22, 'lady', 'osaka kitaku kyuuhouji')
# print(risa.age)
# print(risa.gender)
# print(risa.address)
# alfe = Person('Alfe', 19, 'boy', 'wakayama momoyamacyou')
# print(alfe.age)
# print(alfe.gender)
# print(alfe.address)

