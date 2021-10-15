import arcade
from game.projectile import Projectile


class Player_Range_Shot(Projectile):
    """A projectile fired from the player from a range."""



    def __init__(self, sprites: dict, path: str, scaling:int, position: tuple, velocity: tuple, power: int):
        super().__init__(sprites, path, scaling, position, velocity, power)

        # self.direction = direction
        self.change_x = velocity[0]
        self.change_y = velocity[1]
        self.power = power
        self.time_since_spawn = 0
        self.change_angle = 5
       
    def update(self):
        self.angle += self.change_angle
        self.center_x += self.change_x
        self.center_y += self.change_y
        for key in self.sprites:
            if key != "player" and key != "walls" and key != "sword" and key != "shooter" and key!= "objectives" and key != "projectiles":
                for sprite in self.sprites[key]:
                    if self.collides_with_sprite(sprite):
                        sprite.take_damage(self.power)
                        self.kill()

    def on_update(self, delta_time):
        self.time_since_spawn += delta_time
        if self.time_since_spawn > 0.9:
            self.kill()

    def collision_event(self, target):
        target.take_damage(self.power)
        target.change_y = 4
        if self.center_x > target.center_x:
            target.change_x = -3
        else:
            target.change_x = 3

        
        self.kill()