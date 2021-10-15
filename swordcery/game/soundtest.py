import arcade



SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Sound Tester"



class gamewindow(arcade.Window):
    def __init__(self):
        self.test_sound = arcade.load_sound(":resources:sounds/hit5.wav")

    def setup(self):
        arcade.play_sound(self.test_sound)


"""


"""
#Jump sound :resources:sounds/jump5.wav or 3
#Damage sound :resources:sounds/hurt3.wav
#Death sound :resources:sounds/gameover2.wav
#Enemy damage sound :resources:sounds/hurt2.wav
#Shooting sound :resources:sounds/hit3.wav
#Sword swing sound? :resources:sounds/rockHit2.wav or :resources:sounds/hit5.wav
    
window = gamewindow()
window.setup()
arcade.run()