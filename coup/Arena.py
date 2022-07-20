# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 11:09:54 2022

@author: Daniel Mishler
"""

import Coup
import Markus
import Trey
import Beef
import lazy_sullivan

gm = Coup.Game_Master()

trey = Trey.Player_Trey("trey")
boo = Trey.Player_Trey("boo")
markus = Markus.Player_Markus()
beef = Beef.Player_Beef()
lazy_sullivan = lazy_sullivan.lsPlayer()

wincounts_markus = 0
wincounts_trey = 0
wincounts_boo = 0
wincounts_beef = 0
wincounts_lazy_sullivan = 0

for i in range(1000):
    gm.game([beef, lazy_sullivan], fname = "lazy_sullivantest.coup")
    gamefile = open("lazy_sullivantest.coup")
    lines = gamefile.read().split('\n')
    winnerline = lines[-2]
    winner = winnerline.split()[1]
    if winner == "markus":
        wincounts_markus += 1
    elif winner == "trey":
        wincounts_trey += 1
    elif winner == "boo":
        wincounts_boo += 1
    elif winner == "beef":
        wincounts_beef += 1
    elif winner == "lazy_sullivan":
        wincounts_lazy_sullivan += 1
    gamefile.close()
    
# print("markus wins", wincounts_markus, "games")
# print("trey wins", wincounts_trey, "games")
# print("boo wins", wincounts_boo, "games")
print("beef wins", wincounts_beef, "games")
print("lazy_sullivan wins", wincounts_lazy_sullivan, "games")