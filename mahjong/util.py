from collections import Counter

from .tile import Tile

def check_is_pong(tiles: list[Tile], discard_tile: Tile) -> bool:
    if tiles.count(discard_tile) >= 2: return [discard_tile, discard_tile, discard_tile]
    return None

def check_is_kong(tiles: list[Tile], discard_tile: Tile) -> bool:
    if tiles.count(discard_tile) >= 3: return [discard_tile, discard_tile, discard_tile, discard_tile]
    return None


def check_is_chow(tiles: list[Tile], discard_tile: Tile) -> bool:
    first: bool = (
            (discard_tile % 10 <= 7)
            and (discard_tile + 1 in tiles)
            and (discard_tile + 2 in tiles)
    )
    middle: bool = (
            (discard_tile % 10 <= 8)
            and (discard_tile % 10 >= 2)
            and (discard_tile + 1 in tiles)
            and (discard_tile - 1 in tiles)
    )
    last: bool = (
            (discard_tile % 10 >= 3)
            and (discard_tile - 1 in tiles)
            and (discard_tile - 2 in tiles)
    )

    if first: return [discard_tile, discard_tile + 1, discard_tile + 2]
    elif middle: return [discard_tile - 1, discard_tile, discard_tile + 1]
    else: return [discard_tile - 2, discard_tile - 1, discard_tile]
        
    return None


def check_is_win(tiles: list[Tile], discard_tile: Tile):
    def _iswin(tiles: list[Tile]) -> bool:
        if len(tiles) == 0:
            return True

        min_tile = min(tiles)
        sub_tiles = tiles.copy()

        if tiles.count(min_tile) >= 3:
            for _ in range(3):
                sub_tiles.remove(min_tile)
            return _iswin(sub_tiles)

        if (min_tile + 1 not in tiles) or (min_tile + 2 not in tiles):
            return False

        sub_tiles = tiles.copy()
        for i in range(3):
            sub_tiles.remove(min_tile + i)

        return _iswin(sub_tiles)

    # ---------------------------------------------------------
    """#定理01：

    一副牌P，若把一個對子拿掉後，假設此時數字最小的牌是「x」，

    若x的張數是3張以上，則拿掉3張x（一刻）後，剩下牌為Q。
    否則拿掉x, x+1, x+2（一順）之後，剩下的牌為Q。（若無法拿，則P沒胡）

    則「P胡」若且唯若「Q胡」。
    """

    copied_tiles = tiles.copy()
    copied_tiles.append(discard_tile)

    pairs: list = [i for i, c in Counter(copied_tiles).items() if c >= 2]
    for pair in pairs:
        sub_tiles = copied_tiles.copy()
        sub_tiles.remove(pair)
        sub_tiles.remove(pair)
        if _iswin(sub_tiles):
            return True
    return False


def check_listen(hand_tiles: list[Tile]) -> int:
    def _count_combos_and_partners(tiles: list[Tile]) -> list[int]:
        if len(tiles) == 0:
            return [0, 0]

        result: list[int]  # return (面子，搭子)
        min_tile = min(tiles)
        sub_tiles = tiles.copy()

        if tiles.count(min_tile) >= 3:
            for _ in range(3):
                sub_tiles.remove(min_tile)
            result = _count_combos_and_partners(sub_tiles)
            result[0] += 1
            return result

        if (min_tile + 1 not in tiles) or (min_tile + 2 not in tiles):
            sub_tiles.remove(min_tile)
            if tiles.count(min_tile) == 2:
                sub_tiles.remove(min_tile)
            elif min_tile + 1 in tiles:
                sub_tiles.remove(min_tile + 1)
            elif (min_tile + 2 in tiles) and (min_tile % 10 < 9):
                sub_tiles.remove(min_tile + 2)
            else:
                return _count_combos_and_partners(sub_tiles)
            result = _count_combos_and_partners(sub_tiles)
            result[1] += 1
            return result

        for i in range(3):
            sub_tiles.remove(min_tile + i)
        result = _count_combos_and_partners(sub_tiles)
        result[0] += 1
        return result

    # ---------------------------------------------------------
    # reference from https://www.bilibili.com/opus/563332111030452322

    copied_tiles = hand_tiles.copy()
    pairs: list = [i for i, c in Counter(copied_tiles).items() if c >= 2]
    has_pair: bool = len(pairs) > 0

    result: list[int] = _count_combos_and_partners(hand_tiles)
    combos: int = result[0]
    partners: int = result[1]

    if combos + partners <= 6:
        return 10 - 2 * combos - partners
    else:
        return 5 - combos - has_pair

# if __name__ == "__main__":
# pass