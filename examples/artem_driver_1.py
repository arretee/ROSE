"""
This driver choice the greatest way possible, But can't get into an obstacle.
"""
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

moves_until_finish = 60


def getBestWay(world, player_x, player_y, score, min_x, max_x, moves_left):
    # Check end of recursion
    if player_y == 0 or moves_left == 0:
        return [0, score]

    # Variables
    ret_action = actions.NONE
    max_score = score
    temp_score = score
    pos = []

    # Obstacle in front of driver
    obs_next = world.get((player_x, player_y - 1))

    # If there are no obstacle
    if obs_next == obstacles.NONE:
        if player_x == 0 + min_x:
            acts = [NONE, RIGHT]
        elif player_x == 1 + min_x:
            acts = [LEFT, RIGHT, NONE]
        else:
            acts = [NONE, LEFT]

        for act in acts:
            if min_x <= player_x + act[0] <= max_x:
                player_x += act[0]
                player_y += act[1]

                pos = [player_x, player_y]

                if world.get(pos) == obstacles.NONE or world.get(pos) == obstacles.PENGUIN:
                    temp_score = getBestWay(world, player_x, player_y, temp_score, min_x, max_x, moves_left-1)[1]
                    if temp_score >= max_score:
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
                    if world.get(pos) == obstacles.PENGUIN and act == PICKUP:
                        temp_score += 10

                    temp_score = getBestWay(world, player_x, player_y, temp_score, min_x, max_x, moves_left-1)[1]
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
                    if act == JUMP:
                        temp_score += 5
                    elif act == BRAKE:
                        temp_score += 4

                    temp_score = getBestWay(world, player_x, player_y, temp_score, min_x, max_x, moves_left-1)[1]
                    if temp_score >= max_score:
                        max_score = temp_score
                        ret_action = act

                    temp_score = score

                player_y -= act[1]
                player_x -= act[0]

    # If there is a Bike, Barrier or a Trash
    else:
        for act in [LEFT, RIGHT]:
            if min_x <= player_x + act[0] <= max_x:
                player_x += act[0]
                player_y += act[1]

                pos = [player_x, player_y]

                if world.get(pos) == obstacles.NONE or world.get(pos) == obstacles.PENGUIN:
                    temp_score = getBestWay(world, player_x, player_y, temp_score, min_x, max_x, moves_left-1)[1]
                    if temp_score >= max_score:
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

    act = getBestWay(world, world.car.x, world.car.y, score, player_x_min, player_x_max, moves_until_finish)[0]

    moves_until_finish -= 1

    if moves_until_finish == 0:
        moves_until_finish = 60

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
