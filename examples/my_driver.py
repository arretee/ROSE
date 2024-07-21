"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "version_1"

type1 = (obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER)


def drive(world):


    x = world.car.x
    y = world.car.y



    return actions.NONE
