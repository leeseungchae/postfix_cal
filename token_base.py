class Base:
    def __init__(self, value):
        self.value = value


    def __repr__(self):
        return self.value


class Operator(Base):
    def __init__(self, value):
        super().__init__(value)

    @classmethod
    def is_valid(cls, value):
        return value in "+-*/"

    @classmethod
    def priority(cls, value):

        priority = {'+': 2, '-': 2, '*': 3, '/': 3,}
        return priority[str(value)]


class Operand(Base):
    def __init__(self, value):
        super().__init__(value)

    def __add__(self, other):
        return Operand(float(self.value) + float(other.value))

    def __sub__(self, other):
        return Operand(float(self.value) - float(other.value))

    def __mul__(self, other):
        return Operand(float(self.value) * float(other.value))

    def __truediv__(self, other):
        return Operand(float(self.value) / float(other.value))

    @classmethod
    def is_valid(cls, value):
        try :
            check = isinstance(float(value), float)
            return check
        except :
            return False

