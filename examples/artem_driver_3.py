"""
This driver choice the greatest way possible.

Fixes: Added full function documentation.

"""

from rose.common import obstacles, actions  # NOQA

driver_name = "artem_3"

type1 = (obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER)
type2 = (obstacles.CRACK, obstacles.WATER)
noDamageObstacles = (obstacles.PENGUIN, obstacles.NONE)

LEFT = (-1, -1)
NONE = (0, -1)
RIGHT = (1, -1)

BRAKE = (0, -1, 0)
JUMP = (0, -1, 1)
PICKUP = (0, -1, 2)

moves_until_finish = 60


def getBestWay(world, player_x: int, player_y: int, score: int, min_x: int, max_x: int, until_finish: int, ignore_next=False):
    """
    world - object with data about map.
    player_x - player x position.
    player_y - player y position.
    min_x - min x value player can be (left side x of the road)
    max_x - max x value player can be (right side x of the road)
    until_finish - number moves left until game ends.
    ignore_next(Default value = False) - meaning to say whether to ignore an object in front of the driver
    """

    """
    Function template:
    
    
    if player on finish or on the end of map: end recursion
    
    initialize variables
    
    check if need to ignore item in front of driver
    
    if the obs next to driver is none:
        check all actions that driver can do (even if it leads to loss of points)
        and choose the best option(option with best final score)
    
    elif the obs next to driver is pinguin:
        check all actions that driver can do (even if it leads to loss of points)
        and choose the best option(option with best final score)
        
    elif the ons next to driver from type2 (Water and Crack)
        check all actions that driver can do (even if it leads to loss of points)
        and choose the best option(option with best final score)
    
    else (If obs next to driver from type3 (Bike, Barrier, Trash)
        check all actions that driver can do (even if it leads to loss of points)
        and choose the best option(option with best final score)
        
        
    return [action, best_score, if there was a crash]
    """

    # Check end of recursion(or end of world, or end of race)
    if player_y == 0 or until_finish == 0:
        return [0, score]

    # Variables
    ret_action = actions.NONE
    max_score = score
    temp_score = score
    crash = False
    obs_next = world.get((player_x, player_y - 1))
    pos = []

    # Obstacle in front of driver.
    if ignore_next is True:
        obs_next = obstacles.NONE

    # If there are no obstacle
    if obs_next == obstacles.NONE:
        # Keep driver in middle of road if there are similar scores.
        if player_x == 0 + min_x:
            acts = [NONE, RIGHT]
        elif player_x == 1 + min_x:
            acts = [LEFT, RIGHT, NONE]
        else:
            acts = [NONE, LEFT]

        for act in acts:
            # If player new x position is on the road.
            if min_x <= player_x + act[0] <= max_x:
                # Update driver pos
                player_x += act[0]
                player_y += act[1]

                pos = [player_x, player_y]

                if world.get(pos) in noDamageObstacles:
                    temp_score = \
                    getBestWay(world, player_x, player_y, temp_score, min_x, max_x, until_finish - 1, False)[1]
                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act
                        crash = False

                    temp_score = score

                elif ignore_next is False:
                    temp_score -= 10
                    temp_score = \
                        getBestWay(world, player_x, player_y + 1, temp_score, min_x, max_x, until_finish - 1, True)[
                            1]

                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act
                        crash = True

                    temp_score = score

                player_y -= act[1]
                player_x -= act[0]

    # If there are a Pinguin
    elif obs_next == obstacles.PENGUIN:
        for act in [PICKUP, LEFT, RIGHT]:
            if min_x <= player_x + act[0] <= max_x:
                player_x += act[0]
                player_y += act[1]

                pos = [player_x, player_y]

                if world.get(pos) in noDamageObstacles:
                    if world.get(pos) == obstacles.PENGUIN and act == PICKUP:
                        temp_score += 10

                    temp_score = \
                        getBestWay(world, player_x, player_y, temp_score, min_x, max_x, until_finish - 1, False)[1]
                    if temp_score > max_score:
                        max_score = temp_score
                        ret_action = act
                        crash = False

                    temp_score = score

                elif ignore_next is False:
                    temp_score -= 10
                    temp_score = \
                        getBestWay(world, player_x, player_y + 1, temp_score, min_x, max_x, until_finish - 1, True)[1]

                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act
                        crash = True

                    temp_score = score

                player_y -= act[1]
                player_x -= act[0]

    # If there is a Water or Crack
    elif obs_next in type2:
        if obs_next == obstacles.WATER:
            acts = [BRAKE, LEFT, RIGHT]
        else:   # obs_next = obstacles.CRACK
            acts = [JUMP, LEFT, RIGHT]

        for act in acts:
            if min_x <= player_x + act[0] <= max_x:
                player_x += act[0]
                player_y += act[1]

                pos = [player_x, player_y]

                if world.get(pos) not in type1:
                    if act == JUMP:
                        temp_score += 5
                    elif act == BRAKE:
                        temp_score += 4

                    temp_score = \
                        getBestWay(world, player_x, player_y, temp_score, min_x, max_x, until_finish - 1, False)[1]
                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act
                        crash = False

                    temp_score = score

                elif ignore_next is False:
                    temp_score -= 10
                    temp_score = \
                        getBestWay(world, player_x, player_y + 1, temp_score, min_x, max_x, until_finish - 1, True)[1]

                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act
                        crash = True

                    temp_score = score

                player_y -= act[1]
                player_x -= act[0]

    # If there is a Bike, Barrier or a Trash
    else:
        for act in [NONE, LEFT, RIGHT]:
            if min_x <= player_x + act[0] <= max_x:
                player_x += act[0]
                player_y += act[1]

                pos = [player_x, player_y]

                if world.get(pos) == obstacles.NONE:
                    temp_score = \
                        getBestWay(world, player_x, player_y, temp_score, min_x, max_x, until_finish - 1, False)[1]
                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act
                        crash = False

                    temp_score = score

                elif ignore_next is False:
                    temp_score -= 10
                    temp_score = \
                        getBestWay(world, player_x, player_y + 1, temp_score, min_x, max_x, until_finish - 1, True)[1]

                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act
                        crash = True

                    temp_score = score

                player_y -= act[1]
                player_x -= act[0]

    # Return
    return [ret_action, max_score, crash]


def drive(world):
    global moves_until_finish, crash_times
    score = 0

    if 3 <= world.car.x <= 5:
        player_x_min = 3
        player_x_max = 5
    else:
        player_x_min = 0
        player_x_max = 2

    act = getBestWay(world, world.car.x, world.car.y, score, player_x_min, player_x_max, moves_until_finish)

    moves_until_finish -= 1

    if moves_until_finish == 0:
        moves_until_finish = 60

    act = act[0]
    if act == LEFT:
        return actions.LEFT
    if act == RIGHT:
        return actions.RIGHT
    if act == NONE:
        return actions.NONE
    if act == BRAKE:
        return actions.BRAKE
    if act == JUMP:
        return actions.JUMP

    return actions.PICKUP
