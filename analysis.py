import berserk

def main(playerName: str, game_type: str, max_game: int, as_pgn: bool):
    white, black = load(playerName, game_type, max_game, as_pgn)
    white_games = []
    black_games = []
    for times in range(50):
        game_to_list(white_games, black_games, white, black)
    print("White:",white_games)
    print("")
    print("")
    print("Black:",black_games)

def load(player: str, game: str, max: int, pgn: bool):
    client = berserk.Client()
    #Generator for the games (black and white seperately)
    white = client.games.export_by_player(player, perf_type=game, max=max, color="white", as_pgn=pgn)
    black = client.games.export_by_player(player, perf_type=game, max=max, color="black", as_pgn=pgn)
    return white, black

def game_to_list(white_games, black_games, white, black):
    white_game = next(white)
    #We care about overextention, therefore moves that take are hard to evaluate as well as pawn moves that are checks
    #Therefore those are ignored, also pushing to 6th rank or further probably means either the pawn was doomed to die anyway or it is going towards queening, both of which are hard to evaluate in terms of overextension.  
    #If there is no winner, the game was a draw, the generator ignores aborted games automatically
    white_game_dict = {'winner': 'draw', 'a4': 0, 'a5': 0, 'b4': 0, 'b5': 0, 'c4': 0, 'c5': 0, 'd4': 0, 'd5': 0, 'e4': 0, 'e5': 0, 'f4': 0, 'f5': 0, 'g4': 0, 'g5': 0, 'h4': 0, 'h5': 0}
    black_game_dict = {'winner': 'draw', 'a4': 0, 'a5': 0, 'b4': 0, 'b5': 0, 'c4': 0, 'c5': 0, 'd4': 0, 'd5': 0, 'e4': 0, 'e5': 0, 'f4': 0, 'f5': 0, 'g4': 0, 'g5': 0, 'h4': 0, 'h5': 0}

    #Checks whether or not the starting position is the standard or not, ignores non-standard starting positions 
    if 'initialFen' not in white_game.keys():
        if 'winner' in white_game.keys():
            white_game_dict['winner'] = white_game['winner']
        white_games_array = white_game['moves'].split()
        for i in range(len(white_games_array)):
            #White starts, indices 0,2,4,.. are white's moves
            if i % 2 == 0 and white_games_array[i] in white_game_dict.keys():
                white_game_dict[white_games_array[i]] = 1
        white_games.append(white_game_dict)

    black_game = next(black)
    if 'initialFen' not in black_game.keys():
        if 'winner' in black_game.keys():
            black_game_dict['winner'] = black_game['winner']
        black_games_array = black_game['moves'].split()
        for i in range(len(black_games_array)):
            if i % 2 != 0 and black_games_array[i] in black_game_dict.keys():
                black_game_dict[black_games_array[i]] = 1
        black_games.append(black_game_dict)


if __name__ == "__main__":
    main('C9C9C9C9C9', 'blitz', 1000, False)