import berserk

def main(playerName: str, game_type: str):
    client = berserk.Client()
    #Generator for the games
    games = client.games.export_by_player(playerName, perf_type=game_type)
    print("Test values:")
    for i in range(10):
        print(next(games))


if __name__ == "__main__":
    main('C9C9C9C9C9', 'blitz')