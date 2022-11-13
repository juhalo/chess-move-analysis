import berserk

def main(playerName: str, game_type: str, max_game: int, as_pgn: bool):
    white, black = load(playerName, game_type, max_game, as_pgn)
    white_games = []
    black_games = []
    for i in range(2):
        game_to_list(white_games, black_games, white, black)
    print("White:",white_games)
    print("Black:",black_games)

def load(player: str, game: str, max: int, pgn: bool):
    client = berserk.Client()
    #Generator for the games (black and white seperately)
    white = client.games.export_by_player(player, perf_type=game, max=max, color="white", as_pgn=pgn)
    black = client.games.export_by_player(player, perf_type=game, max=max, color="black", as_pgn=pgn)
    return white, black

def game_to_list(white_games, black_games, white, black):
    white_game = next(white)
    white_game_dict = {}
    #If there is no winner, the game was a draw
    if 'winner' in white_game.keys():
        white_game_dict['winner'] = white_game['winner']
    else:
        white_game_dict['winner'] = 'draw'
    white_game_dict['moves'] = white_game['moves']
    white_games.append(white_game_dict)
    black_game = next(black)
    black_game_dict = {}
    if 'winner' in black_game.keys():
        black_game_dict['winner'] = black_game['winner']
    else:
        black_game_dict['winner'] = 'draw'
    black_game_dict['moves'] = black_game['moves']
    black_games.append(black_game_dict)


if __name__ == "__main__":
    main('C9C9C9C9C9', 'blitz', 1000, False)