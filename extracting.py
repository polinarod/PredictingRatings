import chess.pgn
import pandas as pd
import numpy as np
from math import ceil

stockfish = pd.read_csv('data\stockfish.csv')
stockfish.MoveScores = stockfish.MoveScores.str.replace('NA','').str.split()
stockfish.MoveScores = stockfish.MoveScores.apply(lambda x: list(map(int, x)))
stockfish.drop("Event",axis=1,inplace=True)

def get_games(filename="data\data.pgn"):
    with open(filename) as pgn:
        game = chess.pgn.read_game(pgn)
        cnt = 0
        while game:
            cnt += 1
            yield game
            game = chess.pgn.read_game(pgn)

games = get_games()

white_elos = []
black_elos = []
results = []
moves = []
uci_moves=[]
counts=[]

for game in games:
    if 'WhiteElo' in game.headers:
        white_elos.append(game.headers['WhiteElo'])
    if 'BlackElo' in game.headers:
        black_elos.append(game.headers['BlackElo'])
    results.append(game.headers['Result'])

    node = game.variation(0)
    sans = []
    uci=[]
    count = 0

    while node.variations:
        board = node.board()
        count += 1
        sans.append(node.san())
        uci.append(node.uci())
        node = node.variations[0]

    board = node.board()
    count += 1
    sans.append(node.san())
    uci.append(node.uci())
    count = ceil(count / 2)

    counts.append(count)
    moves.append(sans)
    uci_moves.append(uci)

df=pd.DataFrame(np.column_stack([results,moves,uci_moves,stockfish.MoveScores,counts]),
                columns=['Result','Moves','UCI','Scores','NumMoves'])

df.to_csv(r'data\games.csv', sep=',',index=False)

elos=pd.DataFrame(np.column_stack([white_elos,black_elos]),
                columns=['WhiteElo','BlackElo'])
elos.to_csv(r'data\elos.csv', sep=',',index=False)
