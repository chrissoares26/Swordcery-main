import arcade
import game.constants as constants

class Objective(arcade.Sprite):

    def __init__(self, path, scaling, position):
        super().__init__(path, scaling)
        self.position = position

    def collision_event(self, player):
        #What happens when the player touches me?
        pass
