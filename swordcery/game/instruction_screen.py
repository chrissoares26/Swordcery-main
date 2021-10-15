import arcade
import game.constants as constants
from game.director import Director

class InstructionView(arcade.View):

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, constants.ScreenWidth - 1, 0, constants.ScreenHeight - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Welcome to Swordcery", constants.ScreenWidth / 2, constants.ScreenHeight / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Use the arrow keys or A,W,S, and D to move and jump", (constants.ScreenWidth / 2), (constants.ScreenHeight / 2) - 40,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Use the space bar for the sword", (constants.ScreenWidth / 2), (constants.ScreenHeight / 2) - 80,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Use the enter key for the projectile", (constants.ScreenWidth / 2), (constants.ScreenHeight / 2) - 120,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Click to begin the game. Have fun!", constants.ScreenWidth / 2, constants.ScreenHeight / 2 - 160,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = Director()
        game_view.setup(0)
        self.window.show_view(game_view)