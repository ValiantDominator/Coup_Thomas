# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:12:44 2022

@author: Daniel Mishler
"""
import pickle
# Problem 1
# Open the pickled file 'test.pkl'.
# What is its data type?
# What does it say?
loadfile = open("test.pkl","rb")
mydata = pickle.load(loadfile)
loadfile.close()
print(mydata)
print(mydata['never'][0])

# Problem 2
# Use my files:
    # human_player
    # Coup
    # Markus
    # Beef
# Play enough 1v1 games against Markus until you can figure out a way
# that you'll be confident you can win more than half the time. Don't
# worry about coding it quite yet. Just see if *you* can understand the
# strategy in *your* head before you try to teach Python to do it


# Problem 3
# Play enough 1v1 games against Beef until you can figure out a way
# that you'll be confident you can win more than half the time.



# Problem 4
# Write a coup agent that is capable of beating Beef and Markus at least
# 1/3 of the time. Name your coup agent `Player_*`, where * is a name of your
# choice. Example: `Player_Anton`. You might end up making many, many such
# agents. Just make one that has a chance to win against Markus and Beef.
# And it better beat Trey 100% of the time.


# Problem 5
# (this will be a work in progress for all this week and bleed into next week.)
# You need to figure out a way to record data about your opponents with respect
# to their name. In other words, you need to figure out a way that you can
# record, between games, the behavior of a player based on their name.
# I recommend your Coup Agent should do the following things:
    # Every time on boot, it loads a pickle file that contains a dictionary
    # of history
    # Every time it receives "winner: ..." from receive, it will save the
    # work it's done on its history dictionary back to the pickle file

# Goal: Beat Markus and Beef both more than 1/2 of the time, but not by
# just *knowing* their behavior, instead by *adapting* to their strategies.
# In other words, if I randomized their names, you should still eventually
# learn to beat both.