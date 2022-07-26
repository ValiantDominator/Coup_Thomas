#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 11:47:46 2022

@author: dsmishler
"""

import random
import Couptils
import pickle

class Player_JoeyD:
    def __init__(self, name="joeyd"):
        self.name = name
        self.log = ""
        self.coins = 0
        self.cards = []
        try:
            memory_file = open("joeyd_memory.pkl", "rb")
            self.memory = pickle.load(memory_file)
            memory_file.close()
        except FileNotFoundError:
            self.memory = {}
            self.memory["games"] = []
            self.memory["opponents"] = {}
        if(random.randint(0,9) == 0):
            self.mode = "cannon"
        else:
            self.mode = "normal"
    
    def react(self, hint):
        game_dict = Couptils.log_to_game_dict(self.log)
        if hint == "turn":
            # Can I assassinate or coup?
            target = self.find_active_target(game_dict)

            if "assassin" in self.cards:
                if self.coins >= 3:
                    return "assassinate " + target
            
            if self.coins >= 7:
                return "coup " + target
            
            # What's the money-making strategy?
            if "duke" in self.cards:
                return "tax"
            
            
            
            return "income"
            
            
        elif hint in ["discard", "placeback"]:
            discard_me = self.cards[0]
            return discard_me
        
        elif hint == "challenged":
            if game_dict["this_turn"]["blocker"] is None:
                action = game_dict["this_turn"]["action"]
            else:
                action = "block_"+game_dict["this_turn"]["action"]
            for card in self.cards:
                if action in Couptils.card_abilities[card]:
                    return card
            return self.cards[0]
        
        elif hint == "cb?":
            # decide whether to block
            if game_dict["this_turn"]["blocker"] is None:
                action = game_dict["this_turn"]["action"]
                target = game_dict["this_turn"]["target"]
                if action == "steal" and target == self.name:
                    if "captain" in self.cards or "ambassador" in self.cards:
                        return "block"
                if action == "assassinate" and target == self.name:
                    if "contessa" in self.cards:
                        return "block"
                if action == "foreign_aid":
                    if "duke" in self.cards:
                        return "block"
                
                
            return "pass"
        else:
            print("error: unknown hint for reaction!")
            return "?"
    
    # Look at the log, and find a player who is still active for a target
    # Perhaps for stealing, coup-ing, or assassinating
    def find_active_target(self, game_dict):
        players_array = list(game_dict["players"].keys())
        random.shuffle(players_array)
        for player in players_array:
            if player == self.name:
                continue
            if game_dict["players"][player]["cards"] != 0:
                target = player
                break
        
        return target
                
    def receive(self, message):
        self.log += message
        self.log += "\n"
        if message[:7] == "winner:":
            game_dict = Couptils.log_to_game_dict(self.log)
            self.memory["games"].append(game_dict)
            
            # Add all the players to memory if they're not already there.
            for player in game_dict["players"].keys():
                if player == self.name:
                    continue
                try:
                    self.memory["opponents"][player]
                except KeyError:
                    self.memory["opponents"][player] = {
                        "challenged" : {},
                        "turn1": {"total": 0}
                    }
            
            for turn in game_dict["turns"]:
                # For all the challenges
                if turn["challenger"] is not None:
                    # who was challenged? The blocker or the actor?
                    if turn["blocker"] is not None:
                        challenged_player = turn["blocker"]
                        challenged_action = "block_"+turn["action"]
                    else:
                        challenged_player = turn["actor"]
                        challenged_action = turn["action"]
                    
                    if challenged_player == self.name:
                        continue # just focus on opponents for now
                    
                    
                    # Now add in the data that the player was challenged doing
                    # this. Add a new category if need be.
                    
                    # pcd: player challenged data
                    pcd = (
                     self.memory["opponents"][challenged_player]["challenged"])
                    
                    try:
                        pcd[challenged_action]
                    except KeyError:
                        pcd[challenged_action] = {
                            "total": 0, # Total times challenged doing this
                            "won": 0    # times won while challenged doing this
                            }
                    
                    pcd[challenged_action]["total"] += 1
                    if turn["challenger_win"] == False: # Challenger lost
                        pcd[challenged_action]["won"] += 1 # Challenged won
                    
            
            
            memory_file = open("joeyd_memory.pkl", "wb")
            pickle.dump(self.memory, memory_file)
            memory_file.close()

    def show(self, show_cards = False):
        print("player", self.name)
        if show_cards:
            print("cards:", self.cards)
        else:
            print("cards:", len(self.cards))
        print("coins:", self.coins)
    



if __name__ == '__main__':
    memory_file = open("joeyd_memory.pkl", "rb")
    joeyd_memory = pickle.load(memory_file)
    memory_file.close()
    
    print(joeyd_memory["opponents"])