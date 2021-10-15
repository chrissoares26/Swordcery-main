import arcade


class Block(arcade.Sprite):


    def __init__(self, path, scaling, position):
        super().__init__(path,scaling)

        self.position = position