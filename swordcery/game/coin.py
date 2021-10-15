import arcade
from game.objective import Objective
import game.constants as constants

class Coin(Objective):

    coin_sound = arcade.load_sound(constants.COIN_SOUND)

    def __init__(self, path, scaling, position):
        super().__init__(path,scaling,position)

    def collision_event(self, player):
        player.score += 1
        arcade.play_sound(Coin.coin_sound, constants.VOLUME_SFX) #constants.VOLUME_SFX
        self.kill()


