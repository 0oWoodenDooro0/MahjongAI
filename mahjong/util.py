from collections import Counter
from typing import Optional

from .tile import Tile


def check_is_pong(
    tiles: list[Tile], discard_tile: Tile
) -> Optional[tuple[Tile, Tile, Tile]]:
    if tiles.count(discard_tile) >= 2:
        return discard_tile, discard_tile, discard_tile
    return None


def check_is_kong(
    tiles: list[Tile], discard_tile: Tile
) -> Optional[tuple[Tile, Tile, Tile, Tile]]:
    if tiles.count(discard_tile) >= 3:
        return discard_tile, discard_tile, discard_tile, discard_tile
    return None


def check_is_closed_kong(tiles: list[Tile]) -> Optional[tuple[Tile, Tile, Tile, Tile]]:
    for i in range(34):
        if tiles.count(Tile(i)) == 4:
            return Tile(i), Tile(i), Tile(i), Tile(i)
    return None


def check_is_add_kong(decalaration: list[tuple[Tile, Tile, Tile] | tuple[Tile, Tile, Tile, Tile]], hand: list[Tile]) -> \
        Optional[list[Tile]]:
    kong_list = []
    for tiles in decalaration:
        for tile in set(hand):
            if tiles.count(tile) == 3:
                kong_list.append(tile)
    if kong_list:
        return kong_list
    return None


def check_is_chow(
    tiles: list[Tile], discard_tile: Tile
) -> Optional[list[tuple[Tile, Tile, Tile]]]:
    if discard_tile >= Tile.W1:
        return None
    first: bool = (
        (discard_tile % 9 < 7)
        and (discard_tile + 1 in tiles)
        and (discard_tile + 2 in tiles)
    )
    middle: bool = (
        (discard_tile % 9 < 8)
        and (discard_tile % 9 > 0)
        and (discard_tile + 1 in tiles)
        and (discard_tile - 1 in tiles)
    )
    last: bool = (
        (discard_tile % 9 > 1)
        and (discard_tile - 1 in tiles)
        and (discard_tile - 2 in tiles)
    )
    possibles = []
    if not any((first, middle, last)):
        return None
    if last:
        possibles.append(
            (Tile(discard_tile - 2), Tile(discard_tile - 1), Tile(discard_tile))
        )
    if middle:
        possibles.append(
            (Tile(discard_tile - 1), Tile(discard_tile), Tile(discard_tile + 1))
        )
    if first:
        possibles.append(
            (Tile(discard_tile), Tile(discard_tile + 1), Tile(discard_tile + 2))
        )

    return possibles


def check_is_win(tiles: list[Tile], discard_tile: Tile) -> bool:
    def _iswin(tiles: list[Tile]) -> bool:
        if len(tiles) == 0:
            return True

        min_tile = min(tiles)
        sub_tiles = tiles.copy()

        if tiles.count(min_tile) >= 3:
            for _ in range(3):
                sub_tiles.remove(min_tile)
            return _iswin(sub_tiles)

        if min_tile >= Tile.W1:
            return False
        elif (min_tile + 1 not in tiles) or (min_tile + 2 not in tiles):
            return False
        elif (min_tile % 9 + 1 != (min_tile + 1) % 9) or (
            min_tile % 9 + 2 != (min_tile + 2) % 9
        ):
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


def check_is_self_win(tiles: list[Tile]) -> bool:
    def _iswin(tiles: list[Tile]) -> bool:
        if len(tiles) == 0:
            return True

        min_tile = min(tiles)
        sub_tiles = tiles.copy()

        if tiles.count(min_tile) >= 3:
            for _ in range(3):
                sub_tiles.remove(min_tile)
            return _iswin(sub_tiles)

        if min_tile >= Tile.W1:
            return False
        elif (min_tile + 1 not in tiles) or (min_tile + 2 not in tiles):
            return False
        elif (min_tile % 9 + 1 != (min_tile + 1) % 9) or (min_tile % 9 + 2 != (min_tile + 2) % 9):
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

        if ((next := min_tile.next_seq_tile(1)) not in tiles) or (
            min_tile.next_seq_tile(2) not in tiles
        ):
            sub_tiles.remove(min_tile)
            if tiles.count(min_tile) == 2:
                sub_tiles.remove(min_tile)
            elif next in tiles:
                sub_tiles.remove(next)
            elif (next_2 := min_tile.next_seq_tile(2)) in tiles:
                sub_tiles.remove(next_2)
            else:
                return _count_combos_and_partners(sub_tiles)
            result = _count_combos_and_partners(sub_tiles)
            result[1] += 1
            return result

        sub_tiles.remove(min_tile)
        sub_tiles.remove(min_tile.next_seq_tile(1))
        sub_tiles.remove(min_tile.next_seq_tile(2))
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
