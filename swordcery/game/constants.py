ScreenWidth = 1000
ScreenHeight = 650
ScreenTitle = "Swordcery"

CHARACTER_SCALING = 0.98
TILE_SCALING = 0.5
COIN_SCALING = 0.5

PLAYER_SPRITE = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
PLAYER_SPRITE_BASE_PATH = ":resources:/images/animated_characters/female_adventurer/femaleAdventurer"
PLAYER_JUMP = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_jump.png"
WALL_SPRITE = ":resources:images/tiles/grassMid.png"
OBSTACLE_SPRITE = ":resources:images/tiles/boxCrate_double.png"
ENEMY_SPRITE = ":resources:images/enemies/slimeBlock.png"
PROJECTILE_SPRITE = ":resources:images/enemies/wormGreen_dead.png"
PROJECTILE_VELOCITY = 3
PLAYER_PROJECTILE_VELOCITY = 8
DEATH_IMAGE = "swordcery/assets/images/items/gravestone.png"
COIN_SPRITE = ":resources:images/items/coinGold.png"

UPDATES_PER_FRAME = 20 # Base player walk animation speed
STANDING_STILL_THRESHOLD = 0.5 # How slow the player can be moving in order to get an idle animation

# Used to flip the player sprite right or left
RIGHT_FACING_INDEX = 0
LEFT_FACING_INDEX = 1

PLAYER_MOVEMENT_SPEED = 0.8
PLAYER_MAXIMUM_HORIZONTAL_SPEED = 56
PLAYER_MAXIMUM_VERTICAL_SPEED = 64
PLAYER_JUMP_HEIGHT = 15.35
GRAVITY = 1.25
MELEEE_SPRITE = ":resources:images/items/keyRed.png"
RANGE_SPRITE = ":resources:images/items/star.png"

LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 375
TOP_VIEWPORT_MARGIN = 50
BOTTOM_VIEWPORT_MARGIN = 100

ENTITY_HEALTH = 3

HAZARD_BLOCK = ":resources:images/tiles/spikes.png"
FINISH_BLOCK = ":resources:images/tiles/signExit.png"

VOLUME_BGM = 0.10
VOLUME_SFX = 0.50

BGM = "swordcery/assets/sounds/bgm/adventure-meme-by-kevin-macleod-from-filmmusic-io.mp3"
JUMP_SOUND =  ":resources:sounds/jump5.wav"
PLAYER_DAMAGE_SOUND =  ":resources:sounds/hurt3.wav"
PLAYER_DEATH_SOUND =  ":resources:sounds/gameover2.wav"
ENEMY_DAMAGE_SOUND = ":resources:sounds/hurt2.wav"
PROJECTILE_SOUND =  ":resources:sounds/hit3.wav"
MELEE_SOUND = ":resources:sounds/hit5.wav"
COIN_SOUND = ":resources:sounds/coin5.wav"