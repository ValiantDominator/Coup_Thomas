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
    def __init__(self,name="lazy_sullivan",debug=True):
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
        if self.coins >= 7:
            return ("coup " + self.find_target())
        return "tax"
    
    def discard(self):
        return self.cards[0]
    
    def placeback(self):
        return self.cards[0]
    
    def challenged(self):
        action = self.last_action()["action"]
        card_to_rep = self.search_to_win_challenge(action)
        if card_to_rep in self.cards:
            return card_to_rep
        else:
            return self.cards[0]
            
    def cb(self):
        try:
            if self.last_action()["actor"] != self.name:
                if self.last_action()["action"] in Couptils.challengeable_actions:
                    return self.decide_to_challenge()
                return "pass"
            return "pass"
        except:
            if self.debug:
                print("cb? error:", self.last_action())
                print("Turn Number:", self.turns_taken_by_me)
            return "pass"
        else:
            return "pass"

    def decide_to_challenge(self):
        try:
            player = self.last_action()["actor"]
            action = self.last_action()["action"]
            lies = self.memory["challenge_success"][player][action]["success_total"]
            attempts = self.memory["challenge_success"][player][action]["attempt_total"]
            lie_rate = lies/attempts
            if self.debug:
                print("Lie rate for", player, "doing", action, ":", lie_rate)
            if lie_rate > 0.50:
                return "challenge"
            else:
                if lie_rate*100 < random.randint(0, 50):
                    return "pass"
                else:
                    return "challenge"
        except:
            if self.debug:
                print("New situation:", player, "doing", action)
            return "challenge"

    def search_to_win_challenge(self,action):
        if action in Couptils.card_abilities["duke"]:
            return "duke"
        if action in Couptils.card_abilities["ambassador"]:
            return "ambassador"
        if action in Couptils.card_abilities["assassin"]:
            return "assassin"
        if action in Couptils.card_abilities["captain"]:
            return "captain"
        if action in Couptils.card_abilities["contessa"]:
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
    
    def open_data_write(self,newdata):
        loadfile = open("lazy_sullivan.pkl","wb")
        pickle.dump(newdata, loadfile)
        loadfile.close()
        
    def forget_memory(self):
        self.open_data_write({})
        print("lazy_sullivan memory forgot")