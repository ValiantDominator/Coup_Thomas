# Coup files

All coup files start with a list of players, in turn order.

In a word with no challenging and blocking, a game file is quite simple.
Each player in turn order must take an action. When a player finally
discards a card, then the gamefile must display who discarded that card.
So, at all times, your game master should know what to expect (when blocks
and challenges get here, it gets more complicated).

The format of a line in the document is the following
```
<Acting_player> <action/reaction> <target>
```
Notice that the target portion is optional. Your program should know
when to expect a target or not. You *can* expect and enforce that
there will be no spaces in player names and action/reaction names.


```
players: [a, b, c, d]
a tax
b tax
c steal a
d steal c
a assassinate c
c discard contessa
b assassinate d
d discard duke
c tax
d tax
a tax
b tax
c assassinate d
a tax
... # many more lines
winner: a
```

Notice that player D was skipped when he was eliminated. Eliminated players
don't get a turn, and they don't get to block or challenge.

This means that, at all times, your program must know
    - How many cards each player has
        - Who is eliminated and must be skipped (or removed from a list...)
    - How many coins each player has
        - What actions are legal for that player
        - If that player must coup


When there is only one player remaining, that player is marked as the winner.
This piece of information is not necessary for the purposes of the game (we
should know who won because we know who the last player is), but it could be
very convenient later on to go through many files with the same players and
just look at the last line to see who won.



Add challenging and blocking:

Players: [a, b, c, ...] # Max 6. In turn order.
a tax # First player's action
b challenge # Other players have a chance to block or challenge
b discard captain # the loser of the challenge discards a card
    # It is inferred that player a must have replaced his card
b tax # Second player's action
a challenge
b discard ambassador # this time, the challenger won the challenge
    # It is inferred that player b is eliminated. On turn 2!
c tax
...