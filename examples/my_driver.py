"""
This driver does not do any action.
"""
import random

from rose.common import obstacles, actions  # NOQA

driver_name = "version_1"

type1 = (obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER)
type2 = (obstacles.CRACK, obstacles.WATER)
type3 = (obstacles.PENGUIN)


def drive(world):
    x = world.car.x
    y = world.car.y

    if world.get((x, y - 1)) in type1:
        if x == 0:
            return actions.RIGHT
        elif x == 2:
            return actions.LEFT
        else:
            return random.choice((actions.LEFT, actions.RIGHT))
    elif world.get((x, y - 1)) in type2:
        if obstacles.CRACK == world.get((x, y - 1)):
            return actions.JUMP
        elif obstacles.WATER == world.get((x, y - 1)):
            return actions.BRAKE
    else:
        return actions.PICKUP

    return actions.NONE
