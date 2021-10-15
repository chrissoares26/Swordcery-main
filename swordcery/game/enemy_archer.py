import arcade
import game.constants as constants
import random
from game.enemy import Enemy
from game.projectile import Projectile


class EnemyArcher(Enemy):
    def __init__(self, sprites: dict, path: str, scaling: int, position: tuple):
        super().__init__(sprites, path, scaling, position)
        self.speed = 5
        self.time_since_attack = 0

    def update(self):
        super().update()
        self.get_distance_from_player()
        if self._distance_x <= constants.ScreenWidth/2 and self._distance_y <= constants.ScreenHeight/2:
            self.change_y -= constants.GRAVITY
            self.center_y += self.change_y

            #Takes an imaginary step forward to test what's going to happen at the start of the tick.
            self.center_x += self.change_x
            next_step = self.collides_with_list(self.sprites["walls"])
            self.center_x -= self.change_x

            #Is the player too close?
            if self._distance_x < 375:
                #Is the player to my left or my right?
                if self.center_x > self.sprites["player"][0].center_x:
                    self.change_x = self.speed
                else:
                    self.change_x = -self.speed
                
            elif self._distance_x > 425:
                if self.center_x > self.sprites["player"][0].center_x:
                    self.change_x = -self.speed
                else:
                    self.change_x = self.speed
                    
            else:
                self.change_x = 0 #Stop moving if in the sweet spot

            if len(next_step) == 0: #If the enemy would have fallen off of a cliff this turn, it tries to turn around.
                #print("I almost fell!")
                if self.center_x > self.sprites["player"][0].center_x:
                    self.center_x -= abs(self.change_x) #If there's a cliff in front of the enemy and the player is to the left, it will try to take a step towards the player.
                elif self.center_x < self.sprites["player"][0].center_x:
                    self.center_x += abs(self.change_x)

            #Goes through with whatever movement was planned.
            hit_list = self.handle_movement()

    def on_update(self, delta_time):
        """Handles the attacks."""
        if self._distance_x <= 750 and self._distance_y <= 250:
            self.ranged_attack(delta_time)

    def ranged_attack(self, delta_time):

        """The enemy will try to attack."""

        player = self.sprites["player"][0]

        # check if player is nearby
        # if so, shoot projectile
        self.time_since_attack += delta_time

        #How quickly will it fire a projectile?
        modifier = 1
        if self._distance_x < 425:
            modifier = 0.6
        elif self._distance_x < 375:
            modifier = 0.3
        interval = 2*modifier

        if self.time_since_attack > interval: 
            #print("trying to attack...")
            self.time_since_attack = 0
            #print("projectile launched")
            #Which way does it shoot?
            if player.center_x > self.center_x:
                velocity = (constants.PROJECTILE_VELOCITY*2, 0)
            else:
                velocity = (-(constants.PROJECTILE_VELOCITY)*2, 0)

            projectile = Projectile(self.sprites, constants.PROJECTILE_SPRITE, constants.CHARACTER_SCALING * 0.5, self.position, velocity, self.power)
            self.sprites["projectiles"].append(projectile)