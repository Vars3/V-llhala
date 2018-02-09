# -*- coding: utf-8 -*-
from pirates import *


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


def open_capsule(game, capsules_list):
    """
    the function finds whether there is an unused capsule. if so , it returns the capsule, else return None.

    :param game: the current game state, capsules_list: a lsit with the current state of each capsule
    :type game: PirateGame, capsules_list: list of Bool
    """
    for capsule in game.get_my_capsules():
        if not capsules_list[game.get_my_capsules().index(capsule)]:
            return capsule
    return None


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



