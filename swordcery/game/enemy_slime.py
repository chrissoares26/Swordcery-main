import arcade
import game.constants as constants
import random
from game.enemy import Enemy
from game.projectile import Projectile


class EnemySlime(Enemy):
    def __init__(self, sprites: dict, path: str, scaling: int, position: tuple):
        super().__init__(sprites, path, scaling, position)

    def update(self):
        #Is this enemy nearby? If so, update gravity.
        super().update()
        
        self.get_distance_from_player()

        if self._distance_x <= constants.ScreenWidth/2 and self._distance_y <= constants.ScreenHeight/2:
            self.change_y -= constants.GRAVITY
            self.center_y += self.change_y

            hit_list = self.handle_movement()

    def on_update(self, delta_time: float):
        """For timed things, like turning around."""
        #Is the player on screen with me?
        
        #if self._distance_x <= constants.ScreenWidth and self._distance_y <= constants.ScreenHeight:
        if self._distance_x <= constants.ScreenWidth/2 and self._distance_y <= constants.ScreenHeight/2:
            self.jump_move(delta_time)

        #Is the player within 750 pixels (3/4 of the screen?) If yes, shoot.
        if self._distance_x <= 750 and self._distance_y <= 250:
            self.ranged_attack(delta_time)
        
    def jump_move(self, delta_time):
        """A jump move."""
        self.time_since_move += delta_time
        if self.time_since_move >= 5:
            self.change_y = 10
            self.change_x = random.randint(5,15) * random.choice([-1,1])
            self.time_since_move = 0
        if self.change_y == 0 and self.change_x != 0:
            self.change_x *= 2/3
            if abs(self.change_x) < 0.5:
                self.change_x = 0

    def ranged_attack(self, delta_time):

        """The enemy will try to attack."""

        player = self.sprites["player"][0]

        # check if player is nearby
        # if so, shoot projectile
        self.time_since_attack += delta_time
        if self.time_since_attack > 3: 
            #print("trying to attack...")
            self.time_since_attack = 0
            #print("projectile launched")
            #Which way does it shoot?
            if player.center_x > self.center_x:
                velocity = (constants.PROJECTILE_VELOCITY, 0)
            else:
                velocity = (-(constants.PROJECTILE_VELOCITY), 0)

            projectile = Projectile(self.sprites, constants.PROJECTILE_SPRITE, constants.CHARACTER_SCALING*(1/2),self.position, velocity, self.power)
            self.sprites["projectiles"].append(projectile)
            
        #else:
            #print("too far away")