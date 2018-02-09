# -*- coding: utf-8 -*-
from functions import *


def attack(game, attack_pirates):
    """
    the function controls the attack mechanism of the offensive pirates.
    strategy: putting pairs of pirates together. first pirate takes the capsule, the second follows him. when close
    enough to the mothership, the second push the first over the defenses to the mother ship


    :param game: the current game state, attack_pirates: a list of the defensive pirates
    :type game: PirateGame, attack_pirates: list of Pirate
    """
    if attack_pirates:
        # in order to avoid pirates changing their pairs constantly, i sorted the pirates by generic, static filter.
        # now, the order of pirates within the list will stay the same, uunless a pirate dies.
        # so, the pairs will stay the same.
        attack_pirates = sorted(attack_pirates, key=lambda pirate: pirate.initial_location.distance(Location(0, 0)))
        # a boolean list for knowing which capsule is already taken care of.
        is_capsule_taken = [False] * len(game.get_my_capsules())
        # setting the initials values of the list
        for capsule in game.get_my_capsules():
            if capsule.holder is not None:
                is_capsule_taken[game.get_my_capsules().index(capsule)] = True

        # dividing the pirates into pairs
        pairs = [attack_pirates[i:i + 2] for i in xrange(0, len(attack_pirates), 2)]

        for pair in pairs:

            # if the pair is two
            if len(pair) > 1:
                # if one of the pair has capsule
                if pair[0].has_capsule() or pair[1].has_capsule():
                    sorted_pair = capsule_holder(pair[0], pair[1])
                    #if the distance between is too big, narrow it down
                    if pair[0].get_location().distance(pair[1]) > 300:
                        sorted_pair[0].sail(sorted_pair[0].get_location())
                        sorted_pair[1].sail(sorted_pair[0].get_location())
                        continue
                    # if an enemy is within push range or if i can score, push the capsule to mothership
                    elif can_enemys_push(game, sorted_pair[0]) or sorted_pair[0].distance(
                            desirable_mothership(game, sorted_pair[0])) < 600:
                        #if you can push, push
                        if sorted_pair[1].can_push(sorted_pair[0]):
                            sorted_pair[1].push(sorted_pair[0], desirable_mothership(game, sorted_pair[0]))
                            sorted_pair[0].sail(desirable_mothership(game, sorted_pair[0]))
                            continue
                        else:
                            # cant push, sail to mothership
                            sorted_pair[0].sail(desirable_mothership(game, sorted_pair[0]))
                            sorted_pair[1].sail(sorted_pair[0])
                            continue
                    # if u just cruising with your capsule, keep it going then
                    else:
                        """ TO DO: check if there is an enemy that will be in push range in the next turn"""
                        sorted_pair[0].sail(desirable_mothership(game, sorted_pair[0]))
                        sorted_pair[1].sail(sorted_pair[0])
                        continue
                # if you don't have capsule, find an open capsule and go for it
                else:
                    dest_capsule = open_capsule(game, is_capsule_taken)
                    if dest_capsule is not None:
                        pair[0].sail(dest_capsule)
                        pair[1].sail(dest_capsule)
                        is_capsule_taken[game.get_my_capsules().index(capsule)] = True
                        continue
                    # if there is no open capsule go wait in the mine of the capsule
                    else:
                        pair[0].sail(game.get_my_capsules()[0].initial_location)
                        pair[1].sail(game.get_my_capsules()[0].initial_location)
                        continue

            # if you are only 1 pirate, and u have a capsule, sail
            elif pair[0].has_capsule():
                pair[0].sail(desirable_mothership(game, pair[0]))
                continue
            #if you dont have a capsule, go find one
            else:
                dest_capsule = open_capsule(game, is_capsule_taken)
                if dest_capsule is not None:
                    pair[0].sail(capsule)
                    is_capsule_taken[game.get_my_capsules().index(capsule)] = True
                    continue
                # if there is no open capsule, go wait in the mine of the capsule
                else:
                    pair[0].sail(game.get_my_capsules()[0].initial_location)

