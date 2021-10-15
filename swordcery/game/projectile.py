import arcade
from game.entity import Entity
import game.constants as constants


class Projectile(Entity):
    """A projectile. Who knows what it does?"""

    projectile_sound = arcade.load_sound(constants.PROJECTILE_SOUND)


    def __init__(self, sprites: dict, path: str, scaling:int, position: tuple, velocity: tuple, power: int):
        super().__init__(sprites, path, scaling, position)

        self.change_x = velocity[0]
        self.change_y = velocity[1]
        self.power = power
        self.time_since_spawn = 0
        self.health = 1
        arcade.play_sound(Projectile.projectile_sound, constants.VOLUME_SFX)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.health <= 0:
            self.kill()
        pass

    def on_update(self, delta_time):
        self.time_since_spawn += delta_time
        if self.time_since_spawn > 5:
            self.kill()

    def collision_event(self, target):
        target.take_damage(self.power)
        target.change_y = 4
        if self.center_x > target.center_x:
            target.change_x = -3
        else:
            target.change_x = 3

        self.kill()