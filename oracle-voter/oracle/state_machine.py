class State:
    def __init__(self, name): self.name = name
    def __str__(self): return self.name


class Input:
    pass


class Condition:

    @staticmethod
    def test(input_data):
        assert 0, "Abstract Method test() not implemented"


class Transition:

    @staticmethod
    def run(oracle, input_data):
        assert 0, "Static Method run() not implemented"
