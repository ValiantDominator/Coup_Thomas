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
import human_player

'''
valid coup actions:
    income
    foreign aid
    coup
    steal
    tax
    assassinate
    swap
    block_steal
    block_foreign_aid
    block_assassinate
    challenge
    '''

class Player:
    def __init__ (self,name="default_player",debug=False):
        self.name = name
        self.coins = 3
        self.cards = []
        self.log = ""
        self.actions_taken = 0
        self.opponents = []
        self.debug = debug
    def react(self,hint="turn"):
        if self.actions_taken == 0:
            self.find_opponents()
            
        if self.debug:
            print(self.name + " actions_taken ", self.actions_taken)
            print("coins:", self.coins)
            print("cards:", self.cards)
            print("log:", self.log)
            print("")
        self.actions_taken += 1
        #determine what to do and return something like "tax"
        #or "steal markus"
        if self.coins >= 7:
            return ("coup " + self.target_selection())
        else:
            return "tax"
    def receive(self,newlog):
        self.log = newlog
    def discard(self):
        discard = self.cards[0]
        self.cards.pop(0)
        return discard
    def find_opponents(self):
        log_copy = self.log
        log_lines = log_copy.split("\n")
        log_first_line = log_lines[0]
        players = log_first_line.split(" ")
        players.pop(0)
        for i in range(len(players)):
            players[i]=players[i].replace("[","")
            players[i]=players[i].replace(",","")
            players[i]=players[i].replace("]","")
            players[i]=players[i].replace("'","")
        for i in players:
            if self.name == i:
                pass
            else:
                self.opponents.append(i)
    def target_selection(self):
        random.shuffle(self.opponents)
        if self.debug:
            print("I am " + self.name + " and I fight", self.opponents[0])
        return self.opponents[0]
        
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
    def put_on_top(self,card):
        self.deck.insert(0,card)

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
        self.players = []
        self.deck = Deck()
        self.list_of_active_players = []
        self.log = ""
        self.active_player = Player()
    # MAIN FUNCTIONS
    def game_init(self,list_of_players):
        #create deck and shuffle it
        self.deck.coupInit()
        self.deck.shuffle()
        
        #start log
        player_name_list = []
        for i in list_of_players:
            player_name_list.append(i.name)
        player_name_list = str(player_name_list)
        player_name_list.replace("'","")
        self.add_to_log(("players: " + player_name_list))
        
        #add in players and give them cards
        for i in list_of_players:
            self.list_of_active_players.append(i)
            i.cards.append(self.deck.draw())
            i.cards.append(self.deck.draw())
        self.active_player = self.list_of_active_players[0]
        
    def turn(self):
        #give every player the gamestate
        for i in self.list_of_active_players:
            i.receive(self.log)
        
        #ask the active player what action they want
        action = self.active_player.react("turn")
        action_str = (self.active_player.name + " " + action)
        
        #update the log
        self.add_to_log(action_str)
        
        #execute the action
        self.action_handler(action_str)
        
        #rotate to next active players
        self.next_active_player()
        pass
    
    def game(self):
        while len(self.list_of_active_players) > 1:
            self.turn()
        self.add_to_log("winner: " + self.list_of_active_players[0].name)
        coupFile = open(self.filename,'w')
        coupFile.write(self.log)
        coupFile.close()
        
        
    
    #BONUS FUNCTIONS
    def add_to_log(self,message):
        self.log += message
        self.log += "\n"
        
    def next_active_player(self):
        current_player_index = 0
        for i in (self.list_of_active_players):
            if i == self.active_player:
                break
            else:
                current_player_index += 1
        if current_player_index == (len(self.list_of_active_players) + -1):
            next_player_index = 0
        else:
            next_player_index = current_player_index + 1
        
        self.active_player = self.list_of_active_players[next_player_index]
    
    def eliminate(self,player):
        self.list_of_active_players.remove(player)

    def action_handler(self,action_str):
        #parse string
        action_list = action_str.split(" ")
        acting_player = self.name_to_player(action_list[0])
        if len(action_list)>2:
            receiving_player = self.name_to_player(action_list[2])
        action = action_list[1]
        
        #choose action
        #modify player data
        if action == "income":
            acting_player.coins += 1
        elif action == "foreign_aid":
            if self.foreign_aid_check:
                acting_player.coins += 2
        elif action == "coup":
            if self.coup_check(acting_player,receiving_player):
                acting_player.coins += -7
                self.add_to_log(receiving_player.name + " discards " + 
                receiving_player.discard())
                if len(receiving_player.cards) == 0:
                    self.eliminate(receiving_player)
        elif action == "steal":
            if self.steal_check(acting_player,receiving_player):
                steal_amount = max(2,receiving_player.coins)
                acting_player.coins += steal_amount
                receiving_player.coins += steal_amount
        elif action == "tax":
            if self.tax_check(acting_player):
                acting_player.coins += 3
        elif action == "assassinate":
            if self.assassinate_check(acting_player,receiving_player):
                acting_player.coins += -3
                receiving_player.discard()
        elif action == "swap":
            if self.swap_check(acting_player,receiving_player):
                acting_player.cards.append(self.deck.draw())
                acting_player.cards.append(self.deck.draw())
                
                self.deck.lay_on_top(acting_player.react("placeback"))
                self.deck.lay_on_top(acting_player.react("placeback"))
    
    def foreign_aid_check(self,acting_player):
        return True
    
    def coup_check(self,acting_player,receiving_player):
        if acting_player.coins < 7:
            return False
        if len(receiving_player.cards) < 1:
            return False
        return True
    
    def steal_check(self,acting_player,receiving_player):
        return True
    
    def tax_check(self,acting_player):
        return True
    
    def assassinate_check(self,acting_player,receiving_player):
        pass
    
    def swap_check(self,acting_player,receiving_player):
        pass
    
    def name_to_player(self,player_name):
        for i in self.list_of_active_players:
            if i.name == player_name:
                return i
        print("Error at name_to_player")
        print(i)
        print(player_name)
    
coupgame = Game_Master()
p1 = Player("Joe_Creek")
p2 = Player("MY_GUY")
p3 = human_player.Player("man")
coupgame.game_init([p1,p2,p3])