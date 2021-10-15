import arcade
import game.constants as constants
from game.entity import Entity
from game.player_melee import PlayerMelee
from game.projectile import Projectile
from game.player_range_shot import Player_Range_Shot


class Player(Entity):
    """The player class."""

    damage_sound = arcade.load_sound(constants.PLAYER_DAMAGE_SOUND)
    jump_sound = arcade.load_sound(constants.JUMP_SOUND)

    #TODO: player swing deletes projectiles

    def __init__(self, sprites: dict, path, scaling, position):
        super().__init__(sprites, path, scaling, position)
        self.damaged_time_count = 0
        self._took_damage = False
        self.last_direction = 1
        self.power = 1
        self._set_sword_position()
        self.has_won = False
        self.currently_attacking = False
        self.can_attack = True
        self.melee_cooldown = 0.5
        self.melee_time_count = 0

        self.magic_max = 5
        self.magic_current = self.magic_max
        self.magic_time_count = 0

        self.magic_regen = 2

        self.score = 0

        # improved movement config
        self.landing_lag = 3 # frames before player can jump again after landing
        self.jump_lag = 20 # frames before player can jump again after jumping
        self.jump_boost = 30 # frames after jumping where holding jump reduces gravity for higher jumps
        self.jump_boost_gravity_multiplier = 0.35
        self.horizontal_friction: float = 0.95
        self.vertical_friction: float = 0.99
        self.surface_friction: float = 0.1

        # improved movement
        self.jump_boost_time = 0 # frames until jump boost runs out
        self.ground_time = 0 # frames since player has landed
        self.jump_time = 0 # frames since player has jumped last
        self.can_jump = False # is set by the director, enables jumping
        self.input_state = {"up": False, "down": False, "left": False, "right": False} # used to keep track of held keys
        self.horizontal_acceleration: float = 0.0 # horizontal movement speed, can accumulate across ticks
        self.vertical_acceleration: float = 0.0 # vertical movement speed, can accumulate across ticks

        # Load textures for idle standing
        self.idle_texture_pair = self.load_texture_pair(f"{constants.PLAYER_SPRITE_BASE_PATH}_idle.png")

         # Default to face-right
        self.character_face_direction = constants.RIGHT_FACING_INDEX

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = constants.CHARACTER_SCALING
        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = self.load_texture_pair(f"{constants.PLAYER_SPRITE_BASE_PATH}_walk{i}.png")
            self.walk_textures.append(texture)
            #print(f"{constants.PLAYER_SPRITE_BASE_PATH}_walk{i}.png")
    
    def load_texture_pair(self, filename):
        """
        Load a texture pair, with the second being a mirror image.
        """
        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True)
        ]
        
    def update_animation(self, delta_time: float = 1/60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == constants.RIGHT_FACING_INDEX:
            self.character_face_direction = constants.LEFT_FACING_INDEX
        elif self.change_x > 0 and self.character_face_direction == constants.LEFT_FACING_INDEX:
            self.character_face_direction = constants.RIGHT_FACING_INDEX

        """# Idle animation
        if self.currently_attacking:
            self.cur_texture += 1
            if self.cur_texture > 7 * constants.UPDATES_PER_FRAME:
                self.cur_texture = 0
                self.currently_attacking = False
            frame = self.cur_texture // constants.UPDATES_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.
            return"""

        # Walking animation
        self.cur_texture += abs(self.horizontal_acceleration) if self.can_jump else 0
        self.cur_texture %= 7 * constants.UPDATES_PER_FRAME # wrap value around
        frame = int(self.cur_texture // constants.UPDATES_PER_FRAME)
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]

        # Idle animation
        if abs(self.horizontal_acceleration) < constants.STANDING_STILL_THRESHOLD and abs(self.vertical_acceleration) < constants.STANDING_STILL_THRESHOLD and self.can_jump:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

    def update(self):
        """Updates the player. What are they doing?"""
        super().update()
        self._handle_collisions()
        self._set_sword_position()
        #print("am I updating?")
        pass

    def on_update(self, delta_time: float=1/60):
        """Code that repeats in however many seconds."""
        self.ground_time += self.can_jump
        self.jump_time += 1

        # player movement

        if self.change_x == 0:
            self.horizontal_acceleration *= self.surface_friction
        if self.change_y == 0:
            self.vertical_acceleration *= self.surface_friction

        self.horizontal_acceleration += constants.PLAYER_MOVEMENT_SPEED * constants.PLAYER_MOVEMENT_SPEED * (self.input_state["right"] - self.input_state["left"])
        self.vertical_acceleration += constants.PLAYER_MOVEMENT_SPEED * constants.PLAYER_MOVEMENT_SPEED * (0 - self.input_state["down"]) # ignore up key otherwise player can fly lol
        if self.input_state["up"]:
            if self.can_jump and self.ground_time > self.landing_lag and self.jump_time > self.jump_lag:
                self.vertical_acceleration = constants.PLAYER_JUMP_HEIGHT
                self.cur_texture = 1
                arcade.play_sound(self.jump_sound, constants.VOLUME_SFX * 0.8)
                self.ground_time = 0
                self.jump_time = 0
                self.jump_boost_time = self.jump_boost
                self.can_jump = False #HACK: idk if this is effective, might want to remove it

        if self.input_state["up"] and self.jump_boost_time > 0 and not self.can_jump:
            self.vertical_acceleration -= constants.GRAVITY * self.jump_boost_gravity_multiplier
        elif not self.can_jump:
                self.vertical_acceleration -= constants.GRAVITY
        self.jump_boost_time -= 1

        self.vertical_acceleration *= self.vertical_friction
        self.horizontal_acceleration *= self.horizontal_friction

        self.change_x = min(constants.PLAYER_MAXIMUM_HORIZONTAL_SPEED, max(-constants.PLAYER_MAXIMUM_HORIZONTAL_SPEED, self.horizontal_acceleration))
        self.change_y = min(constants.PLAYER_MAXIMUM_VERTICAL_SPEED, max(-constants.PLAYER_MAXIMUM_VERTICAL_SPEED, self.vertical_acceleration))

        # other stuff
        if self._took_damage:
            #print("took damage")
            self.damaged_time_count += delta_time
            if 0.5 > self.damaged_time_count > 0.4:
                pass
                #stops the player from sliding
            if self.damaged_time_count > 1.5: #The invulnerability window
                self._took_damage = False
                self.damaged_time_count = 0
                #print("No longer invulnerable")
        
        #The melee cooldown handler.
        if not self.can_attack:
            self.melee_time_count += delta_time
            if self.melee_time_count >= self.melee_cooldown:
                self.can_attack = True
                self.melee_time_count = 0
        
        if self.magic_current < self.magic_max:
            self.magic_time_count += delta_time
            if self.magic_time_count >= self.magic_regen:
                self.magic_current += 1
                self.magic_time_count = 0


    def _handle_collisions(self):
        """Tests to see if the player is colliding with another entity."""
        for key in self.sprites:
            if key != "walls" and key != "player" and key!= "sword" and key != "shooter" and key != "objectives" and not self._took_damage: 
                #print(key)
                for sprite in self.sprites[key]:
                    if self.collides_with_sprite(sprite):
                        #print(f"collision with {sprite}")
                        sprite.collision_event(self)
                        self._took_damage = True
                        arcade.play_sound(Player.damage_sound, constants.VOLUME_SFX)
            elif key == "objectives":
                for sprite in self.sprites[key]:
                    if self.collides_with_sprite(sprite):
                        sprite.collision_event(self)
            elif key == "walls":
                pass


    def _set_sword_position(self):
        
        if self.last_direction > 0:
            x = self.center_x + self.width/2
        else:
            x = self.center_x - self.width/2
        y = self.center_y
        
        self.sword_position = (x,y)
            

    def attack(self):
        """The basic attack method, spawns a hitbox in front of the player that damages enemies."""

        #print(position)
        if self.can_attack:
            self.currently_attacking = True
            sword = PlayerMelee(self.sprites, constants.MELEEE_SPRITE, 1, self.sword_position, self.last_direction, self.power)
            self.sprites["sword"].append(sword)
            self.can_attack = False

    def ranged_attack(self):
        """Secondary attack method, allows the player to shoot projectiles at range."""
        if self.magic_current > 0:
            self.magic_current -= 1
            if self.last_direction > 0:
                velocity = (constants.PLAYER_PROJECTILE_VELOCITY, 0)
            else:
                velocity = (-(constants.PLAYER_PROJECTILE_VELOCITY), 0)
            shooter = Player_Range_Shot(self.sprites, constants.RANGE_SPRITE, constants.CHARACTER_SCALING*(1/2), self.position, velocity, self.power)
            self.sprites["shooter"].append(shooter)