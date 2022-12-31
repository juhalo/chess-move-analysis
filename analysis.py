import berserk
import pandas as pd
import numpy as np
from sklearn import linear_model, model_selection, feature_selection
import time
import statsmodels.formula.api as smf
import statsmodels.api as sm
from sklearn.metrics import accuracy_score

# player_name: username on lichess.org
# game_type: specifies the game type, e.g. 'blitz', 'bullet'
# max_games: defines how many games the generator uses
# as_pgn: defines in which format the games are streamed
# sm_or_not: defined the function used to in the analysis, if 'False', then uses smf (see above)  
def main(player_name: str, game_type: str, max_game: int, as_pgn: bool, sm_or_not: bool):
    white, black = load(player_name, game_type, max_game, as_pgn)
    white_games = []
    black_games = []
    #White and black are done seperately due to reducing the requests
    for _ in range(max_game):
        try:
            game_to_list(white_games, black_games, white, black, True)
        except StopIteration:
            break
    #Sleep helps at not doing too many queries too quickly, would result in error otherwise
    time.sleep(60)
    for _ in range(max_game):
        try:
            game_to_list(white_games, black_games, white, black, False)
        except StopIteration:
            break
    df_white = pd.DataFrame(white_games)
    df_black = pd.DataFrame(black_games)
    for col in df_white.columns:
        df_white[col] = df_white[col].astype('category').cat.codes
    for col in df_black.columns:
        df_black[col] = df_black[col].astype('category').cat.codes
    # Removing the below might make for better results:
    # letters = 'abcdefgh'
    # for letter in letters:
    #     df_white = df_white.drop([letter+"4"], axis=1)
    #     df_black = df_black.drop([letter+"5"], axis=1)
    df_white_loss = df_white[df_white['winner']==0]
    df_white_win = df_white[df_white['winner']==1]
    #This makes the distribution of wins and losses more similar to allow for better comparison
    if df_white_loss['winner'].count() < df_white_win['winner'].count():
        df_white_win = df_white_win.head(df_white_loss['winner'].count())
    else:
        df_white_loss = df_white_loss.head(df_white_win['winner'].count())
    df_white = pd.concat([df_white_win, df_white_loss])
    df_black_loss = df_black[df_black['winner']==0]
    df_black_win = df_black[df_black['winner']==1]
    if df_black_loss['winner'].count() < df_black_win['winner'].count():
        df_black_win = df_black_win.head(df_black_loss['winner'].count())
    else:
        df_black_loss = df_black_loss.head(df_black_win['winner'].count())
    df_black = pd.concat([df_black_win, df_black_loss])
    white_ana = logistic_regression(df_white) 
    black_ana = logistic_regression(df_black)
    if sm_or_not:
        p_white, w_acc = sm_logit(df_white)
        p_black, b_acc = sm_logit(df_black)
    else:
        p_white, w_acc = smf_logit(df_white)
        p_black, b_acc = smf_logit(df_black)
    p_white = pd.DataFrame(p_white.pvalues[1:]).sort_values(by=0)
    p_white.columns = ['pvalue']
    p_white['include'] = p_white['pvalue']<=0.15
    for i in p_white.index:
        #We only want moves that are statistically somewhat significant for the result as well as it accounts for a lot of the losses compared to the wins (note that 'a lot' here does not mean there is more losses than wins with it)
        if p_white.loc[i, 'include'] and 2.5*df_white_loss[i].sum()/df_white_loss[i].count()<=df_white_win[i].sum()/df_white_win[i].count():
            p_white.loc[i, 'include'] = False
    p_black = pd.DataFrame(p_black.pvalues[1:]).sort_values(by=0)
    p_black.columns = ['pvalue']
    p_black['include'] = p_black['pvalue']<=0.15
    for i in p_black.index:
        if p_black.loc[i, 'include'] and 2.5*df_black_loss[i].sum()/df_black_loss[i].count()<=df_black_win[i].sum()/df_black_win[i].count():
            p_black.loc[i, 'include'] = False
    p_white.to_json('pos.json', orient = 'split', compression = 'infer')
    p_black.to_json('neg.json', orient = 'split', compression = 'infer')
    with open('reg.txt', 'w') as f:
        f.write(str(white_ana[0]) + ", " + str(white_ana[1]) + ", " + str(w_acc))
        f.write('\n')
        f.write(str(black_ana[0]) + ", " + str(black_ana[1]) + ", " + str(b_acc))
    
def sm_logit(df):
    df_now = df.drop(['winner'], axis=1)
    win = df['winner']
    logit_model=sm.Logit(win, df_now)
    result=logit_model.fit()
    in_sample = pd.DataFrame({'prob':result.predict()})
    in_sample['pred_label'] = (in_sample['prob']>0.5).astype(int)
    return result, accuracy_score(df['winner'], in_sample['pred_label'])

def smf_logit(df):
    columns = [col for col in df.columns]
    arg = columns[0] + " ~  " + columns[1] 
    for col in columns[2:]:
        arg += " + " + col
    log_reg = smf.logit(arg, data=df).fit()
    in_sample = pd.DataFrame({'prob':log_reg.predict()})
    in_sample['pred_label'] = (in_sample['prob']>0.5).astype(int)
    return log_reg, accuracy_score(df[columns[0]], in_sample['pred_label'])

def regression(df):
    p = pd.DataFrame()
    p["Moves"] = list(df.columns)[1:]
    p["P"] = feature_selection.f_regression(df[list(df.columns)[1:]], df.winner)[1]
    return p

def logistic_regression(df):
    df_now = df.drop(['winner'], axis=1)
    win = df['winner']
    X_train, X_test, y_train, y_test = model_selection.train_test_split(df.drop(['winner'], axis=1), df.winner)

    reg_views = linear_model.LogisticRegression().fit(X_train, y_train)
    reg_views_score = reg_views.score(X_test, y_test)
    reg_views2 = linear_model.LogisticRegression().fit(df_now, win)
    reg_views2_score = reg_views2.score(df_now, win)
    return reg_views_score, reg_views2_score


def load(player: str, game: str, max: int, pgn: bool):
    session = berserk.TokenSession('lip_IcEC8JTT9lYcvdCWspNh')
    client = berserk.Client(session=session)
    #Generator for the games (black and white seperately)
    white = client.games.export_by_player(player, perf_type=game, max=max, color="white", as_pgn=pgn)
    black = client.games.export_by_player(player, perf_type=game, max=max, color="black", as_pgn=pgn)
    return white, black

def game_to_list(white_games, black_games, white, black, white_or_not):
    #We cannot do too many queries, different ways were tried such as putting sleep between these two, most ways did not work
    if white_or_not:
        white_game = next(white)
        #We care about overextention, therefore moves that take are hard to evaluate as well as pawn moves that are checks
        #Therefore those are ignored, also pushing to 6th rank or further probably means either the pawn was doomed to die anyway or it is going towards queening, both of which are hard to evaluate in terms of overextension.  
        #If there is no winner, the game was a draw, the generator ignores aborted games automatically, here draw=0.5, loss=1, and win=0
        #Draws are removed since we care about only wins and losses
        white_game_dict = {'winner': 0.5, 'a4': 0, 'a5': 0, 'a6': 0, 'b4': 0, 'b5': 0, 'b6': 0, 'c4': 0, 'c5': 0, 'c6': 0, 'd4': 0, 'd5': 0, 'd6': 0, 'e4': 0, 'e5': 0, 'e6': 0, 'f4': 0, 'f5': 0, 'f6': 0, 'g4': 0, 'g5': 0, 'g6': 0, 'h4': 0, 'h5': 0, 'h6': 0}
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
        return

    black_game_dict = {'winner': 0.5, 'a3': 0, 'a4': 0, 'a5': 0, 'b3': 0, 'b4': 0, 'b5': 0, 'c3': 0, 'c4': 0, 'c5': 0, 'd3': 0, 'd4': 0, 'd5': 0, 'e3': 0, 'e4': 0, 'e5': 0, 'f3': 0, 'f4': 0, 'f5': 0, 'g3': 0, 'g4': 0, 'g5': 0, 'h3': 0, 'h4': 0, 'h5': 0}

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
    main('penguingim1', 'blitz', 1000, False, True)