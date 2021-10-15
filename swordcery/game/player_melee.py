from game.entity import Entity
import arcade
import game.constants as constants

class PlayerMelee(Entity):
    """An entity that appears in front of the player whenever they do an attack."""

    melee_sound = arcade.load_sound(constants.MELEE_SOUND)

    def __init__(self, sprites: dict, path: str, scaling:int, position: tuple, direction: int, power: int):
        super().__init__(sprites, path, scaling, position)

        self.direction = direction
        self.power = power
        self.time_counter = 0
        #Flips the sprite left if the player is facing left.
        if self.direction < 0:
            self.texture = arcade.load_texture(path, flipped_horizontally=True)
        
        self.has_dealt_damage = False
        
        arcade.play_sound(PlayerMelee.melee_sound, constants.VOLUME_SFX)

    def update(self):
        if not self.has_dealt_damage:
            for key in self.sprites:
                if key != "player" and key != "walls" and key != "sword" and key != "shooter" and key != "objectives":
                    for sprite in self.sprites[key]:
                        if self.collides_with_sprite(sprite):
                            sprite.take_damage(self.power)
                            self.has_dealt_damage = True
        self.position = self.sprites["player"][0].sword_position

    def on_update(self, delta_time):
        self.time_counter += delta_time
        if self.time_counter > 0.2:
            self.kill()

  