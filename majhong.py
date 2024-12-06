from tile import Tile
from collections import Counter,defaultdict


def check_is_pong(tiles: list[Tile], discard_tile: Tile) -> bool:
    return tiles.count(discard_tile) >= 3


def check_is_kong(tiles: list[Tile], discard_tile: Tile) -> bool:
    return tiles.count(discard_tile) >= 4


def check_is_chow(tiles: list[Tile], discard_tile: Tile) -> bool:
    first: bool = (discard_tile%10 <= 7) and (discard_tile+1 in tiles) and (discard_tile+2 in tiles)
    middle: bool = (discard_tile%10 <= 8) and (discard_tile%10 >= 2) and (discard_tile+1 in tiles) and (discard_tile-1 in tiles)
    last: bool = (discard_tile%10 >= 3) and (discard_tile-1 in tiles) and (discard_tile-2 in tiles)

    return first or middle or last

def check_is_win(tiles: list[Tile], discard_tile: Tile):
    """#定理01：

    一副牌P，若把一個對子拿掉後，假設此時數字最小的牌是「x」，

    若x的張數是3張以上，則拿掉3張x（一刻）後，剩下牌為Q。
    否則拿掉x, x+1, x+2（一順）之後，剩下的牌為Q。（若無法拿，則P沒胡）

    則「P胡」若且唯若「Q胡」。
    """
    pairs : list = [i for i,_ in Counter(tiles).items() if _==2]
    for pair in pairs:
        if _iswin([i for i in tiles if i != pair]):
            return True
    return False

def _iswin(tiles: list[Tile]) -> bool:
    if tiles is None:
        return True
    min_tiles = min(tiles)
    if tiles.count(min_tiles) >= 3:
        return _iswin([i for i in tiles if i != min_tiles])
    if (min_tiles+1 not in tiles) or (min_tiles+2 not in tiles):
        return False
    return _iswin([i for i in tiles if i not in [min_tiles, min_tiles+1, min_tiles+2]])


#check_is_win([Tile.C1,Tile.C1,Tile.C2,Tile.C3,Tile.C4,Tile.C4,Tile.C4],Tile.C5)