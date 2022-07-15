#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 17:28:06 2022

@author: dsmishler
"""

class Player:
    def __init__(self, name):
        self.name = name
        self.log = ""
        self.coins = 0
        self.cards = []
    
    def react(self, hint):
        if hint == "turn":
            reaction = input("your turn: ")
            while reaction == "show":
                print("your cards: ", self.cards)
                print("your coins: ", self.coins)
                print("so far:")
                print(self.log)
                reaction = input("your turn: ")
            return reaction
        elif hint == "discard":
            reaction = input("discard: ")
            while reaction == "show":
                print("you must discard")
                print("your hand:", self.cards)
                reaction = input("discard: ")
            return reaction
        elif hint == "placeback":
            reaction = input("placeback: ")
            while reaction == "show":
                print("you must placeback from your exchange")
                print("your hand:", self.cards)
                reaction = input("placeback: ")
            return reaction
        elif hint == "challenged":
            reaction = input("challenged: ")
            while reaction == "show":
                print("you must choose a card to respond to the challenge")
                print("your hand:", self.cards)
                reaction = input("challenged: ")
            return reaction
        elif hint == "cb?":
            reaction = input("challenge or block?: ")
            while reaction == "show":
                print("you must choose to challenge, block, or pass.")
                print("your hand:", self.cards)
                reaction = input("challenge or block?: ")
            return reaction
        else:
            print("uknown hint '%s'" % hint)
            return "?"
                
    def receive(self, message):
        self.log += message
        self.log += "\n"
        print(message)

    def show(self, show_cards = False):
        print("player", self.name)
        if show_cards:
            print("cards:", self.cards)
        else:
            print("cards:", len(self.cards))
        print("coins:", self.coins)

