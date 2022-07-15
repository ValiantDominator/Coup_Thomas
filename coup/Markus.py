# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 20:52:00 2022

@author: Daniel Mishler
"""
import random

card_abilities = {
    "duke" :       ["tax", "block_foreign_aid"],
    "captain" :    ["steal", "block_steal"],
    "assassin" :   ["assassinate"],
    "contessa" :   ["block_assassinate"],
    "ambassador" : ["exchange", "block_steal"]
    }

class Player_Markus:
    def __init__(self, name="markus"):
        self.name = name
        self.log = ""
        self.coins = 0
        self.cards = []
    
    def react(self, hint):
        if hint == "turn":
            victim = self.find_active_target()
            if self.coins < 7:
                return "steal " + victim
            else:
                return "coup " + victim
        elif hint in ["discard", "placeback"]:
            for card in self.cards:
                if card != "captain":
                    return card
            # if nothing else works...
            return "captain"
        elif hint == "challenged":
            log_lines = self.log.split('\n')
            # -1 would be the last line,
            # but the last line is empty (we add a newline every time)
            # and the second to last line is the thing that we are responding
            # to (the challenge).
            # so we want -3.
            last_line = log_lines[-3]
            action = last_line.split()[1]
            # This is overkill for markus, because all markus should be doing
            # is showing you the captain when you challenge his steal
            # But this will be good for Beef.
            for card in self.cards:
                if action in card_abilities[card]:
                    return card
            for card in self.cards:
                if card != "captain":
                    return card
            return "captain"
            
        elif hint == "cb?":
            log_lines = self.log.split('\n')
            last_line = log_lines[-2]
            action = last_line.split()[1]
            
            if action in ["steal", "block_steal", "exchange"]:
                return "challenge"
            
            
            return "pass"
        return

    # Look at the log, and find a player who is still active for a target
    # Perhaps for stealing, coup-ing, or assassinating
    def find_active_target(self):
        # Find all the players
        first_log_line = self.log.split('\n')[0]
        start_i = first_log_line.find('[')
        end_i = first_log_line.find(']')
        players_string = first_log_line[start_i+1:end_i]
        players_array = players_string.split(", ")
        # Remove myself
        players_array.remove(self.name)
        
        # You might entertain using a dictionary here: I will just double
        # the list
        original_len = len(players_array)
        for i in range(original_len):
            players_array.append(players_array[i])
        
        # Find the last player that acted
        for line in self.log.split('\n'):
            if line == "":
                continue # ignore the last (empty) line
                # the difference between break and continue here is simply
                # that continue will end the iteration of the for loop, and
                # instead of being *guaranteed* to exit the for loop, will
                # enter the next iteration if there is one to do.
            player = line.split()[0]
            action = line.split()[1]
            if action == "discard" and player != self.name:
                players_array.remove(player)
        
        # You don't need to shuffle, but I will
        random.shuffle(players_array)
        
        target = players_array[0]
        return target

    def receive(self, message):
        self.log += message
        self.log += "\n"
    
    def show(self, show_cards = False):
        print("player", self.name)
        if show_cards:
            print("cards:", self.cards)
        else:
            print("cards:", len(self.cards))
        print("coins:", self.coins)