# -*- coding: utf-8 -*-
from functions import *
from attack import *
from defense import *
from math import *
""" -------- TO DO LIST ---------
    1. write aan asteroid dealing function, pirates keep killing themselves
    2. fix some bugs in the attack function. look in steroids an other battles for examples

"""


def divide_living_pirates(game):
    """
    the function sets the defense \ offense dividing ratio and calls the defense and offense functions,
    transferring them a list with the needed pirates.
    the function sets the defense \ offense dividing ratio as follow:

     num of living pirates | num of defense | num of offense

       8 living | 4 defense | 4 offense
       7 living | 4 defense | 3 offense
       6 living | 4 defense | 2 defense
       5 living | 3 defense | 2 offense
       4 living | 2 defense | 2 offense
       3 living | 2 defense | 1 offense
       2 living | 1 defense | 1 offense
       1 living | 1 defense | 0 offense

    :param game: the current game state
    :type game: PirateGame
    """
    offense_pirates = []
    defense_pirates = []
    # setting the dividing ratio
    if len(game.get_my_living_pirates()) == 6:
        num_of_defense = 4
    else:
        num_of_defense = ceil(0.5 * len(game.get_my_living_pirates()))
    num_of_offense = len(game.get_my_living_pirates()) - num_of_defense

    living_pirates = game.get_my_living_pirates()
    # sorting the living pirates according to their distance to the enemy's mothership
    # TO DO: write a code that deals with a case in which there are 2 enemy motherships
    if game.get_enemy_motherships():
        sorted_pirates = sorted(living_pirates, key=lambda pirate: desirable_enemy_mothership(game).get_location().distance(
            pirate.get_location()))
    else:
        sorted_pirates = sorted(living_pirates, key=lambda pirate: desirable_mothership(game,pirate).get_location().distance(
            pirate.get_location()))
    for i in xrange(len(living_pirates)):
        if i < num_of_defense:
            defense_pirates.append(sorted_pirates[i])
        else:
            offense_pirates.append(sorted_pirates[i])
    print offense_pirates
    print defense_pirates
    attack(game, offense_pirates)
    defense(game, defense_pirates)



def do_turn(game):
    """
Makes the bot run a single turn

:param game: the current game state
:type game: PirateGame
"""
    divide_living_pirates(game)

