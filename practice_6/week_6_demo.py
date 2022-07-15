# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 20:56:22 2022

@author: Daniel Mishler
"""

import pickle


mystorage = {"key1": "hello my name is daniel", "key2": 3}


storefile = open("storefile.pkl", "wb")
# .pkl is the common pickle file extension
# wb is like write, but necessary to get it to work with pickle
pickle.dump(mystorage, storefile)
storefile.close()


loadfile = open("storefile.pkl", "rb")
mystorage = pickle.load(loadfile)
loadfile.close()
print(mystorage)


try:
    while True:
        print("haha, you can't stop this")
except: # Spyder is too smart and won't let us do this,
        # But you can try-except your way out of keyboard interrupts
    print("well done")