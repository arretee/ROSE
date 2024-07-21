"""
This driver does not do any action.
"""
import random

from rose.common import obstacles, actions  # NOQA

driver_name = "artem_1"

type1 = (obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER)
type2 = (obstacles.CRACK, obstacles.WATER)
type3 = (obstacles.PENGUIN)

LEFT = (-1, -1)
NONE = (0, -1)
RIGHT = (1, -1)

BRAKE = (0, -1, 0)
JUMP = (0, -1, 1)
PICKUP = (0, -1, 2)


def getBestWay(world, player_x, player_y, score):
    if player_y == 0:
        return [0, score]


    ret_action = actions.NONE
    max_score = score
    temp_score = score
    pos = []

    obs_next = world.get((player_x, player_y - 1))

    if obs_next == obstacles.NONE:
        if player_x == 0:
            acts = [NONE, RIGHT]
        elif player_x == 1:
            acts = [LEFT, RIGHT, NONE]
        else:
            acts = [NONE, LEFT]

        for act in acts:
            if -1 < player_x + act[0] < 3:
                player_x += act[0]
                player_y += act[1]

                pos = [player_x, player_y]


                if world.get(pos) == obstacles.NONE:
                    temp_score = getBestWay(world, player_x, player_y, temp_score)[1]
                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act

                    temp_score = score

                player_y -= act[1]
                player_x -= act[0]

    elif obs_next == obstacles.PENGUIN:
        for act in [PICKUP, LEFT, RIGHT]:
            if -1 < player_x + act[0] < 3:
                player_x += act[0]
                player_y += act[1]

                pos = [player_x, player_y]

                if world.get(pos) not in type1 and world.get(pos) not in type2:
                    if world.get(pos) == obstacles.PENGUIN and act == PICKUP:
                        temp_score += 10


                    temp_score = getBestWay(world, player_x, player_y, temp_score)[1]
                    if temp_score > max_score:
                        max_score = temp_score
                        ret_action = act

                    temp_score = score

                player_y -= act[1]
                player_x -= act[0]

    elif obs_next in type2:
        if obs_next == obstacles.WATER:
            acts = [BRAKE, LEFT, RIGHT]
        else:
            acts = [JUMP, LEFT, RIGHT]

        for act in acts:
            if -1 < player_x + act[0] < 3:
                player_x += act[0]
                player_y += act[1]

                pos = [player_x, player_y]

                if world.get(pos) not in type1:
                    if act == JUMP:
                        temp_score += 5
                    elif act == BRAKE:
                        temp_score += 4


                    temp_score = getBestWay(world, player_x, player_y, temp_score)[1]
                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act

                    temp_score = score

                player_y -= act[1]
                player_x -= act[0]

    else:
        for act in [LEFT, RIGHT]:
            if -1 < player_x + act[0] < 3:
                player_x += act[0]
                player_y += act[1]

                pos = [player_x, player_y]

                if world.get(pos) == obstacles.NONE:
                    temp_score = getBestWay(world, player_x, player_y, temp_score)[1]
                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act

                    temp_score = score

                player_y -= act[1]
                player_x -= act[0]


    return [ret_action, max_score]







def drive(world):
    score = 0

    act = getBestWay(world, world.car.x, world.car.y, score)[0]

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
