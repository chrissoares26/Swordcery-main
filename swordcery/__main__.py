import arcade
from game.instruction_screen import InstructionView
import game.constants as constants


def main():
    """ Main method """
    window = arcade.Window(constants.ScreenWidth, constants.ScreenHeight, constants.ScreenTitle)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()