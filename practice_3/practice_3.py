"""
@author: Thomas
"""
# Problem 1
# Write a function that takes a string as an argument
# Returns: the longest substring in that string after splitting the string
#          based on spaces.
# Example: my_func("hello world my name is Daniel")
#          returns: "Daniel"
def longestWord (sentence):
    if type(sentence) is str:
        wordss = sentence.split(" ")
        wordss.sort(key=len)
        return wordss[-1]
    else:
        print("Error; enter a string")
        return None
print(longestWord("hello world my name is Daniel"))
# Problem 2
# In any way you see fit, find a way to *programmatically* determine whether
# the 8 files `game_*.coup` are valid games.
# You probably won't directly use this in your coup Game_Master,
# but you'll definitely implement a better game master with this knowledge.
# Recommendation: write some helper functions that are modular and easily
#                 usable in your coup.py file you'll make later on.

#geez dood, it really seems that i should go ahead and go all out for this
def coupResultParser (name_of_coup_file):
    coupFile = open(name_of_coup_file)
    rawtext = coupFile.read()
    coupFile.close()
    #turn string into list
    textlines = rawtext.split("\n")
    try:
        textlines.remove(" ")
    except:
        None
    try:
        textlines.remove("")
    except:
        None
    #this is ur fault danny ;)
    actionline = textlines[1:-1]
    players = textlines[0]
    winner = textlines[-1]
    return [actionline,players,winner]

def income(playerAData,playerBData):
    playerAData[2] += 1
    valid = True
    return [playerAData,playerBData,valid]

def foreign_aid(playerAData,playerBData):
    playerAData[2] += 2
    valid = True
    return [playerAData,playerBData,valid]

def coup(playerAData,playerBData):
    ###player a coups from player b
    ###does not check for validity of the move
    playerAData[2] += -7
    playerBData[1] += -1
    valid = True
    if playerAData[2]<1 or playerBData[1]<1:
        valid = False
    return [playerAData,playerBData,valid]

def tax(playerAData,playerBData):
    playerAData[2] += 3
    valid = True
    return [playerAData,playerBData,valid]

def steal(playerAData,playerBData):
    ###player a steals from player b
    ###returns the data of the 2 players
    ###does not check for validity of the move
    stealamount = 0
    while (stealamount < 2) & ((playerBData)[2] > 0):
        playerAData[2] += 1
        playerBData[2] += -1
        stealamount += 1
    valid = True
    if playerAData[2]<1 or playerBData[2]<1: ##spageti coad
        valid = False
    return [playerAData,playerBData,valid]

def exchange(playerAData,playerBData):
    playerAData[1] += 2
    ###stuff happens
    playerAData[1] += -2
    valid = True
    return [playerAData,playerBData,valid]

def assassinate(playerAData,playerBData):
    ###player a coups from player b
    ###does not check for validity of the move
    playerAData[2] += -3
    playerBData[1] += -1
    valid = True
    if playerAData[2]<1 or playerBData[1]<1: ##spageti coad
        valid = False
    return [playerAData,playerBData,valid]

def actionLineParser(actionline,playerdata,numplayers):
    # turn line of file into an action, returns the new gamestate
    # to the master fucntion.
    actionparts = actionline.split(" ")
    for x in range(numplayers):
        if playerdata[1][0] == actionparts[0]:
            playerAData = playerdata[x]
            playerALocation = x
        if len(actionparts) == 3:
            if playerdata[1][0] == actionparts[2]:
                playerBData = playerdata[x]
                playerBLocation = x
    #now we have found our players! now we can make action
    action = actionparts[1]
    [playerAData,playerBData,valid]=locals()[action](playerAData,playerBData)
    playerdata[playerALocation]=playerAData
    playerdata[playerBLocation]=playerBData
    return [playerdata,valid]
    
def gameResult (name_of_coup_file):
    [actionlines,plers,winner] = coupResultParser(name_of_coup_file)
    #translate players
    players = plers.split(" ")
    players.pop(0)
    for i in range(len(players)):
        players[i]=players[i].replace("[","")
        players[i]=players[i].replace(",","")
        players[i]=players[i].replace("]","")
    numplayers = len(players)
    numactions = len(actionlines)
    ##now we have a list for player names, coin, and lives
    ##combine them into a list of lists
    ## PLAYER_NAME LIVES COINS
    playerdata = []
    for x in range(numplayers):
        playerdata.append([players[x],2,3])
    x = 0
    valid = True
    while (x < numactions) and (valid == True):
        x +=1
        #run the game
        [playerdata,valid] = actionLineParser(actionlines[x],playerdata,numplayers)
    
    
name_of_coup_file="game_a.coup"
gameResult("game_a.coup")
[actionlines,players,winner] = coupResultParser("game_a.coup")

# Problem 3
# Build yourself a 'coup' directory and make a file called coup.py there.
# Build a player class in coup.py
    # Data
        # Coins
        # Cards
        # log ### Whenever the game writes to its game file, it also writes
              ### to each player's log
    # act()
        # If you have fewer than 7 coins, tax. Else, coup another player
        # You might have to parse the log to find another active player's name.


# Problem 4
# Copy over your deck class from practice 2 to coup.py
# Add the draw() method, which returns the first (top) card in the deck
# and then removes that card from the deck

# Problem 5
# Build a class Game_Master in coup.py
    # Data:
        # players
        # gamefile (file opened by game_init() and closed when the game ends)
        # deck
    # Methods:
        # game_init() (Note, this is *not* the __init__ function)
            # Arguments: the names of the players
            # Initializes the deck with 5 cards (they can all be dukes for now)
            # Give each player 2 cards and 2 coins
        # turn()
            # Process one action, such as "a tax" or "markus steal daniel"
            # Check to see whether that action was valid
            # Write that action to a gamefile and each player's log
            # If a player had to discard, also write that action to a gamefile
            # Update player cards and coins accordingly
        # game()
            # initialize a game and call turn() until the game is over
# Play a FFA game with 3 players and submit the file in your practice_3
# directory (since your Game_Master class lives in another directory)

"""
The following problem is for Michael, Thomas, and Philip
"""
# Problem 6
# Assume your player class only plays 1v1 coup.
# What is the optimal strategy for a no blocking, no challenging coup?
# Adjust your player class to adopt this strategy.
# To receive 4/4 on this assignment, I must *not* be able to design
# An agent to beat your player (no matter who goes first)