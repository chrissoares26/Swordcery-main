import arcade
import game.constants as constants
from game.objective import Objective

class FinishLine(Objective):

    def __init__(self, path, scaling, position):
        super().__init__(path,scaling,position)

    def collision_event(self, player):
        print("You win!")
        #Some other event code here
        player.has_won = True
        player.score += 5

        