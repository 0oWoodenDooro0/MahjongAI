from enum import IntEnum


class Tile(IntEnum):
    C1 = 0  # 萬 1-9
    C2 = 1
    C3 = 2
    C4 = 3
    C5 = 4
    C6 = 5
    C7 = 6
    C8 = 7
    C9 = 8
    D1 = 9  # 筒 1-9
    D2 = 10
    D3 = 11
    D4 = 12
    D5 = 13
    D6 = 14
    D7 = 15
    D8 = 16
    D9 = 17
    B1 = 18  # 條 1-9
    B2 = 19
    B3 = 20
    B4 = 21
    B5 = 22
    B6 = 23
    B7 = 24
    B8 = 25
    B9 = 26
    W1 = 27  # 風 東南西北
    W2 = 28
    W3 = 29
    W4 = 30
    Dragon1 = 31  # 箭 白發中
    Dragon2 = 32
    Dragon3 = 33

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)
