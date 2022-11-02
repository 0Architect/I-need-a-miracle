class Struct:
    def __init__(self, possible_val: set):
        self.value = -1
        self.possible_values = possible_val
        self.adjacent = []

    def link(self, other):
        if self not in other.adjacent and other not in self.adjacent:
            self.adjacent.append(other)
            other.adjacent.append(self)

    def update(self, value):
        self.value = value
        for other in self.adjacent:
            other.possible_values -= {value}