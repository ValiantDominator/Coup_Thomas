"""
@author Thomas

Player class
"""
# Build a player class in coup.py
    # Data
        # Coins
        # Cards
        # log ### Whenever the game writes to its game file, it also writes
              ### to each player's log
    # act()
        # If you have fewer than 7 coins, tax. Else, coup another player
        # You might have to parse the log to find another active player's name.
import random

class Player:
    def __init__ (self):
        self.coins = 3
        self.cards = []
        self.log = ""
    def act():
        #determine what to do and return something like "tax"
        #or "steal markus"
        if self.coins >= 7:
            return "coup"
        else:
            return "tax"
        
class Deck:
    def __init__(self, cards=[]):
        self.deck = cards
    def add(self,newcard):
        if type(newcard) == str:
            self.deck.append(newcard)
        else:
            print('new card must be str')
    def show(self):
        for i in (self.deck):
            print(i)
    def shuffle(self):
        random.shuffle(self.deck)
    def draw(self):
        drawncard = self.deck[0]
        self.deck.pop(0)
        return drawncard
    def coupInit(self):
        self.deck.clear()
        coupcards = ["Duke", "Assassin", "Captain", "Ambassator", "Contessa"]
        self.deck = coupcards*3

coupdeck = Deck()
coupdeck.coupInit()
coupdeck.show()

def actionHandler(action_str):
    #parse string
    #choose action
    #modify player data
    print("ahhh")

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
            
#wishlist:
    #actionHandler (run an action depending on what string is inputted)

class Game_Master:
    def __init__(self,filename="default_game.coup"):
        self.filename = filename