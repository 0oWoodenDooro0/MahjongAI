from enum import IntEnum


class Tile(IntEnum):
    C1 = 1  # 萬 1-9
    C2 = 2
    C3 = 3
    C4 = 4
    C5 = 5
    C6 = 6
    C7 = 7
    C8 = 8
    C9 = 9
    D1 = 11  # 筒 1-9
    D2 = 12
    D3 = 13
    D4 = 14
    D5 = 15
    D6 = 16
    D7 = 17
    D8 = 18
    D9 = 19
    B1 = 21  # 條 1-9
    B2 = 22
    B3 = 23
    B4 = 24
    B5 = 25
    B6 = 26
    B7 = 27
    B8 = 28
    B9 = 29
    W1 = 100  # 風 東南西北
    W2 = 110
    W3 = 120
    W4 = 130
    Dragon1 = 200  # 箭 中發白
    Dragon2 = 210
    Dragon3 = 220

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)
