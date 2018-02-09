from attack import *


def defense(game, defense_pirates):
    """
    the function controls the defense mechanism of the defensive pirates.
    strategy: putting pairs of pirates together. first pair is located far enough from the mother ship so if the enemy
    jumps above he doesnt get to the unload range

    :param game: the current game state, defense_pirates: a list of the defensive pirates
    :type game: PirateGame, defense_pirates: list of Pirate
    """
    if defense_pirates:
        defended_mothership = desirable_enemy_mothership(game)
        if defended_mothership == None:
            attack(game, defense_pirates)
        else:
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
