# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 16:22:16 2022

@author: Val
"""

'''
lazy_sullivan
'''
import random
import pickle
import Couptils

class lsPlayer:
    def __init__(self,name="lazy_sullivan",debug=False):
        self.name = name
        self.cards = []
        self.coins = 0
        self.opponents = []
        self.log = ""
        self.turns_taken_by_me = 0
        self.game_dict = {}
        self.debug = debug
        self.memory = {}
        self.open_data_read()
        self.nut_size = 0
        self.tried_swap = False
        self.card_types = ["duke","captain","assassin","ambassador","contessa"]
        
    def react(self,hint):
        if hint == "turn":
            return self.turn()
        elif hint == "discard":
            return self.discard()
        elif hint == "placeback":
            return self.placeback()
        elif hint == "challenged":
            return self.challenged()
        elif hint == "cb?":
            return self.cb()
        
        
        
    def turn(self):
        self.turns_taken_by_me += 1
        balls = self.nut_size
        #Mandatory actions
        if self.coins >= 10:
            return ("coup " + self.find_target())
        
        #Predictable actions
        if self.coins >= 7 and len(self.opponents) == 1:
            return ("coup " + self.find_target())
        
        #Semi-predictable
        if self.turns_taken_by_me == 1:
            if "duke" in self.cards:
                return "tax"
            if self.lie_rate(self.name,"tax")<(0.05*balls):
                return "tax"
        
        if self.coins >= 3 and not self.assassin_fail:
            if "assassin" in self.cards:
                return ("assassinate " + self.find_target())
            if self.lie_rate(self.name,"assassinate")<(0.05*balls):
                return ("assaasinate " + self.find_target())
        
        if self.tried_swap == False:
            if "ambassador" in self.cards:
                self.tried_swap = True
                return "exchange"
            if self.lie_rate(self.name,"exchange")<(0.07*balls):
                self.tried_swap = True
                return "exchange"
        
        if balls > 6 and "captain" in self.cards and not self.steal_fail:
            return ("steal " + self.find_target())
        
        if "duke" in self.cards:
            return "tax"
        if balls > 5:
            return "tax"
        
        if "captain" in self.cards and not self.steal_fail:
            return ("steal " + self.find_target())
        
        return "income"
        
    
    def discard(self):
        return self.least_valuable_card()
    
    def placeback(self):
        return self.least_valuable_card()
    
    def challenged(self):
        self.smart_log()
        action = self.last_action()["action"]
        actor = self.last_action()["actor"]
        target = self.last_action()["target"]
        if self.name == actor:
            card_to_rep = self.search_to_win_challenge(action)
            if self.debug:
                print("\n","challenged on", [action])
                print("my cards", self.cards)
                print("represent my", [card_to_rep])
            return card_to_rep
        elif self.name == target:
            card_to_rep = self.search_to_win_challenge("block_"+action)
            if self.debug:
                print("\n","challenged on", ["block_"+action])
                print("my cards", self.cards)
                print("represent my", [card_to_rep])
            return card_to_rep
        return self.least_valuable_card()
            
    def cb(self):
        action = self.last_action()["action"]
        actor = self.last_action()["actor"]
        target = self.last_action()["target"]
        try:
            if actor != self.name:
                if (action in Couptils.blockable_actions 
                      and target == self.name):
                    if self.block_safe() == "block":
                        return self.block_safe()
                if len(self.cards) == 1 and action == "assassinate":
                    return "challenge"
                if self.debug:
                    print("\n",self.cards)
                    print(action)
                    print("Can't block, checking to challenge")
                if self.last_action()["action"] in Couptils.challengeable_actions:
                    return self.decide_to_challenge()
                        
                return "pass"
            return "pass"
        
        except:
            if self.debug:
                print("cb? error:", self.last_action())
                print("Turn Number:", self.turns_taken_by_me)
            return "pass"
        
        return "pass"

    def least_valuable_card(self):
        #return duplicate if available
        for card in self.card_types:
            if self.cards.count(card) > 1:
                return card
            pass
        
        #return first card (priority sorted from lowest to highest)
        my_priority = ["ambassador","captain","duke","assassin","contessa"]
        for card in my_priority:
            if card in self.cards:
                return card
        print("least_valuable_card tardout")
        return self.cards[0]
        
    
    def decide_to_challenge(self):
        try:
            player = self.last_action()["actor"]
            action = self.last_action()["action"]
            lies = self.memory["challenge_success"][
                player][action]["success_total"]
            attempts = self.memory["challenge_success"][
                player][action]["attempt_total"]
            lie_rate = lies/attempts
            if attempts < 25:
                lie_rate = 0.33
            if self.debug:
                print("Lie rate for", player, "doing", action, ":", lie_rate)
            if lie_rate > 0.33:
                if self.debug:
                    print("decided to challenge on account of lie_rate >33%")
                return "challenge"
            else:
                challenge_roll = random.randint(0, 33)
                if lie_rate*100 < challenge_roll:
                    if self.debug:
                        print("decided to pass",lie_rate,"<",challenge_roll)
                    if action == "block_assassinate":
                        print("assassin fail")
                        self.assassin_fail = True
                    if action == "block_steal":
                        print("steal fail")
                        self.steal_fail = True
                    return "pass"
                else:
                    if self.debug:
                        print("decided to challenge",lie_rate,">",challenge_roll)
                    return "challenge"
        except:
            if self.debug:
                print("New situation:", player, "doing", action)
            return "challenge"
    
    def block_safe(self):
        action = self.last_action()["action"]
        if action in Couptils.blockable_actions:
            if ("block_" + action) in Couptils.card_abilities[self.cards[0]]:
                return "block"
            elif len(self.cards) == 2:
                if ("block_" + action) in Couptils.card_abilities[self.cards[1]]:
                    return "block"
        return "pass"
    
    def block_unsafe(self):
        player = self.last_action()["actor"]
        action = self.last_action()["action"]
        block = ("block_" + action)
        myattempts = self.memory["challenge_success"][
            self.name][block]["attempt_total"]
        mylies = self.memory["challenge_success"][
            self.name][block]["success_total"]
        lie_rate = mylies/myattempts
        if len(self.cards == 1):
            lie_rate += -0.2
        
        if len(self.cards) == 1 and action == "assassinate":
            return "block"
        
        if lie_rate*100 < random.randint(0,50):
            return "block"
        
        return "pass"

    def search_to_win_challenge(self,action):
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
    
    def last_action(self):
        try:
            return self.game_dict["this_turn"]
        except:
            if self.debug:
                print("Error at last_action:", self.game_dict)
                print("Turn Number:", self.turns_taken_by_me)
                print("Called empty game_dict")
            return {"action": "none"}
    
    def find_target(self,action="coup"):
        self.opponents = Couptils.get_players_from_log(self.log)
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
        
    def smart_log(self):
        try:
            self.game_dict.clear()
            self.game_dict = Couptils.turn_list_to_game_dict(
                Couptils.get_players_from_log(self.log),
                Couptils.log_to_turn_list(self.log))
        except:
            if self.debug:
                print("Error at smart_log:", self.log)
    
    def receive(self,message):
        self.log += message
        self.log += "\n"
        if message[0:7] == "winner:":
            self.open_data_write(self.memory)
        elif message[0:8] == "players:":
            pass
        else:
            self.smart_log()
            self.modify_memory()
    
    def show(self,show_cards=False):
        print("player: " + self.name)
        if show_cards == True:
            print("cards: " + str(self.cards))
        else:
            print("cards: " + str(len(self.cards)))
        print("coins: " + str(self.coins))
        
    def lie_rate(self,player,action):
        try:
            lies = self.memory["challenge_success"][
                player][action]["success_total"]
            attempts = self.memory["challenge_success"][
                player][action]["attempt_total"]
            return lies/attempts
        except:
            return 0
    
    def modify_memory(self):
        last_action = self.last_action()
        #challenge memory
        if "challenge_success" in self.memory:
            pass
        else:
            self.memory = {"challenge_success":
                {last_action["actor"]:
                 {"tax":{"success_total" : 0,"attempt_total" : 0},
                  "steal":{"success_total" : 0,"attempt_total" : 0},
                  "exchange":{"success_total" : 0,"attempt_total" : 0},
                  "assassinate":{"success_total" : 0,"attempt_total" : 0},
                  "block_steal":{"success_total" : 0,"attempt_total" : 0},
                  "block_assassinate":{"success_total" : 0,"attempt_total" : 0},
                  "block_foreign_aid":{"success_total" : 0,"attempt_total" : 0}}}}
        if last_action["challenger_win"] != None:
            try: #modify memory
                self.memory["challenge_success"][last_action["actor"]][
                    last_action["action"]]["success_total"] += int(
                        last_action["challenger_win"])
                self.memory["challenge_success"][last_action["actor"]][
                    last_action["action"]]["attempt_total"] += 1
            except: #create memory
                print("New player encountered!")
                if self.debug:
                    print(self.memory)
                self.memory[
                    "challenge_success"].update(
                    {last_action["actor"]:
                     {"tax":{"success_total" : 0,"attempt_total" : 0},
                      "steal":{"success_total" : 0,"attempt_total" : 0},
                      "exchange":{"success_total" : 0,"attempt_total" : 0},
                      "assassinate":{"success_total" : 0,"attempt_total" : 0},
                      "block_steal":{"success_total" : 0,"attempt_total" : 0},
                      "block_assassinate":{"success_total" : 0,"attempt_total" : 0},
                      "block_foreign_aid":{"success_total" : 0,"attempt_total" : 0}}})

    def open_data_read(self):
        try:
            loadfile = open("lazy_sullivan.pkl","rb")
            mydata = pickle.load(loadfile)
            loadfile.close()
        except:
            newfile = open("lazy_sullivan.pkl","x")
            newfile.close()
            loadfile = open("lazy_sullivan.pkl","wb")
            mydata = {}
            pickle.dump(mydata, loadfile)
            loadfile.close()
        self.memory = mydata
        self.log = ""
        self.turns_taken_by_me = 0
        self.nut_size = random.randint(1,10)
        self.tried_swap = False
        self.steal_fail = False
        self.assassin_fail = False
    
    def open_data_write(self,newdata):
        loadfile = open("lazy_sullivan.pkl","wb")
        pickle.dump(newdata, loadfile)
        loadfile.close()
        
    def forget_memory(self):
        self.open_data_write({})
        print("lazy_sullivan has cleared his memory")