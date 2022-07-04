#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 17:28:06 2022

@author: dsmishler
"""

import random

class Player:
    def __init__(self, name):
        self.name = name
        self.log = ""
        self.coins = 0
        self.cards = []
    def turn(self):
        print("your cards: ", self.cards)
        print("your coins: ", self.coins)
        print("so far:")
        print(self.log)
        action = input("your turn: ")
        return action
    
    def react(self, hint):
        if hint == "turn":
            return self.turn()
        # else
        print("reaction time: hint ", hint)
        print("your hand:", self.cards)
        reaction = input("reaction: ")
        return reaction
        
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
        print(message)

    def show_all(self):
        print("player", self.name)
        print("cards:", self.cards)
        print("coins:", self.coins)


def double_list(mylist):
    orig_len = len(mylist)
    for i in range(orig_len):
        mylist.append(mylist[i])
    return mylist