# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 14:05:21 2022

@author: Daniel Mishler
"""

coup_actions = [
    "income",
    "foreign_aid",
    "coup",
    "tax",
    "steal",
    "exchange",
    "assassinate",
    "block_steal",
    "block_assassinate",
    "block_foreign_aid",
    "challenge"
    ]

turn_actions = [
    "income",
    "foreign_aid",
    "coup",
    "tax",
    "steal",
    "exchange",
    "assassinate"
    ]

actions_requiring_target = [
    "coup",
    "steal",
    "assassinate"
    ]

respondable_actions = [
    "foreign_aid",
    "tax",
    "steal",
    "exchange",
    "assassinate",
    "block_steal",
    "block_assassinate",
    "block_foreign_aid",
    ]

challengeable_actions = [
    "tax",
    "steal",
    "exchange",
    "assassinate",
    "block_steal",
    "block_assassinate",
    "block_foreign_aid",
    ]

blockable_actions = [
    "foreign_aid",
    "steal",
    "assassinate"
    ]

singly_blockable_actions = [
    "steal",
    "assassinate"
    ]

card_abilities = {
    "duke" :       ["tax", "block_foreign_aid"],
    "captain" :    ["steal", "block_steal"],
    "assassin" :   ["assassinate"],
    "contessa" :   ["block_assassinate"],
    "ambassador" : ["exchange", "block_steal"]
    }

# returns: an array of `turn` dictionaries
# assumes: log is a correct coup game
# edge case: a player who was supposed to lose 2 cards may only lose 1 card.
#            This is fine! It means they only had 1 card to lose. It won't even
#            be in the logs.
def log_to_turn_list(log):
    # The log is a string containing the lines of the game
    log_lines = log.split('\n')[1:] # skip the players: line
    turns = []
    for line in log_lines:
        if line == "":
            continue
        
        actor = line.split()[0]
        action = line.split()[1]

        
        if action in turn_actions:
            if action in actions_requiring_target:
                target = line.split()[2]
            else:
                target = None        
            turn_dict = {}
            turn_dict["actor"] = actor
            turn_dict["action"] = action
            turn_dict["target"] = target
            turn_dict["blocker"] = None
            turn_dict["challenger"] = None
            turn_dict["challenger_win"] = None
            turn_dict["discard_a"] = {}# Discarded as a result of the action
            turn_dict["discard_c"] = {}# Discarded as a result of the challenge
            
            turns.append(turn_dict)
        
        elif action[:6] == "block_":
            turns[-1]["blocker"] = actor
        
        elif action == "challenge":
            turns[-1]["challenger"] = actor
        
        elif action == "discard":
            # The challenge discard is resolved first
            card = line.split()[2]
            if turns[-1]["challenger"] is not None:
                if actor == turns[-1]["challenger"]:
                    turns[-1]["challenger_win"] = False
                else:
                    turns[-1]["challenger_win"] = True
                turns[-1]["discard_c"][actor] = card
            else: # The challenge was from the action
                turns[-1]["discard_a"][actor] = card

        elif actor == "winner:":
            pass
        
        else:
            print("Error! unknown line '%s'" % line)
    
    return turns

def get_players_from_log(log):
    first_log_line = log.split('\n')[0]
    start_i = first_log_line.find('[')
    end_i = first_log_line.find(']')
    players_string = first_log_line[start_i+1:end_i]
    players_array = players_string.split(", ")
    return players_array
    
def turn_list_to_game_dict(players, turn_list):
    # First, build the players dict.
    players_dict = {}
    for player in players:
        players_dict[player] = {}
        players_dict[player]["coins"] = 2
        players_dict[player]["cards"] = 2
    for turn in turn_list:
        # decide whether to apply action
        if turn["blocker"] == None:
            blocked = False
        else:
            blocked = True
        
        if turn["challenger_win"] == True:
            challenge_success = True
        else: # False or None
            challenge_success = False
            
        if blocked ^ challenge_success:
            # action was either blocked or successfully challenged
            
            if turn["action"] == "assassinate":
                players_dict[turn["actor"]]["coins"] -= 3
            
        else:
            # action was neither blocked nor challenged, or
            # action was blocked, but block was challenged
            # apply the action
            action = turn["action"]
            actor = turn["actor"]
            target = turn["target"]
            if action == "income":
                players_dict[actor]["coins"] += 1
            if action == "foreign_aid":
                players_dict[actor]["coins"] += 2
            if action == "tax":
                players_dict[actor]["coins"] += 3
            if action == "steal":
                steal_coins = min(players_dict[target]["coins"], 2)
                players_dict[actor]["coins"] += steal_coins
                players_dict[target]["coins"] -= steal_coins
            if action == "assassinate":
                players_dict[actor]["coins"] -= 3
            if action == "coup":
                players_dict[actor]["coins"] -= 7
        # apply discards
        for player in turn["discard_a"]: # a loop with at most 1 iteration
            players_dict[player]["cards"] -= 1
        for player in turn["discard_c"]:
            players_dict[player]["cards"] -= 1
    
    
    # How to know what round it is:
    # The player who just took the last turn can define what round it is.
    # Simply observe how many times *that player's name* appears in the turns
    # when that player is the actor.
    this_round = 0
    for turn in turn_list:
        if turn["actor"] == turn_list[-1]["actor"]:
            this_round += 1
    # There's a catch, though. If that player ended a round, then the *next*
    # turn is in round `this_round+1`.
    
    game_dict = {}
    game_dict["players"] = players_dict
    game_dict["turns"] = turn_list
    try:
        game_dict["this_turn"] = turn_list[-1]
    except IndexError:
        game_dict["this_turn"] = None
    game_dict["round"] = this_round
    return game_dict

def log_to_game_dict(log):
    turns = log_to_turn_list(log)
    players = get_players_from_log(log)
    game_dict = turn_list_to_game_dict(players, turns)
    return game_dict

if __name__ == '__main__':
    turnfile = open("coup_game_test.coup", "r")
    log = turnfile.read()
    game_dict = log_to_game_dict(log)
    print(game_dict)
    turnfile.close()