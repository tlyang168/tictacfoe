import json

##############################################################################
#                STRATEGY 1: basic survival
##############################################################################

"""
THE DON'T LOSE METHOD
1. If there is a opportunity to win in the next turn, take it.
    1. we check each row, col, diagonal for 2 of the Computer's symbol in that path.
    If there is 2 in any, we tell Big Boi to fill
2. If there is an opportunity to lose in the next turn, block it.
3. else: choose a random location so the human player doesn't learn its strategies
"""

def make_move(w_i, b_i, t_i, btns, turnfunc, pressfunc):
    """Allows the computer to make a move for its turn based on the indexes of tiles to win, block, or strategize"""
    if w_i and pressfunc(w_i):
        btns[w_i]['command'] = (lambda btn: lambda: turnfunc(btn))(btns[w_i])()
    elif b_i and pressfunc(b_i):
        btns[b_i]['command'] = (lambda btn: lambda: turnfunc(btn))(btns[b_i])()
    elif pressfunc(t_i):
        btns[t_i]['command'] = (lambda btn: lambda: turnfunc(btn))(btns[t_i])()


def block(possible_moves, hotspot, pressfunc):
    """Returns the index of the tile to block a win from the opponent in the next turn"""
    if hotspot:
        latest = hotspot[-1]
        return latest


def triumph(possible_moves, winspot, pressfunc):
    """Returns the index of the tile to win in the next turn"""
    if winspot:
        latest = winspot[-1]
        return latest


def all_but1(lst):
    """Takes in a flat list and checks for 2 True values."""
    tcount = 0
    for i in lst:
        if i:
            tcount+=1
    if tcount == 2:
        return True
    else:
        return False


def identify_index(deeplst, path, win_loss, pressfunc): #path is 0: row, 1: col, or 2: diag; win_loss: list
    """Finds the index on the game board of the empty space of opponents' 2/3 filled r/c/d"""
    diags = [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]
    for r in range(len(deeplst)):
        if all_but1(deeplst[r]):
            for c in range(len(deeplst[r])):
                if not deeplst[r][c]:
                    if (path == 0 ) and ((c,r) not in win_loss) and pressfunc((c,r)):
                        win_loss.append((c, r))
                    elif (path == 1 ) and ((r, c) not in win_loss)and pressfunc((r,c)):
                        win_loss.append((r, c))
                    elif (path == 2 ) and (diags[r][c] not in win_loss)and pressfunc(diags[r][c]):
                        win_loss.append(diags[r][c])  


##############################################################################
#                STRATEGY 2: remembering past successful plays
##############################################################################

"""
1. If there is a opportunity to win in the next turn, take it.
2. If there is an opportunity to lose in the next turn, block it.
3. else: choose a location from a past successful game state that maximizes the outcome of the scenario
"""
with open('PastSuccess.json') as f:
        paststates = json.load(f)

def save_board(moves, kind, players, outcome): 
    """Saves the game sequence of a game."""
    p1 = next(filter(lambda x: isinstance(x, kind), players))
    moves.insert(0, p1.sym)
    new = moves[1:]
    paststates[moves[0]][outcome].append(new)
    with open('PastSuccess.json', 'w') as f:
        json.dump(paststates, f, indent=3)


    


