import arcade
import game.constants as constants

class Entity(arcade.Sprite):

    def __init__(self, sprites: dict, path: str, scaling:int, position: tuple):

        super().__init__(path, scaling)

        self.sprites = sprites
        self.position = position
        self.health = constants.ENTITY_HEALTH
        self.initial_color = self._get_color()
        self.damage_color = (self.initial_color[0],self.initial_color[1]-60,self.initial_color[2]-60)
        self._color_tick = 0

    def collision_event(self, target):
        """Defines what event is triggered when the player collides with it."""
        pass


    def update(self):
        if self.center_y <= -512: #if the player falls more than 8 tiles below the level, they will die.
            self.health = 0
        if self._color != self.initial_color:
            self._color_tick += 1
            if self._color_tick == 5: #After 10 update ticks, reset the color.
                self._set_color(self.initial_color)
                self._color_tick = 0

    def take_damage(self, damage):
        """The method that gets called whenever an entity takes damage."""
        self.health -= damage
        self._set_color(self.damage_color)