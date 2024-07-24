"""
This driver choice the greatest way possible.

Fixes: Bot know when race is over.
       Bot can lose points to get more points.

"""
from rose.common import obstacles, actions  # NOQA

driver_name = "Moshiko"

type1 = (obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER)
type2 = (obstacles.CRACK, obstacles.WATER)


LEFT = (-1, -1)
NONE = (0, -1)
RIGHT = (1, -1)

BRAKE = (0, -1, 0)
JUMP = (0, -1, 1)
PICKUP = (0, -1, 2)

moves_until_finish = 60


def getBestWay(world, player_x, player_y, score, min_x, max_x, until_finish):
    """
    world - object with data about map.
    player_x - player x position.
    player_y - player y position.
    min_x - min x value player can be (left side x of the road)
    max_x - max x value player can be (right side x of the road)
    until_finish - number moves left until game ends.
    cells_to_ignore - list of cells to ignore collision with them.
    """

    """
    Function template:


    if player on finish or on the end of map: end recursion

    initialize variables


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


    return [action, best_score]
    """


    # Check end of recursion(or end of world, or end of race)
    if player_y == 0 or until_finish == 0:
        return [0, score]

    if player_y > 10:
        player_y = 10

    # Variables
    ret_action = actions.NONE
    max_score = -100000
    temp_score = score
    pos = []

    # Obstacle in front of driver
    obs_next = world.get((player_x, player_y - 1))


    # If there are no obstacle
    if obs_next == obstacles.NONE:
        if min_x == 3:
            if player_x == 0 + min_x:
                acts = [RIGHT, NONE]
            elif player_x == 1 + min_x:
                acts = [RIGHT, NONE, LEFT]
            else:
                acts = [NONE, LEFT]
        else:
            if player_x == 0 + min_x:
                acts = [NONE, RIGHT]
            elif player_x == 1 + min_x:
                acts = [LEFT, NONE, RIGHT]
            else:
                acts = [LEFT, NONE]

        for act in acts:
            if min_x <= player_x + act[0] <= max_x:
                player_x += act[0]
                player_y += act[1]

                pos = [player_x, player_y]

                if world.get(pos) == obstacles.NONE or world.get(pos) == obstacles.PENGUIN:
                    temp_score += 10
                    temp_score = getBestWay(world, player_x, player_y, temp_score, min_x, max_x, until_finish - 1)[1]
                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act

                    temp_score = score

                else:
                    temp_score -= 10
                    temp_score = getBestWay(world, player_x, player_y, temp_score, min_x, max_x, until_finish - 1)[1]

                    if temp_score > max_score:
                        max_score = temp_score
                        ret_action = act

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

                if world.get(pos) not in type1 and world.get(pos) not in type2:
                    temp_score += 10
                    if world.get(pos) == obstacles.PENGUIN and act == PICKUP:
                        temp_score += 10

                    temp_score = getBestWay(world, player_x, player_y, temp_score, min_x, max_x, until_finish - 1)[1]
                    if temp_score > max_score:
                        max_score = temp_score
                        ret_action = act

                    temp_score = score

                else:
                    temp_score -= 10
                    temp_score = getBestWay(world, player_x, player_y, temp_score, min_x, max_x, until_finish - 1)[1]

                    if temp_score > max_score:
                        max_score = temp_score
                        ret_action = act

                    temp_score = score

                player_y -= act[1]
                player_x -= act[0]

    # If there is a Water or Crack
    elif obs_next in type2:
        if obs_next == obstacles.WATER:
            acts = [BRAKE, LEFT, RIGHT]
        else:
            acts = [JUMP, LEFT, RIGHT]

        for act in acts:
            if min_x <= player_x + act[0] <= max_x:
                player_x += act[0]
                player_y += act[1]

                pos = [player_x, player_y]

                if world.get(pos) not in type1:
                    temp_score += 10
                    if act == JUMP:
                        temp_score += 5
                    elif act == BRAKE:
                        temp_score += 4

                    temp_score = getBestWay(world, player_x, player_y, temp_score, min_x, max_x, until_finish - 1)[1]
                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act


                    temp_score = score

                else:
                    temp_score -= 10
                    temp_score = getBestWay(world, player_x, player_y, temp_score, min_x, max_x, until_finish - 1)[1]

                    if temp_score > max_score:
                        max_score = temp_score
                        ret_action = act

                    temp_score = score

                player_y -= act[1]
                player_x -= act[0]

    # If there is a Bike, Barrier or a Trash
    else:
        if min_x == 3:
            acts = [NONE, RIGHT, LEFT]
        else:
            acts = [NONE, LEFT, RIGHT]

        for act in acts:
            if min_x <= player_x + act[0] <= max_x:
                player_x += act[0]
                player_y += act[1]

                pos = [player_x, player_y]

                if world.get(pos) == obstacles.NONE or world.get(pos) == obstacles.PENGUIN:
                    temp_score += 10
                    temp_score = getBestWay(world, player_x, player_y, temp_score, min_x, max_x, until_finish - 1)[1]
                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act

                    temp_score = score

                else:
                    temp_score -= 10
                    temp_score = getBestWay(world, player_x, player_y, temp_score, min_x, max_x, until_finish - 1)[1]

                    if temp_score > max_score:
                        max_score = temp_score
                        ret_action = act

                    temp_score = score

                player_y -= act[1]
                player_x -= act[0]



    # Return
    return [ret_action, max_score]


def drive(world):
    global moves_until_finish
    score = 0

    if 3 <= world.car.x <= 5:
        player_x_min = 3
        player_x_max = 5
    else:
        player_x_min = 0
        player_x_max = 2

    ret = getBestWay(world, world.car.x, world.car.y, score, player_x_min, player_x_max, moves_until_finish)

    moves_until_finish -= 1

    if moves_until_finish == 0:
        moves_until_finish = 60

    act = ret[0]
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
