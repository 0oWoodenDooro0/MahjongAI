from collections import Counter
from typing import Optional, List

from .declaration import Declaration
from .hand import Hand
from .meld import Meld, SequenceMeld, TripletMeld, QuadrupletMeld
from .tile import Tile


class Player:
    def __init__(self, turn: int):
        self.turn: int = turn
        self.hand: Hand = Hand()
        self.declaration: Declaration = Declaration()

    def draw(self, tile: Tile):
        self.hand.draw(tile)

    def discard(self, tile: Tile):
        if tile not in self.hand:
            raise ValueError("tile not in hand")
        self.hand.discard(tile)

    def add_to_declaration(self, meld: Meld):
        for tile in meld:
            self.discard(tile)
        self.declaration.call(meld)

    def chow(self, chow_tiles: SequenceMeld, discard_tile: Tile):
        self.hand.draw(discard_tile)
        self.add_to_declaration(chow_tiles)

    def pong(self, pong_tiles: TripletMeld, discard_tile: Tile):
        self.hand.draw(discard_tile)
        self.add_to_declaration(pong_tiles)

    def kong(self, kong_tiles: QuadrupletMeld, discard_tile: Tile):
        self.hand.draw(discard_tile)
        self.add_to_declaration(kong_tiles)

    def closed_kong(self, closed_kong_tiles: QuadrupletMeld):
        self.add_to_declaration(closed_kong_tiles)

    def add_kong(self, add_kong_tile: Tile):
        self.discard(add_kong_tile)
        self.declaration.add_kong(add_kong_tile)

    def can_chow(self, discard_tile: Tile) -> Optional[List[SequenceMeld]]:
        if discard_tile >= Tile.W1:
            return None
        first: bool = (
                (discard_tile % 9 < 7)
                and (discard_tile + 1 in self.hand)
                and (discard_tile + 2 in self.hand)
        )
        middle: bool = (
                (discard_tile % 9 < 8)
                and (discard_tile % 9 > 0)
                and (discard_tile + 1 in self.hand)
                and (discard_tile - 1 in self.hand)
        )
        last: bool = (
                (discard_tile % 9 > 1)
                and (discard_tile - 1 in self.hand)
                and (discard_tile - 2 in self.hand)
        )
        possibles = []
        if not any((first, middle, last)):
            return None
        if last:
            possibles.append(SequenceMeld((Tile(discard_tile - 2), Tile(discard_tile - 1), Tile(discard_tile))))
        if middle:
            possibles.append(SequenceMeld((Tile(discard_tile - 1), Tile(discard_tile), Tile(discard_tile + 1))))
        if first:
            possibles.append(SequenceMeld((Tile(discard_tile), Tile(discard_tile + 1), Tile(discard_tile + 2))))

        return possibles

    def can_pong(self, discard_tile: Tile) -> Optional[TripletMeld]:
        if self.hand.count(discard_tile) >= 2:
            return TripletMeld((discard_tile, discard_tile, discard_tile))
        return None

    def can_kong(self, discard_tile: Tile) -> Optional[QuadrupletMeld]:
        if self.hand.count(discard_tile) >= 3:
            return QuadrupletMeld((discard_tile, discard_tile, discard_tile, discard_tile))
        return None

    def can_closed_kong(self) -> Optional[QuadrupletMeld]:
        for i in range(34):
            kong_tile = Tile(i)
            if self.hand.count(kong_tile) == 4:
                return QuadrupletMeld((kong_tile, kong_tile, kong_tile, kong_tile))
        return None

    def can_add_kong(self) -> Optional[List[QuadrupletMeld]]:
        kong_list = []
        for meld in self.declaration:
            if isinstance(meld, TripletMeld):
                tile = meld.tiles[0]
                if tile in set(self.hand):
                    kong_list.append(QuadrupletMeld((tile, tile, tile, tile)))
        if kong_list:
            return kong_list
        return None

    def can_win(self, discard_tile: Tile) -> bool:
        tiles = self.hand.tiles.copy()
        tiles.append(discard_tile)
        return self.check_is_win(tiles)

    def can_self_win(self) -> bool:
        return self.check_is_win(self.hand.tiles)

    @staticmethod
    def check_is_win(tiles: List[Tile]) -> bool:
        def _iswin(tiles: List[Tile]) -> bool:
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

        pairs: List = [i for i, c in Counter(tiles).items() if c >= 2]
        for pair in pairs:
            sub_tiles = tiles.copy()
            sub_tiles.remove(pair)
            sub_tiles.remove(pair)
            if _iswin(sub_tiles):
                return True
        return False

    def __str__(self):
        return f"Player {self.turn}"
