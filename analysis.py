import berserk
import pandas as pd
import numpy as np
from sklearn import linear_model, model_selection, feature_selection

def main(playerName: str, game_type: str, max_game: int, as_pgn: bool):
    white, black = load(playerName, game_type, max_game, as_pgn)
    white_games = []
    black_games = []
    print(white)
    print(black)
    for times in range(300):
        game_to_list(white_games, black_games, white, black)
    # print("White:",white_games)
    # print("")
    # print("")
    # print("Black:",black_games)
    df_white = pd.DataFrame(white_games)
    df_black = pd.DataFrame(black_games)
    print(df_white)
    print(df_black)
    white_ana = analyse(df_white) 
    black_ana = analyse(df_black)
    print(white_ana)
    print(black_ana)
    p_white = analyse2(df_white).sort_values(by="P")
    p_black = analyse2(df_black).sort_values(by="P")
    print(p_white)
    print(p_black)
    p_white.to_json('pos.json', orient = 'split', compression = 'infer')
    p_black.to_json('neg.json', orient = 'split', compression = 'infer')
    with open('reg.txt', 'w') as f:
        f.write(str(white_ana))
        f.write('\n')
        f.write(str(black_ana))
    

def analyse2(df):
    p = pd.DataFrame()
    p["Moves"] = list(df.columns)[1:]
    p["P"] = feature_selection.f_regression(df[list(df.columns)[1:]], df.winner)[1]
    return p

def analyse(df):
    X_train, X_test, y_train, y_test = model_selection.train_test_split(df.drop(['winner'], axis=1), df.winner)

    reg_views = linear_model.LogisticRegression().fit(X_train, y_train)
    return reg_views.score(X_test, y_test)


def load(player: str, game: str, max: int, pgn: bool):
    session = berserk.TokenSession('lip_IcEC8JTT9lYcvdCWspNh')
    client = berserk.Client(session=session)
    #Generator for the games (black and white seperately)
    white = client.games.export_by_player(player, perf_type=game, max=max, color="white", as_pgn=pgn)
    black = client.games.export_by_player(player, perf_type=game, max=max, color="black", as_pgn=pgn)
    return white, black

def game_to_list(white_games, black_games, white, black):
    white_game = next(white)
    #We care about overextention, therefore moves that take are hard to evaluate as well as pawn moves that are checks
    #Therefore those are ignored, also pushing to 6th rank or further probably means either the pawn was doomed to die anyway or it is going towards queening, both of which are hard to evaluate in terms of overextension.  
    #If there is no winner, the game was a draw, the generator ignores aborted games automatically, here draw=0.5, loss=1, and win=0
    # white_game_dict = {'winner': 0.5, 'a4': False, 'a5': False, 'b4': False, 'b5': False, 'c4': False, 'c5': False, 'd4': False, 'd5': False, 'e4': False, 'e5': False, 'f4': False, 'f5': False, 'g4': False, 'g5': False, 'h4': False, 'h5': False}
    #black_game_dict = {'winner': 'draw', 'a4': 0, 'a5': 0, 'b4': 0, 'b5': 0, 'c4': 0, 'c5': 0, 'd4': 0, 'd5': 0, 'e4': 0, 'e5': 0, 'f4': 0, 'f5': 0, 'g4': 0, 'g5': 0, 'h4': 0, 'h5': 0}
    white_game_dict = {'winner': 0.5, 'a4': 0, 'a5': 0, 'a6': 0, 'b4': 0, 'b5': 0, 'b6': 0, 'c4': 0, 'c5': 0, 'c6': 0, 'd4': 0, 'd5': 0, 'd6': 0, 'e4': 0, 'e5': 0, 'e6': 0, 'f4': 0, 'f5': 0, 'f6': 0, 'g4': 0, 'g5': 0, 'g6': 0, 'h4': 0, 'h5': 0, 'h6': 0}
    # black_game_dict = {'winner': 0.5, 'a4': False, 'a5': False, 'b4': False, 'b5': False, 'c4': False, 'c5': False, 'd4': False, 'd5': False, 'e4': False, 'e5': False, 'f4': False, 'f5': False, 'g4': False, 'g5': False, 'h4': False, 'h5': False}
    black_game_dict = {'winner': 0.5, 'a3': 0, 'a4': 0, 'a5': 0, 'b3': 0, 'b4': 0, 'b5': 0, 'c3': 0, 'c4': 0, 'c5': 0, 'd3': 0, 'd4': 0, 'd5': 0, 'e3': 0, 'e4': 0, 'e5': 0, 'f3': 0, 'f4': 0, 'f5': 0, 'g3': 0, 'g4': 0, 'g5': 0, 'h3': 0, 'h4': 0, 'h5': 0}
    #Checks whether or not the starting position is the standard or not, ignores non-standard starting positions 
    if 'initialFen' not in white_game.keys():
        if 'winner' in white_game.keys():
            win = white_game['winner']
            if win == 'white':
                win = 1
            else:
                win = 0
            white_game_dict['winner'] = win
        white_games_array = white_game['moves'].split()
        for i in range(len(white_games_array)):
            #White starts, indices 0,2,4,.. are white's moves
            if i % 2 == 0 and white_games_array[i] in white_game_dict.keys():
                white_game_dict[white_games_array[i]] = 1
        if white_game_dict['winner'] != 0.5:
            white_games.append(white_game_dict)

    black_game = next(black)
    if 'initialFen' not in black_game.keys():
        if 'winner' in black_game.keys():
            win = black_game['winner']
            if win == 'black':
                win = 1
            else:
                win = 0
            black_game_dict['winner'] = win
        black_games_array = black_game['moves'].split()
        for i in range(len(black_games_array)):
            if i % 2 != 0 and black_games_array[i] in black_game_dict.keys():
                black_game_dict[black_games_array[i]] = 1
        if black_game_dict['winner'] != 0.5:
            black_games.append(black_game_dict)


if __name__ == "__main__":
    main('C9C9C9C9C9', 'blitz', 1000, False)