import random

from mahjong import Game, check_is_win, check_is_closed_kong, check_is_add_kong, Tile, check_is_kong, check_is_pong, \
    check_is_chow


def draw_a_tile(game: Game):
    draw_tile = game.draw()
    if draw_tile is None:
        return
    player = game.players[game.turn]
    if check_is_win(player.hand, draw_tile):
        if random.random() < 0.5:
            game.win()
    elif add_kong_tile := check_is_add_kong(player.declaration, draw_tile):
        if random.random() < 0.5:
            game.add_kong(add_kong_tile)
    elif closed_kong_tiles := check_is_closed_kong(player.hand, draw_tile):
        if random.random() < 0.5:
            game.closed_kong(draw_tile, closed_kong_tiles)
            discard_tile = random.choice(player.hand)
            game.discard(discard_tile)
    else:
        player.add_to_hand(draw_tile)
        discard_tile = random.choice(player.hand)
        game.discard(discard_tile)
        other_player_discards_a_tile(game, discard_tile)


def other_player_discards_a_tile(game: Game, discard_tile: Tile):
    for player in game.players:
        if player.turn == game.turn:
            continue
        elif check_is_win(player.hand, discard_tile):
            if random.random() < 0.5:
                game.win()
                return
    for player in game.players:
        if player.turn == game.turn:
            continue
        elif kong_tiles := check_is_kong(player.hand, discard_tile):
            if random.random() < 0.5:
                game.turn = player.turn
                game.kong(kong_tiles)
                discard_tile = random.choice(player.hand)
                game.discard(discard_tile)
                other_player_discards_a_tile(game, discard_tile)
                return
        elif pong_tiles := check_is_pong(player.hand, discard_tile):
            if random.random() < 0.5:
                game.turn = player.turn
                game.pong(pong_tiles)
                discard_tile = random.choice(player.hand)
                game.discard(discard_tile)
                other_player_discards_a_tile(game, discard_tile)
                return
    for player in game.players:
        if player.turn == (game.turn + 1) % len(game.players):
            if chow_tiles_list := check_is_chow(player.declaration, discard_tile):
                if random.random() < 0.5:
                    game.turn = player.turn
                    chow_tiles = random.choice(chow_tiles_list)
                    game.pong(chow_tiles)
                    discard_tile = random.choice(player.hand)
                    game.discard(discard_tile)
                    other_player_discards_a_tile(game, discard_tile)
                    return
    game.turn_next()
    return


if __name__ == '__main__':
    game = Game()
    while True:
        if game.over:
            break
        draw_a_tile(game)
