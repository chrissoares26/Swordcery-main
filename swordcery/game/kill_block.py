import arcade
import game.constants as constants
from game.objective import Objective

class KillBlock(Objective):

    def __init__(self, path, scaling, position):
        super().__init__(path,scaling,position)

    def collision_event(self, player):
        player.health = 0
