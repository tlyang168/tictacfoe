import random
import sys
import os
import json
import strategy as strat
from tkinter import *
import tkinter.messagebox

""" 
TIC-TAC-TOE GAME

You against the computer (appropriately named 'Big Boi') 
GUI is adapted to allow for game restarts and score tracking based on username between game sessions.
Top scorer is remembered.
"""

###############################################################################
#       Handling Usernames: bringing old ones from memory and adding new      #
###############################################################################

with open('GameSaves.json') as f:
    data = json.load(f)

def find_high(d):
    """Finds highest score from past sessions."""
    largest = 0
    person = ''
    for i in d:
        rate = (lambda x, y: (0.5*x) + (0.5*(x / y)))(d[i][i], (d[i][i] + d[i]['Big Boi']))
        if rate > largest:
            largest = rate
            person = i
    return person, largest


high, h_score= find_high(data)


def save(players):
    """Saves the current play state to GameSaves.json"""
    new_state = {}
    if isinstance(players[0], Computer):
        players = players[::-1]
    new_state[players[0].name] = {players[0].name: players[0].score, players[1].name: players[1].score}
    data.update(new_state)
    with open('GameSaves.json', 'w') as f:
        json.dump(data, f, indent=1)


def store_delete(n, name):
    """Takes in an integer n and a string name to assign the name to the n index in Grids.players."""
    Grids.players[n].name = name.title()
    Grids.e1.delete(0, 'end')
    Grids.e1.place_forget()


def update_mem_score(name, n_human, n_computer):
    """Finds scores in json memory and brings it to the current state"""
    if name in data:
        print('testing json', data[name][name])
        print('testing json', data[name]['Big Boi'])
        Grids.players[n_human].score = data[name][name]
        Grids.players[n_computer].score = data[name]['Big Boi']


def keep_name(entry, event):
    """Calls store_delete to keep the user input and delete the entry box."""
    name = entry.get().title().strip()
    [enable(Grids.buttons[i]) for i in Grids.buttons]
    if not isinstance(Grids.players[0], Computer):
        store_delete(0, name)
        update_mem_score(name, 0, 1)
        Grids.scoresdisplay(g)
    else:
        store_delete(1, name)
        update_mem_score(name, 1, 0)
        Grids.scoresdisplay(g)


def store_username():
    """Creates an Entry widget to get the name of the user."""
    p1 = StringVar()
    Grids.e1 = Entry(root, bd=0, textvariable=p1, bg="#E2C044", fg="white")
    Grids.e1.place(x=340, y=260)
    p1.set("Input name here")
    Grids.e1.bind("<Return>", lambda x: keep_name(p1, x))

def order():
    """Sets the player with symbol x as the first player."""
    if Grids.players[1].sym == 'X':
        Grids.players.reverse()


######################
#       Classes      #
######################


class Grids:
    moved_already, players = [], []
    buttons = {}
    gameover = False

    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(root, height=300, 
                            width=500, bg="white", relief=FLAT)

        self.label = Label(self.canvas, text="TIC TAC FOE", font=('Helvetica', '16'), 
                            fg="#2D080A", bg="white")
        self.canvas.pack()
        self.label.place(x=335, y=10)

        #creates the tiles for X's and O's
        self.squares()

        #Takes input and disables game until noncomputer player types a name
        [disable(Grids.buttons[i]) for i in Grids.buttons]
        store_username()

        #Setting up the initial scoreboard frame with SCOREBOARD, PLAYERS, and SCORE
        self.scoreboard = Frame(root, bg="#393E41",
                        height=120, width=122)
        self.scoreboard.place(x=340, y=130)
        scorelbl = Label(self.scoreboard, text="SCOREBOARD", fg="white", bg="#393E41", font=('Helvetica', '10'))
        scorelbl.grid(row= 0, column=1, columnspan=2, pady=2, padx=10, sticky=N)
        ppl = Label(self.scoreboard, text= "PLAYERS", 
                    fg="white", bg="#393E41", font=('Helvetica', '8'))
        sc = Label(self.scoreboard, text= "SCORE", 
                    fg="white", bg="#393E41", font=('Helvetica', '8'))
        highscore = Label(self.scoreboard, text= "BEST", 
                    fg="white", bg="#393E41", font=('Helvetica', '8'))
        winratio = Label(self.scoreboard, text= "RATIO", 
                    fg="white", bg="#393E41", font=('Helvetica', '8'))
        ppl.grid(row= 1, column=1, pady=2, padx=10, sticky=W)
        sc.grid(row= 1, column=2, pady=2, padx=4, sticky=E)
        highscore.grid(row= 4, column=1, pady=2, padx=10, sticky=W)
        winratio.grid(row= 4, column=2, pady=2, padx=4, sticky=E)


    def squares(self):
        """Creates buttons with key representing the col-row index and sets button function to take turn"""
        for i in range(3):
            for j in range(3):
                self.buttons[(j, i)] = Button(self.root, fg="white", bg="#587B7F", 
                                            font=('Helvetica', '30'), bd = 0) 
                self.buttons[(j, i)].place(height=98, width=98, 
                                            x= (SCL * i), y=(SCL *j))
        
        for indx in self.buttons:
            self.buttons[indx]['command'] = (lambda btn: lambda: taketurn(btn))(self.buttons[indx])

        
    def scoresdisplay(self):
        """"Adds in player names next to symbols X and O, shows respective scores."""
        Grids.p1 = Label(self.scoreboard, text= "On X: " + Grids.players[0].name, 
                    fg="white", bg="#393E41", font=('Helvetica', '8'))
        Grids.p2 = Label(self.scoreboard, text= "On O: " + Grids.players[1].name, 
                    fg="white", bg="#393E41", font=('Helvetica', '8'))
        Grids.h = Label(self.scoreboard, text=high, 
                    fg="white", bg="#393E41", font=('Helvetica', '8'))
        Grids.hs = Label(self.scoreboard, text="{0:.2f}".format(h_score), 
                    fg="white", bg="#393E41", font=('Helvetica', '8'))
        Grids.s1 = Label(self.scoreboard, text= Grids.players[0].score, 
                    fg="white", bg="#393E41", font=('Helvetica', '8'))
        Grids.s2 = Label(self.scoreboard, text= Grids.players[1].score, 
                    fg="white", bg="#393E41", font=('Helvetica', '8'))
        Grids.p1.grid(row= 2, column=1, columnspan=2, pady=2, padx=10, sticky=W)
        Grids.p2.grid(row= 3, column=1, columnspan=10, pady=2, padx=10, sticky=W)
        Grids.h.grid(row= 5, column=1, columnspan=2, pady=2, padx=10, sticky=W)
        Grids.s1.grid(row= 2, column=2, pady=2, padx=4, sticky=E)
        Grids.s2.grid(row= 3, column=2, pady=10, padx=4, sticky=E)
        Grids.hs.grid(row= 5, column=2, pady=2, padx=4, sticky=E)



class Player:
    symbols = ['X', 'O']
    outcome = "loss"
    def __init__(self, name):
        self.score = 0
        self.name = name
        self.sym = random.choice(Player.symbols)
        Player.symbols.remove(self.sym)


    def __repr__(self):
        return f'{self.name}' 


    def win(self):
        """Increase the score and change the game status of winning player"""
        self.score += 1
        Grids.gameover = True
        if isinstance(self, Computer):
            Player.outcome = "win"
        return str(self) + " wins!"


class Computer(Player):
    moves = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    opponent_warnings, winning_move = [], []

    def play(self):
        """Computer playing strategy."""

        one_step_from_losing()
        print("Opponent warning:", Computer.opponent_warnings) #shows index of tile that will lead to opponent win in next move
        print("Winning notice:", Computer.winning_move) #shows index of tile that will lead to Big Boi winning in next move

        avail_moves = list(filter(lambda x: (x not in Grids.moved_already), self.moves))

        tile = random.choice(avail_moves)
        win_i = strat.triumph(avail_moves, Computer.winning_move, is_not_pressed)
        block_i = strat.block(avail_moves, Computer.opponent_warnings, is_not_pressed)

        strat.make_move(win_i, block_i, tile, Grids.buttons, taketurn, is_not_pressed)
        
###############################
#       Playing the Game      #
###############################


def disable(button):
    """Grays out button and prevents new clicks."""
    button['state'] = 'disabled'


def enable(button):
    """Allows new button clicks to occur."""
    button['state'] = 'normal'


def play_game():
    """Allows the computer to make a move."""
    if not Grids.gameover:
        if isinstance(curr_player, Computer):
            curr_player.play()


def switch_player():
    """Changes current player to next player."""
    global curr_player
    if curr_player == Grids.players[0]:
        curr_player = Grids.players[1]
    else:
        curr_player = Grids.players[0]

turns = 0

def taketurn(button):
    """Lets current player make a move, checks for win, and then changes current player to next player."""
    global turns, curr_player
    if not button["text"]:
        Grids.moved_already.extend([indx for indx, btn in Grids.buttons.items() if btn == button])
        print(Grids.moved_already)
        button["text"] = curr_player.sym
        win_check()
        turns += 1
        switch_player()
        play_game()
    else:
        tkinter.messagebox.showinfo(message='This tile is taken. Please pick a new one.', title="Notice")


def win_check():
    """Checks for a win or a tie and changes appropriate labels"""
    x_win = any(all_check(three, x_check))
    o_win = any(all_check(three, o_check))
    def helper(n, tie=False):
        """"Generalizes the function calls and assignment for all three cases, where n is the player index"""
        scores = [Grids.s1, Grids.s2]
        [disable(Grids.buttons[i]) for i in Grids.buttons]
        winlabel.place(height=20, width=122, x=340, y=50)
        if tie == False:
            winlabel['text'] = Grids.players[n].win()
            scores[n]['text'] = Grids.players[n].score
            make_restart()
        else:
            winlabel['text'] = "Tie!"
            Grids.gameover = True
            make_restart()
    
    if x_win:
        helper(0)
    elif o_win:
        helper(1)
    elif turns == 8:
        Player.outcome = "tie"
        helper(8, True)


x_check = lambda btn: btn['text'] == 'X'
o_check = lambda btn: btn['text'] == 'O'


def three(lst):
    """ Looks at a list of lists representing row_check, col_check, and diagonal.
    Checks to see if the inner lists have all True values.
    This tells us if each row, col, or diagonal has three Xs or three Os.
    """
    return any([all(inner) for inner in lst])


is_not_pressed = lambda i: (not Grids.buttons[i]['text'])

def range3generator():
    yield 0
    yield 1
    yield 2
    yield from range3generator()

def one_step_from_losing():
    """Identifies next moves for computer when opponent has 2/3 filled"""
    symbols = ['X', 'O']
    symbols.remove(next(filter(lambda x: isinstance(x, Computer), Grids.players)).sym)
    i_finder_op = lambda x, y: strat.identify_index(x, y, Computer.opponent_warnings, is_not_pressed)
    i_finder_comp = lambda x, y: strat.identify_index(x, y, Computer.winning_move, is_not_pressed)

    def helper(opcheck, compcheck):
        """Calls the strat.identify_index function on each row, col, diag of the game state"""
        gen = range3generator()
        state = game_state(opcheck)
        [i_finder_op(i, next(gen)) for i in list(state)]
        state = game_state(compcheck)
        [i_finder_comp(i, next(gen)) for i in list(state)]

    if symbols[0] == 'X':
        helper(x_check, o_check)
    else:
        helper(o_check, x_check)


def two(lst):
    """ Checks to see if a win will happen in the next turn. Any two in row, col, or diagonal has same symbol."""
    return any([strat.all_but1(inner) for inner in lst])


def all_check(num_func, check):
    """Takes in a number function (three or two) and check functions to see how many of same type symbol are on tiles. Returns a list."""
    r, c, d = game_state(check)
    return [num_func(r), num_func(c), num_func(d)]


def game_state(check):
    """ Checks each row, col, and diagonal for X's or O's in a row.
    Intakes a check function that looks at the text of the button.
    Returns True or False.
    """
    row_check, col_check, diagonal = [[],[],[]], [[],[],[]], [[],[]]
    for row in range(3):
        for i in range(3):
            if (row == 0 and i==2) or (row == 2 and i==0) or (row == 1 and i==1):
                diagonal[1].append(check(Grids.buttons[(row, i)])) #checks diagonal going from NE to SW
            col_check[row].append(check(Grids.buttons[(row, i)]))
            row_check[row].append(check(Grids.buttons[(i, row)]))
        diagonal[0].append(check(Grids.buttons[row, row])) #checks diagonal going from NW to SE
    return row_check, col_check, diagonal

###############################
#       End of Game Menu      #
###############################

def make_restart():
    """Creates Again (play again), New (start over), and Quit in window"""
    if Grids.gameover:
        strat.save_board(Grids.moved_already, Computer, Grids.players, Player.outcome)
        restartbtn.place(x=390, y=90) #New button
        quitbtn.place(x=432, y=90)
        enable(contbtn) 
        contbtn.place(x=340, y=90) #Again button
        print(Grids.players, [p.score for p in Grids.players])


def restart():
    """Restarts the game from initial state"""
    save(Grids.players)
    python = sys.executable
    os.execl(python, python, * sys.argv)


def quitout():
    """Saves the current game with username and quits"""
    save(Grids.players)
    root.destroy()


def new_syms():
    """Randomly picks new symbols for players on the nth iteration of the game"""
    Grids.players[0].sym = 'O'
    Grids.players[1].sym = 'X'
    order()
    Grids.p1['text'] = "On X: " + Grids.players[0].name
    Grids.s1['text'] = Grids.players[0].score
    Grids.p2['text'] = "On O: " + Grids.players[1].name
    Grids.s2['text'] = Grids.players[1].score


def play_again():
    """Clears the board to continue current game, and pick new x and o for players"""
    global turns, curr_player
    for i in Grids.buttons:
        Grids.buttons[i]['text'] = ""
        Grids.buttons[i]['command'] = (lambda btn: lambda: taketurn(btn))(Grids.buttons[i])
        enable(Grids.buttons[i])
    new_syms()
    curr_player = Grids.players[0]
    winlabel.place_forget()
    Grids.moved_already, Computer.opponent_warnings, Computer.winning_move = [], [], []
    Grids.gameover = False
    Player.outcome = "loss"
    turns = 0
    disable(contbtn)
    play_game()



if __name__ == "__main__":
    SCL = 100 #gives the length of each square tile, scaling it 1:100
    root = Tk()
    root.title("Tic Tac Toe")

    g = Grids(root)
    Grids.players.extend([Player("Big Boi"), Computer("Big Boi")])
    order()

    winlabel = Label(root, font=('Helvetica', '10'), 
                    bg="#E2C044", fg="white")
    
    restartbtn = Button(root, text="New", command=restart, bd=0, bg="#D3D0CB")
    contbtn = Button(root, text="Again", command=play_again, bd=0, bg="#D3D0CB")
    quitbtn = Button(root, text="Quit", command=quitout, bd=0, bg="#D3D0CB")
    
    curr_player = Grids.players[0]
    play_game()
    root.mainloop()
