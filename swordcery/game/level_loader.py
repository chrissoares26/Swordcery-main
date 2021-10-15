import game.constants as constants
import random
from game.player import Player
from game.block import Block
from game.enemy_slime import EnemySlime
from game.finish_line import FinishLine
from game.kill_block import KillBlock
from game.enemy_archer import EnemyArcher
from game.coin import Coin

class LevelLoader():

    def __init__(self, level):
        """Args:
            level: (str): a 2 digit string (00, 01, 02, etc.) level code."""
        

        self.level_path = f"swordcery/levels/level_{level}.csv"
        #self.level_key = "swordcery/levels/level_key.csv"
        # swordcery/levels

        self._init_level()

    def _init_level(self):
        with open(self.level_path, mode='r', encoding='utf-8-sig') as level_data:
            self._level_list = []
            width = 0
            height = 0
            for row in level_data:
                row = row.split(",")

                if width < len(row):
                    width = len(row)

                i = 0
                for item in row:
                    item = item.strip()
                    row[i] = item.lower() #Converts it to lower case, just in case. Ha. Ha. 
                    i += 1
                self._level_list.append(row)
            height = len(self._level_list)

            self._level_height = height*64
            self._level_width = width*64

    def load_level(self, director):
        """A callable method. Generates the sprite lists of the player, enemies, walls and objectives."""

        y = self._level_height

        for row in self._level_list:
            x = 0
            for tile in row:
                if tile != "": # immediately filter out all blank tiles
                    if tile == "w": #is the tile a wall?
                        wall = Block(constants.WALL_SPRITE, constants.TILE_SCALING, (x,y))
                        director.sprites["walls"].append(wall)

                    elif tile == "c": #is it a crate?
                        crate = Block(constants.OBSTACLE_SPRITE, constants.TILE_SCALING, (x,y))
                        director.sprites["walls"].append(crate)
                    
                    elif tile == "h":
                        hazard = KillBlock(constants.HAZARD_BLOCK,constants.TILE_SCALING, (x,y))
                        director.sprites["objectives"].append(hazard)

                    elif tile == "f":
                        finish_line = FinishLine(constants.FINISH_BLOCK,constants.TILE_SCALING, (x,y))
                        director.sprites["objectives"].append(finish_line)

                    elif tile == "p":
                        player = Player(director.sprites, constants.PLAYER_SPRITE, constants.CHARACTER_SCALING, (x,y))
                        director.sprites["player"].append(player)

                    elif tile == "s":
                        slime = EnemySlime(director.sprites, constants.ENEMY_SPRITE, constants.CHARACTER_SCALING, (x,y))
                        director.sprites["enemies"].append(slime)

                    elif tile == "r":
                        archer = EnemyArcher(director.sprites, constants.ENEMY_SPRITE, constants.CHARACTER_SCALING, (x,y))
                        director.sprites["enemies"].append(archer)
                    
                    elif tile == "o":
                        coin = Coin(constants.COIN_SPRITE, constants.TILE_SCALING, (x,y))
                        director.sprites["objectives"].append(coin)
                x += 64

            y -= 64

if __name__ == "__main__":
    level = LevelLoader(00)
    level._load_level()
    print(level._level_list)
    print(f"{level._level_width},{level._level_height}")