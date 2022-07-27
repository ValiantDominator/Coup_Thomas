# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 12:16:12 2022

@author: neeb-meister
"""

'''
Agent flyswatter

MACRO STRATEGY:
    -pick 1 of 3 turn patterns
    -pick 1 of 3 cb patterns
    -log data on which strat beats which opponents
    -prefer to pick the winning strat

TO DO:
    -fill out 2 turn patterns
    -fill out 2 cb patterns
    -add DATA LOG and initiliazer
    -add some randomness
    -optimize strats

'''
import Couptils
import pickle
import random


class Flyswatter:
    def __init__(self,name="flyswatter",debug=False):
        self.debug = debug
        self.cards = []
        self.coins = 0
        self.name = name
        self.force_challenge = False
    
    def react(self,hint):
        if hint == "turn":
            if self.turn_mode == "honest":
                return self.honest_turn()
            if self.turn_mode == "cheese":
                return self.cheese_turn()
            if self.turn_mode == "optimal":
                return self.optimal_turn()
        elif hint == "discard":
            return self.discard()
        elif hint == "placeback":
            return self.placeback()
        elif hint == "challenged":
            return self.challenged()
        elif hint == "cb?":
            if self.cb_mode == "alpha":
                return self.alpha_cb()
            if self.cb_mode == "bravo":
                return self.bravo_cb()
            if self.cb_mode == "charlie":
                return self.charlie_cb()
            return self.cb()
        
        
        
    def honest_turn(self):\
        #Coup
        if self.coins >= 10:
            return ("coup " + self.find_target())
        
        if self.coins >= 7 and len(self.opponents) == 1:
            return ("coup " + self.find_target())
        
        #Assassinate
        if (self.coins >= 3 and "contessa" not in 
            self.assumed_opponent_cards[self.find_target()]
            and "assassin" in self.cards):
            return ("assassinate " + self.find_target())
        
        #Money making
        if "duke" in self.cards:
            return "tax"
        
        if ("captain" in self.cards and
            "steal_blocker" not in self.assumed_opponent_cards
            [self.find_target()]):
            return "steal " + self.find_target()
        
        duke_about = False
        for i in self.assumed_opponent_cards.keys():
            if "duke" in self.assumed_opponent_cards[i]:
                duke_about = True
        if not duke_about:
            return "foreign_aid"
        
        if self.debug:
            print("nothing for it ... income")
        return "income"
            
        
    def cheese_turn(self):
        #Rule Coup
        if self.coins >= 10:
            return ("coup " + self.find_target())
        
        #Captain Cheese
        if self.cards.count("captain") == 2:
            print("captain force")
            self.force_steal = True
        
        #Assassinate
        if (self.coins >= 3 and "contessa" not in 
            self.assumed_opponent_cards[self.find_target()]):
            self.force_challenge = True
            return ("assassinate " + self.find_target())
        
        #Money Making
        if self.force_steal:
            self.force_challenge = True
            return "steal " + self.find_target()
        
        if "duke" in self.cards:
            return "tax"
        
        duke_about = False
        for i in self.assumed_opponent_cards.keys():
            if "duke" in self.assumed_opponent_cards[i]:
                duke_about = True
        if not duke_about:
            return "foreign_aid"
        
        if "ambassador" in self.cards:
            self.exchanged == True
            return "exchange"
        #Tardout
        return "income"
        
    def optimal_turn(self):
        if self.coins >= 10:
            return ("coup " + self.find_target())
        
        if self.coins >= 7:
            return ("coup " + self.find_target())
        
        #Assassinate
        if (self.coins >= 3 and "contessa" not in 
            self.assumed_opponent_cards[self.find_target()]
            and "assassin" in self.cards and (random.randint(0,10)>3)):
            return ("assassinate " + self.find_target())
        
        #Money making
        if "duke" in self.cards:
            return "tax"
        
        if ("captain" in self.cards and
            "steal_blocker" not in self.assumed_opponent_cards
            [self.find_target()]):
            return "steal " + self.find_target()
        
        return "tax"
        

    def alpha_cb(self):
        actor = self.la()["actor"]
        action = self.la()["action"]
        target = self.la()["target"]
        blocker = self.la()["blocker"]
        self.basic_cb()
        if (target == self.name and action in Couptils.blockable_actions and 
            random.randint(1,2) == 1 and blocker == None):
            return "block"            
        if random.randint(1,3) == 1 and action in Couptils.challengeable_actions:
            return "challenge"
        return "pass"
 
    def bravo_cb(self):
        actor = self.la()["actor"]
        action = self.la()["action"]
        target = self.la()["target"]
        blocker = self.la()["blocker"]
        self.basic_cb()
        if target == self.name and action == "steal":
            return "challenge"
        return "pass"
        

    def charlie_cb(self):
        actor = self.la()["actor"]
        action = self.la()["action"]
        target = self.la()["target"]
        blocker = self.la()["blocker"]
        self.basic_cb()
        if action == "tax" and "duke" in self.cards:
            return "challenge"
        if action == "foreign_aid" and blocker == None:
            return "block"
        return "pass"
        
    def basic_cb(self):
        if self.la()["target"] == self.name and self.honest_block() != None:
            self.honest_block()
        if self.la()["blocker"] != None and self.la()["actor"] == self.name:
            if self.force_challenge:
                self.force_challenge = False
                print("challenge forced")
                return "challenge"
        actor = self.la()["actor"]
        action = self.la()["action"]
        target = self.la()["target"]
        blocker = self.la()["blocker"]
        if action == "foreign_aid" and "duke" in self.cards and blocker == None:
            return "block"
        if actor != self.name and (self.cards.count(self.repped_card(action)) == 2):
            return "challenge"
        if action == "assassinate" and target == self.name and len(self.cards) == 1:
            return "block"
        
        
    def repped_card(self,action):
        for i in Couptils.card_abilities:
            if action in Couptils.card_abilities[i]:
                return i

    def init_modes(self):
        self.assumed_opponent_cards = {}
        self.known_cards = self.cards.copy()
        self.force_steal = False
        self.exchanged = False
        for i in self.opponents:
            self.assumed_opponent_cards[i] = []
            
        self.turn_mode = self.winrate_simple_turn_mode()
        self.cb_mode = self.winrate_simple_cb_mode()
       
    
    def honest_block(self):
        action = self.la()["action"]
        if action in Couptils.blockable_actions:
            if ("block_" + action) in Couptils.card_abilities[self.cards[0]]:
                return "block"
            elif len(self.cards) == 2:
                if ("block_" + action) in Couptils.card_abilities[self.cards[1]]:
                    return "block"
                
    def least_valuable_card(self):
        #return duplicate if available
        for card in self.card_types:
            if self.cards.count(card) > 1:
                return card
            pass
        
        #return first card (priority sorted from lowest to highest)
        if self.turn_mode == "honest":
            my_priority = ["ambassador","assassin","contessa","captain","duke"]
        if self.turn_mode == "cheese":
            my_priority = ["ambassador","duke","contessa","captain","assassin"]
        if self.turn_mode == "optimal":
            my_priority = ["ambassador","assassin","captain","contessa","duke"]
        for card in my_priority:
            if card in self.cards:
                return card
        print("least_valuable_card tardout")
        return self.cards[0]    
    
    def discard(self):
        return self.least_valuable_card()
    
    def placeback(self):
        return self.least_valuable_card()
    
    def challenged(self):
        if self.search_to_win_challenge() in self.cards:
            return self.search_to_win_challenge()
        return self.least_valuable_card()
            
    def reflect(self):
        if self.debug:
            print(self.la())
        actor = self.la()["actor"]
        action = self.la()["action"]
        target = self.la()["target"]
        blocker = self.la()["blocker"]
        challenger = self.la()["challenger"]
        c_win = self.la()["challenger_win"]
        discard_a = self.la()["discard_a"]
        discard_c = self.la()["discard_c"]
        if self.debug:
            print("reflect", actor, action, target, blocker, challenger)
        #See if there are any dukes out there
        if actor != self.name and action == "tax":
            self.assumed_opponent_cards[actor].append("duke")
        #See if any of our actions were blocked and not challenged        
        if actor == self.name:
            if blocker != None and challenger == None:
                if action == "assassinate":
                    self.assumed_opponent_cards[blocker].append("contessa")
                if action == "foreign_aid":
                    self.assumed_opponent_cards[blocker].append("duke")
                if action == "steal":
                    self.assumed_opponent_cards[blocker].append("steal_blocker")
        
        # someone else discarded a card from an action
        if discard_a != {} and target != self.name:
            self.known_cards.append(discard_a[target])
            if discard_a[target] in self.assumed_opponent_cards[target]:
                self.assumed_opponent_cards[target].remove(discard_a[target])
                
        # someone discarded due to a challenge
        if discard_c != {}:
            # I got challenged and...
            if actor == self.name:
                # I won
                if c_win == False:
                    self.known_cards.append(discard_c[challenger])
                    if discard_c[challenger] in self.assumed_opponent_cards[challenger]:
                        self.assumed_opponent_cards[challenger].remove(discard_c[challenger])
                # I lost
                if c_win == True:
                    # I lost a card and got no information
                    pass
            
            # I challenged and...
            if challenger == self.name:
                # I won
                if c_win:
                    self.known_cards.append(discard_c[actor])
                    if discard_c[actor] in self.assumed_opponent_cards[actor]:
                        self.assumed_opponent_cards[actor].remove(discard_c[actor])
                # I lost
                if not c_win:
                    # I lost a card and got no information
                    pass
            # FFA moment, I wasn't involved
            if actor != self.name and challenger != self.name:
                if not c_win:
                    self.known_cards.append(discard_c[actor])
                    if discard_c[actor] in self.assumed_opponent_cards[actor]:
                        self.assumed_opponent_cards[actor].remove(discard_c[actor])
                else:
                    self.known_cards.append(discard_c[challenger])
                    if discard_c[challenger] in self.assumed_opponent_cards[challenger]:
                        self.assumed_opponent_cards[challenger].remove(discard_c[challenger])

    def winrate_simple_turn_mode(self):
        oppo = str(self.opponents)
        if oppo not in self.memory:
            return "honest"
        games1 = 1 + (self.memory[oppo]["simple_matrix"]["wins"]["honest"]+
                  self.memory[oppo]["simple_matrix"]["losses"]["honest"])
        games2 = 1 + (self.memory[oppo]["simple_matrix"]["wins"]["cheese"]+
                  self.memory[oppo]["simple_matrix"]["losses"]["cheese"])
        games3 = 1 + (self.memory[oppo]["simple_matrix"]["wins"]["optimal"]+
                  self.memory[oppo]["simple_matrix"]["losses"]["optimal"])
        wr1 = self.memory[oppo]["simple_matrix"]["wins"]["honest"]/games1
        wr2 = self.memory[oppo]["simple_matrix"]["wins"]["cheese"]/games2
        wr3 = self.memory[oppo]["simple_matrix"]["wins"]["optimal"]/games3
        if games1+games2+games3 < 50:
            guess = random.randint(1,3)
            if guess == 1:
                return "honest"
            if guess == 2:
                return "cheese"
            if guess == 3:
                return "optimal"
            
        if wr1 >= wr2 and wr1 >= wr3:
            return "honest"
        if wr2 >= wr1 and wr2 >= wr3:
            return "cheese"
        if wr3 >= wr2 and wr3 >= wr1:
            return "optimal"
        
    def winrate_simple_cb_mode(self):
        oppo = str(self.opponents)
        if oppo not in self.memory:
            return "alpha"
        games1 = 1 + (self.memory[oppo]["simple_matrix"]["wins"]["alpha"]+
                  self.memory[oppo]["simple_matrix"]["losses"]["alpha"])
        games2 = 1 + (self.memory[oppo]["simple_matrix"]["wins"]["bravo"]+
                  self.memory[oppo]["simple_matrix"]["losses"]["bravo"])
        games3 = 1 + (self.memory[oppo]["simple_matrix"]["wins"]["charlie"]+
                  self.memory[oppo]["simple_matrix"]["losses"]["charlie"])
        wr1 = self.memory[oppo]["simple_matrix"]["wins"]["alpha"]/games1
        wr2 = self.memory[oppo]["simple_matrix"]["wins"]["bravo"]/games2
        wr3 = self.memory[oppo]["simple_matrix"]["wins"]["charlie"]/games3
        if games1+games2+games3 < 50:
            guess = random.randint(1,3)
            if guess == 1:
                return "alpha"
            if guess == 2:
                return "bravo"
            if guess == 3:
                return "charlie"
        if wr1 >= wr2 and wr1 >= wr3:
            return "alpha"
        if wr2 >= wr1 and wr2 >= wr3:
            return "bravo"
        if wr3 >= wr2 and wr3 >= wr1:
            return "charlie"
        
    def search_to_win_challenge(self):
        action = self.la()["action"]
        if (action in Couptils.card_abilities["duke"]
            and "duke" in self.cards):
            return "duke"
        if (action in Couptils.card_abilities["ambassador"]
            and "ambassador" in self.cards):
            return "ambassador"
        if (action in Couptils.card_abilities["assassin"]
            and "assassin" in self.cards):
            return "assassin"
        if (action in Couptils.card_abilities["captain"]
            and "captain" in self.cards):
            return "captain"
        if (action in Couptils.card_abilities["contessa"]
            and "contessa" in self.cards):
            return "contessa"
        if self.debug:
            print("Error at search to win challenge")
    
    def find_target(self,action="coup"):
        self.opponents = Couptils.get_players_from_log(self.log)
        self.opponents.remove(self.name)
        self.smart_log()
        players = self.game_dict["players"]
        threat_level = []
        for player in self.opponents:
            if self.name == player:
                threat_level.append(-1)
            else:
                threat_level.append(players[player]["coins"] + 
                                    5*players[player]["cards"])
        return self.opponents[threat_level.index(max(threat_level))]
    
    def least_valuable_card(self):
        return self.cards[0]
    
    def receive(self,message):
        self.log += message
        self.log += "\n"
        if message[0:7] == "winner:":
            #SHUT DOWN THE BOT
            if self.name == message.split(" ")[1]:
                self.iwin = True
            else:
                self.iwin = False
            self.memorize_results()
            self.open_data_write(self.memory)
        elif message[0:8] == "players:":
            #INIT THE BOT
            self.log = ""
            self.log += message
            self.log += "\n"
            self.open_data_read()
            self.find_target()
            self.init_modes()
        else:
            if self.la() != None:
                if message.split(" ")[1] in Couptils.turn_actions:
                    self.reflect()
            self.smart_log()
            # self.modify_memory()
    
    def show(self,show_cards=False):
        print("player: " + self.name)
        if show_cards == True:
            print("cards: " + str(self.cards))
        else:
            print("cards: " + str(len(self.cards)))
        print("coins: " + str(self.coins))
        
    def la(self): # last_action
        try:
            return self.game_dict["this_turn"]
        except:
            if self.debug:
                print("Error at last_action:", self.game_dict)
                print("Turn Number:", self.turns_taken_by_me)
                print("Called empty game_dict")
            return {"action": "none"}
        
    def smart_log(self):
        try:
            self.game_dict.clear()
            self.game_dict = Couptils.turn_list_to_game_dict(
                Couptils.get_players_from_log(self.log),
                Couptils.log_to_turn_list(self.log))
        except:
            if self.debug:
                print("Error at smart_log:", self.log)    
    def memorize_results(self):
        self.opponents.sort()
        if str(self.opponents) not in self.memory:
            self.memory[str(self.opponents)] = {"simple_matrix":
              {"wins":{"honest": 0,"cheese": 0,"optimal": 0,
                       "alpha": 0,"bravo": 0,"charlie": 0},
              "losses":{"honest": 0,"cheese": 0,"optimal": 0,
                        "alpha": 0,"bravo": 0,"charlie": 0}},
             "nested_matrix": 
                 {"wins": {"honest":{"alpha": 0,"bravo": 0,"charlie": 0},
                  "cheese":{"alpha": 0,"bravo": 0,"charlie": 0},
                  "optimal":{"alpha": 0,"bravo": 0,"charlie": 0}},
                 "losses": {"honest":{"alpha": 0,"bravo": 0,"charlie": 0},
                  "cheese":{"alpha": 0,"bravo": 0,"charlie": 0},
                  "optimal":{"alpha": 0,"bravo": 0,"charlie": 0}}}}
        if self.iwin:
            result = "wins"
        else:
            result = "losses"
            
        if self.force_steal:
            print("Win:", self.iwin)
        
        self.memory[str(self.opponents)]["simple_matrix"][
            result][self.turn_mode] += 1
        self.memory[str(self.opponents)]["simple_matrix"][
            result][self.cb_mode] += 1
        self.memory[str(self.opponents)]["nested_matrix"][
            result][self.turn_mode][self.cb_mode] += 1
            
            
    def open_data_read(self):
        try:
            loadfile = open("flyswatter.pkl","rb")
            mydata = pickle.load(loadfile)
            loadfile.close()
        except:
            newfile = open("flyswatter.pkl","x")
            newfile.close()
            loadfile = open("flyswatter.pkl","wb")
            mydata = {}
            pickle.dump(mydata, loadfile)
            loadfile.close()
        self.game_dict = {}
        self.memory = mydata
        self.turns_taken_by_me = 0
        self.nut_size = random.randint(1,10)

    def open_data_write(self,newdata):
        loadfile = open("flyswatter.pkl","wb")
        pickle.dump(newdata, loadfile)
        loadfile.close()
        
    def forget(self):
        self.open_data_write({})
        print("flyswatter has cleared his memory")