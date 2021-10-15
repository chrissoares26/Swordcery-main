import arcade
import game.constants as constants
import random
from game.level_loader import LevelLoader


class Director(arcade.View):
    """Main director class"""
    death_sound = arcade.load_sound(constants.PLAYER_DEATH_SOUND)
    bgm = arcade.load_sound(constants.BGM)
    arcade.play_sound(bgm, constants.VOLUME_BGM, looping=True)

    total_score = 0

    def __init__(self):

        super().__init__()
        self.window.set_mouse_visible(False)

        self.sprites = {}
        
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.physics_engine = None

    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """

        self.level = level
        
        # Create the Sprite lists

        self.sprites["player"] = arcade.SpriteList()
        self.sprites["enemies"] = arcade.SpriteList()
        self.sprites["walls"] = arcade.SpriteList(use_spatial_hash=True)
        self.sprites["objectives"] = arcade.SpriteList(use_spatial_hash=True)
        self.sprites["projectiles"] = arcade.SpriteList()
        self.sprites["sword"] = arcade.SpriteList()
        self.sprites["shooter"] = arcade.SpriteList()

        # Shows Winning Screen if the player finishes all the levels
        if self.level == 5:
            view = WinningView(self.level)
            self.window.show_view(view)

        level_loader = LevelLoader(level)
        level_loader.load_level(self)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.sprites["player"][0], self.sprites["walls"], constants.GRAVITY)


        # Displays the current health
        self.view_bottom = 0
        self.view_left = 0

    def add_enemy(self, delta_time):
        new_badguy = Enemy(self.sprites, constants.ENEMY_SPRITE, constants.CHARACTER_SCALING, (random.randint(0,768),random.randint(0,400)))

        self.sprites["enemies"].append(new_badguy)
    
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W: # jump
            self.sprites["player"][0].input_state["up"] = True
        elif key == arcade.key.DOWN or key == arcade.key.S: # fast-fall
            self.sprites["player"][0].input_state["down"] = True
        elif key == arcade.key.LEFT or key == arcade.key.A: # left
            self.sprites["player"][0].input_state["left"] = True
            self.sprites["player"][0].last_direction = -1 # which way is the player facing?
        elif key == arcade.key.RIGHT or key == arcade.key.D: # right
            self.sprites["player"][0].input_state["right"] = True
            self.sprites["player"][0].last_direction = 1 # which way is the player facing?

        elif key == arcade.key.SPACE:
            self.sprites["player"][0].attack()
        elif key == arcade.key.ENTER or key == arcade.key.RETURN:
            self.sprites["player"][0].ranged_attack()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.sprites["player"][0].input_state["up"] = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.sprites["player"][0].input_state["down"] = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.sprites["player"][0].input_state["left"] = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.sprites["player"][0].input_state["right"] = False

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player with the physics engine
        self.sprites["player"][0].can_jump = self.physics_engine.can_jump()
        self.physics_engine.update()

        for sprite_list in self.sprites.values():
            for sprite in sprite_list:
                #if not isinstance(sprite, Player):
                sprite.update()
                sprite.on_update(delta_time)
                sprite.update_animation(delta_time)
                
        if (self.sprites["player"][0].has_won):
            #Adds the level score to the total score
            Director.total_score += self.sprites["player"][0].score
            # Advances to next level if player finishes the level
            if self.level <= 4:
                self.level += 1
                self.setup(self.level)
        elif (self.sprites["player"][0].health <= 0):
            self.setup(self.level)
            arcade.play_sound(Director.death_sound, constants.VOLUME_SFX)
            view = GameOverView(self.level)
            self.window.show_view(view)
        self.handle_scroll()


    def on_draw(self):
        arcade.start_render()
        #Code to draw the screen goes here
        for sprite_list in self.sprites.values():
            sprite_list.draw()
        # Draw our score on the screen, scrolling it with the viewport
        player_health = self.sprites["player"][0].health
        player_magic = self.sprites["player"][0].magic_current
        player_score = self.sprites["player"][0].score
        total_score = Director.total_score
        magic_text = f"Magic: {player_magic}"
        health_text = f"Health: {player_health}"
        level_score_text = f"Level Score: {player_score}"
        total_score_text = f"Total Score: {total_score}"

        arcade.draw_text(health_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)      
        arcade.draw_text(magic_text, 10 + self.view_left, 30 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)
        arcade.draw_text(level_score_text, 120 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)
        arcade.draw_text(total_score_text, 120 + self.view_left, 30 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)

    def draw_walls(self):
        pass

    def handle_scroll(self):
        changed = False
        player_sprite = self.sprites["player"][0]

        # Scroll left
        left_boundary = self.view_left + constants.LEFT_VIEWPORT_MARGIN
        if player_sprite.left < left_boundary:
            self.view_left -= left_boundary - player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + constants.ScreenWidth - constants.RIGHT_VIEWPORT_MARGIN
        if player_sprite.right > right_boundary:
            self.view_left += player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + constants.ScreenHeight - constants.TOP_VIEWPORT_MARGIN
        if player_sprite.top > top_boundary:
            self.view_bottom += player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + constants.BOTTOM_VIEWPORT_MARGIN
        if player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                constants.ScreenWidth + self.view_left,
                                self.view_bottom,
                                constants.ScreenHeight + self.view_bottom)


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self, level):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture(constants.DEATH_IMAGE)
        self.level = level

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.set_viewport(0, constants.ScreenWidth, 0, constants.ScreenHeight)
        self.texture.draw_sized(constants.ScreenWidth/ 2, constants.ScreenHeight / 2,
                                constants.ScreenWidth, constants.ScreenHeight)
        arcade.draw_text(f"Final Score: {Director.total_score}", constants.ScreenWidth / 2 + 184, constants.ScreenHeight - 210,
                         arcade.color.WHITE, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        if Director.total_score != 0:
            if Director.total_score > 1:
                Director.total_score -= 2
            elif Director.total_score == 1:
                Director.total_score -= 1
            else:
                Director.total_score == 0
        game_view = Director()
        game_view.setup(self.level)
        self.window.show_view(game_view)




class WinningView(arcade.View):
    """ View to show when game is over """

    def __init__(self, level):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture(constants.DEATH_IMAGE)
        self.level = level

        arcade.set_background_color(arcade.csscolor.CRIMSON)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.

    def on_draw(self):
        """ Draw this view """
        arcade.set_viewport(0, constants.ScreenWidth, 0, constants.ScreenHeight)
        arcade.start_render()
        arcade.draw_text("You Won!", constants.ScreenWidth / 2, constants.ScreenHeight / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to restart the game", constants.ScreenWidth / 2, constants.ScreenHeight / 2 - 160,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text(f"Final Score: {Director.total_score}", constants.ScreenWidth / 2, constants.ScreenHeight / 2 - 120,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        # self.texture.draw_sized(constants.ScreenWidth/ 2, constants.ScreenHeight / 2,
        #                         constants.ScreenWidth, constants.ScreenHeight)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = Director()
        game_view.setup(00)
        self.window.show_view(game_view)