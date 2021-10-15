import arcade
import game.constants as constants
import random
from game.entity import Entity
from game.projectile import Projectile

from arcade.physics_engines import _move_sprite

class Enemy(Entity):
    """A generic enemy class"""

    damage_sound = arcade.load_sound(constants.ENEMY_DAMAGE_SOUND)


    #TODO: the enemy should know where the player is at all times, and then alter behavior when the player is close enough. 

    def __init__(self, sprites: dict, path: str, scaling: int, position: tuple):

        super().__init__(sprites, path, scaling, position)

        self.time_counter = 0
        self.time_since_move = 0
        self.time_since_attack = 0
        self.power = 1
        #print("I live!")

    def update(self):
        """The generic update. What's happening to the enemy?"""
        super().update()
        if self.health <= 0:
            self.sprites["player"][0].score += 1
            self.kill()

    def get_distance_from_player(self):
        """Calculates the current distance from the player."""
        player_x = self.sprites["player"][0].center_x
        player_y = self.sprites["player"][0].center_y
        
        self._distance_x = ((player_x - self.center_x)**2)**(1/2)
        self._distance_y = ((player_y - self.center_y)**2)**(1/2)

    def collision_event(self, player):
        """What happens to the player when these two touch?"""
        player.take_damage(self.power)
        player.change_y = 2
        if self.center_x > player.center_x:
            player.change_x = -5
        else:
            player.change_x = 5

    def handle_movement(self):
        """Handles the movement and collision of the enemy."""
        player = self.sprites["player"][0]
        platforms = self.sprites["walls"]

        #Responsible for moving the entity and making sure that they collide with walls/platforms. 
        hit_list = _move_sprite(self, platforms, ramp_up=True)

    def take_damage(self, damage):
        """The method that gets called whenever the enemy takes damage."""
        super().take_damage(damage)
        arcade.play_sound(Enemy.damage_sound, constants.VOLUME_SFX*2)