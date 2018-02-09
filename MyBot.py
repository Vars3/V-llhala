# -*- coding: utf-8 -*-
from pirates import *
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
    sorted_pirates = sorted(living_pirates, key=lambda pirate: desirable_enemy_mothership(game).get_location().distance(
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


def attack(game, attack_pirates):
    """
    the function controls the attack mechanism of the offensive pirates.
    strategy: putting pairs of pirates together. first pirate takes the capsule, the second follows him. when close
    enough to the mothership, the second push the first over the defenses to the mother ship


    :param game: the current game state, attack_pirates: a list of the defensive pirates
    :type game: PirateGame, attack_pirates: list of Pirate
    """
    # in order to avoid pirates changing their pairs constantly, i sorted the pirates by generic, static filter.
    # now, the order of pirates within the list will stay the same, uunless a pirate dies.
    # so, the pairs will stay the same.
    attack_pirates = sorted(attack_pirates, key=lambda pirate: pirate.initial_location.distance(
        desirable_enemy_mothership(game).get_location()))
    is_capsule_taken = [False] * len(game.get_my_capsules())
    for capsule in game.get_my_capsules():
        if capsule.holder is not None:
            is_capsule_taken[game.get_my_capsules().index(capsule)] = True
    already_acted = False
    pairs = [attack_pirates[i:i + 2] for i in xrange(0, len(attack_pirates), 2)]

    for pair in pairs:
        already_acted = False
        if len(pair) > 1:
            # if one of the pair has capsule
            if pair[0].has_capsule() or pair[1].has_capsule():
                sorted_pair = capsule_holder(pair[0], pair[1])
                #if the distance between is too big, narrow it down
                if pair[0].get_location().distance(pair[1]) > 300:
                    sorted_pair[0].sail(sorted_pair[0].get_location())
                    sorted_pair[1].sail(sorted_pair[0].get_location())
                    already_acted = True
                # if an enemy is within push range or if i can score, push the capsule to mothership
                elif can_enemys_push(game, sorted_pair[0]) or sorted_pair[0].distance(
                        desirable_mothership(game, sorted_pair[0])) < 600 and not already_acted:
                    try:
                        sorted_pair[1].push(sorted_pair[0], desirable_mothership(game, sorted_pair[0]))
                        already_acted = True
                    except:
                        # cant push, sail to mothership
                        sorted_pair[0].sail(desirable_mothership(game, sorted_pair[0]))
                        sorted_pair[1].sail(sorted_pair[0])
                        already_acted = True
                elif not already_acted:
                    # if u just cruising with your capsule, keep it going then
                    sorted_pair[0].sail(desirable_mothership(game, sorted_pair[0]))
                    sorted_pair[1].sail(sorted_pair[0])
                    already_acted = True
            elif not already_acted:
                # if you don't have capsule, find an open capsule and go for it
                for capsule in game.get_my_capsules():
                    if not is_capsule_taken[game.get_my_capsules().index(capsule)] and not already_acted:
                        pair[0].sail(capsule)
                        pair[1].sail(capsule)
                        already_acted = True
                        is_capsule_taken[game.get_my_capsules().index(capsule)] = True
                # if there is no open capsule go wait in the mine of the capsule
                if not already_acted:
                    pair[0].sail(game.get_my_capsules()[0].initial_location)
                    pair[1].sail(game.get_my_capsules()[0].initial_location)
        # if you are only 1 pirate, and u have a capsule, sail
        elif pair[0].has_capsule():
            pair[0].sail(desirable_mothership(game, pair[0]))
            already_acted = True
        #if you dont have a capsule, go find one
        elif not already_acted:
            for capsule in game.get_my_capsules():
                if not is_capsule_taken[game.get_my_capsules().index(capsule)] and not already_acted:
                    pair[0].sail(capsule)
                    already_acted = True
                    is_capsule_taken[game.get_my_capsules().index(capsule)] = True
            if not already_acted:
                    pair[0].sail(game.get_my_capsules()[0].initial_location)



def defense(game, defense_pirates):
    """
    the function controls the defense mechanism of the defensive pirates.
    strategy: putting pairs of pirates together. first pair is located far enough from the mother ship so if the enemy
    jumps above he doesnt get to the unload range

    :param game: the current game state, defense_pirates: a list of the defensive pirates
    :type game: PirateGame, defense_pirates: list of Pirate
    """
    defended_mothership = desirable_enemy_mothership(game)
    # actual range of defense. this value is the range defended before the capsule dropout zone
    # TO DO: understand what the optimal value of distance, maximal for OneManArmy is -50
    if len(defense_pirates) == 1:
        distance = defended_mothership.unload_range - 50
    else:
        distance = defended_mothership.unload_range + 600
    pairs = [defense_pirates[i:i + 2] for i in xrange(0, len(defense_pirates), 2)]
    already_acted = False
    is_capsule_pushed = [False] * len(game.get_enemy_capsules())
    for pair in pairs:
        already_acted = False
        for capsule in game.get_enemy_capsules():
            if not is_capsule_pushed[game.get_enemy_capsules().index(capsule)]:
                if capsule.holder is not None:
                    try:
                        if pair[0].can_push(capsule.holder) and pair[1].can_push(capsule.holder):
                            pair[0].push(capsule.holder, optimal_pushing_direction(capsule.holder, game))
                            pair[1].push(capsule.holder, optimal_pushing_direction(capsule.holder, game))
                            already_acted = True
                            is_capsule_pushed[game.get_enemy_capsules().index(capsule)] = True
                    except:
                        if pair[0].can_push(capsule.holder):
                            pair[0].push(capsule.holder, optimal_pushing_direction(capsule.holder, game))
                            already_acted = True
                            is_capsule_pushed[game.get_enemy_capsules().index(capsule)] = True

        if not already_acted:
            pair[0].sail(
                defended_mothership.get_location().towards(desirable_enemy(game, defended_mothership), distance))
            try:
                pair[1].sail(
                    defended_mothership.get_location().towards(desirable_enemy(game, defended_mothership), distance))
            except:
                pass
            distance += 500


def asteroid_behavior(game, pirate, next_location):
    """
    the function controls the asteroid behavior of the pirate.
    strategy: checks if thepirate is goiing to collide with an asteroid. if so,
    checks if the pirate should and can push the asteroid and to wat direction or let it pass.

    :param game: the current game state, pirate: a pirate, next_location: the pirates next location
    :type game: PirateGame, pirate: Pirate, next_location: Location
    """
    for asteroid in game.get_living_asteroids():
        pass


def can_enemys_push(game, pirate):
    """
    the function gets a pirate and return true if there are 2 enemy ship that can push the pirate.

    :param game: a game,  pirate: a pirate
    :type game: PirateGame, pirate: Pirate
    """
    count = 0
    for enemy in game.get_enemy_living_pirates():
        if enemy.can_push(pirate) or enemy.distance(pirate) < 350:
            count += 1
        if count == 2:
            return True
    return False


def get_next_location(pirate, destination):
    """
    the function gets a pirate and its sailing destination and return its upcoming location

    :param pirate: a pirate,  destination: a location
    :type pirate: Pirate, destination: Location
    """
    pass


def capsule_holder(pirate1, pirate2):
    """
    the function gets a pair of pirates and return the following list:
    [holding capsule, not holding capsule]

    :param pirate1: a pirate,  pirate2: a pirate
    :type pirate1: Pirate, pirate2: Pirate
    :return list: the desirable mine
    :rtype list: list of Pirate
    """
    if pirate1.has_capsule():
        return [pirate1, pirate2]
    else:
        return [pirate2, pirate1]


def desirable_capsule(game):
    """
    the function returns the mine which is located closest to a mothership, and has a capsule

    :param game: the current game state
    :type game: PirateGame
    :return mine: the desirable mine
    :rtype mine: Location
    """

    minimal_distance = 999999
    minimal_capsule = None
    for capsule in game.get_my_capsules():
        if capsule.holder is None:
            for mothership in game.get_my_motherships():
                if mothership.distance(capsule.initial_location) < minimal_distance:
                    minimal_capsule = capsule
                    minimal_distance = mothership.distance(capsule.initial_location)
    return minimal_capsule


def optimal_pushing_direction(pirate, game):
    """
    the function finds the closest wall to the pirate, thus the best direction to push

    :param pirate: a pirate, game: the current game state
    :type pirate: Pirate, game: PirateGame
    """
    pirate_location = pirate.get_location()
    walls = [Location(0, pirate_location.col), Location(game.rows, pirate_location.col),
             Location(pirate_location.row, game.cols),
             Location(pirate_location.row, 0)]
    minimal_wall = None
    minimal_distance = 999999
    for wall in walls:
        if pirate_location.distance(wall) < minimal_distance:
            minimal_wall = walls.index(wall)
            minimal_distance = pirate_location.distance(wall)
    # in order to push out of the board
    if minimal_wall == 0:
        walls[minimal_wall].row -= 1000
    elif minimal_wall == 1:
        walls[minimal_wall].row += 1000
    elif minimal_wall == 2:
        walls[minimal_wall].col += 1000
    elif minimal_wall == 3:
        walls[minimal_wall].col -= 1000

    return walls[minimal_wall]


def desirable_enemy(game, mothership):
    """
    the function return the enemy's capsule which is in the closest range to the specified mothership

    :param game: the current game state, mothership: the current mothership
    :type game: PirateGame, mothership: Mothership
    """
    minimal_distance = 999999
    minimal_capsule = None
    for capsule in game.get_enemy_capsules():
        if capsule.distance(mothership.get_location()) < minimal_distance:
            minimal_capsule = capsule
            minimal_distance = capsule.distance(mothership.get_location())
    return minimal_capsule


def desirable_enemy_mothership(game):
    """
    the function returns the enemy mothership closest to a mine, best to defend on

    :param game: the current game state
    :type game: PirateGame
    :return mothership: the desirable mothership
    :rtype mothership: Mothership
    """

    minimal_distance = 999999
    minimal_mothership = None
    for mothership in game.get_enemy_motherships():
        for capsule in game.get_enemy_capsules():
            if mothership.distance(capsule.initial_location) < minimal_distance:
                minimal_mothership = mothership
                minimal_distance = mothership.distance(capsule.initial_location)
    return minimal_mothership


def desirable_mothership(game, pirate):
    """
    the function returns the  mothership closest to the pirate, best to sail to

    :param game: the current game state, pirate: a pirate
    :type game: PirateGame, pirate: Pirate
    :return mothership: the desirable mothership
    :rtype mothership: Mothership
    """
    minimal_distance = 999999
    minimal_mothership = None
    for mothership in game.get_my_motherships():
        if mothership.distance(pirate) < minimal_distance:
            minimal_mothership = mothership
            minimal_distance = mothership.distance(pirate)
    return minimal_mothership


def do_turn(game):
    """
Makes the bot run a single turn

:param game: the current game state
:type game: PirateGame
"""
    divide_living_pirates(game)
