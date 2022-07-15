# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 11:11:12 2022

@author: Daniel Mishler
"""

import random

class Player_Trey:
    def __init__(self, name):
        self.name = name
        self.log = ""
        self.coins = 0
        self.cards = []

    
    def react(self, hint):
        if hint == "turn":
            if self.coins < 7:
                return "income"
            else:
                target = self.find_active_target()
                return "coup" + " " + target
        elif hint in ["discard", "placeback", "challenged"]:
            discard_me = self.cards[0]
            return discard_me
        elif hint == "cb?":
            return "pass"
        else:
            print("error: unknown hint for reaction!")
            return "?"
    
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
        players_array = double_list(players_array)
        
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


# as an aside, I know that `mylist` is a mutable, but I'm returning by value
# anyway to sweep that under the rug
def double_list(mylist):
    orig_len = len(mylist)
    for i in range(orig_len):
        mylist.append(mylist[i])
    return mylist