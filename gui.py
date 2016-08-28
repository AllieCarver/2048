"""
2048 GUI
"""
import os, sys
import math
import pygame
from pygame.locals import *

#initilize pygame
pygame.init()

# Tile Images constants
IMAGENAME = "2048.png"
TILE_SIZE = 100
HALF_TILE_SIZE = TILE_SIZE / 2
BORDER_SIZE = 45

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


def load_image(name, colorkey=None, alpha=False):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class GUI:
    """
    Class to run 2048 GUI.
    """

    def __init__(self, game):
        self._rows = game.get_grid_height()
        self._cols = game.get_grid_width()
        self._height = self._rows * TILE_SIZE + 2 * BORDER_SIZE
        self._width = self._cols * TILE_SIZE + 2 * BORDER_SIZE 
        self._message = game.get_message()
        self._message_colors = {"2048!":'#EEE600',"Game Over":"Red","":"Black"}
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._screen_rect = self._screen.get_rect()
        pygame.display.set_caption('2048')
        self._background = pygame.Surface((self._width, self._height))
        self._background.fill((188, 173, 161))
        self._center_height = (self._rows * TILE_SIZE + 2 * BORDER_SIZE)/2
        self._center_width = (self._cols * TILE_SIZE + 2 * BORDER_SIZE)/2
        self._game = game
        self._tiles_sprite, dummy_rect  = load_image(IMAGENAME, alpha=True)
        self._tiles = []
        self.make_tiles()
        self._2048screen, dummy_rect = load_image('win.png', alpha=True)
        self._gameoverscreen, dummy_rect = load_image('gameover.png', alpha=True)
        self._loadscreen, dummy_rect = load_image('loadscreen.png', alpha=True)
        self._directions = {"up": UP, "down": DOWN,
                            "left": LEFT, "right": RIGHT}

    def make_tiles(self):
        """
        subsurface tiles sprite sheet for individual tiles
        """
        #subsurface is rect(left, top, width, height)
        images_in_sprite = 14
        for idx in xrange(14):
            self._tiles.append(self._tiles_sprite.subsurface(
                (idx * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)))
            
    def keydown(self, event):
        """
        Keydown handler
        """

        key = event.key
        if key == K_ESCAPE:
            sys.exit()
        elif key == K_n:
            self._game.reset()
        elif key == K_m:
            self._game.reset_2048_mode()
        elif key == K_u:
            try:
                self._game.undo()
            except KeyError:
                pass
        elif key == K_UP:
            self._game.move(UP)
        elif key == K_DOWN:
            self._game.move(DOWN)
        elif key == K_LEFT:
            self._game.move(LEFT)
        elif key == K_RIGHT:
            self._game.move(RIGHT)
        if self._game.get_message():
            if not self._game._continued:
                if self._game._2048:
                    if key == K_c:
                        self.keep_going()
            if self._game.get_message() == 'first load':
                if key == K_RETURN:
                    self._game.reset()
            

    def update(self):
        """
        update gui
        """

        for row in range(self._rows):
            for col in range(self._cols):
                tile = self._game.get_tile(row, col)
                if tile == 0:
                    val = 0
                else:
                    val = int(math.log(tile, 2))
                try:
                    self._screen.blit(self._tiles[val],
                        (col * TILE_SIZE + BORDER_SIZE,
                        row * TILE_SIZE + BORDER_SIZE))
                except IndexError:
                    self._screen.blit(self._tiles[0],
                        (col * TILE_SIZE + BORDER_SIZE,
                        row * TILE_SIZE + BORDER_SIZE))
        self._message = self._game.get_message()
        
            
    def main(self):
        """
        main game loop
        """

        clock = pygame.time.Clock()
        while 1:
            clock.tick(30)
            self._screen.blit(self._background, self._screen_rect)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.keydown(event)

            #redraw tiles in new positions        
            self.update()
            
            if self._game.get_message():
                if self._game._2048:
                    if not self._game._continued:
                        self._screen.blit(self._2048screen, self._screen_rect)
                elif self._game.get_message() == 'Game Over':
                    self._screen.blit(self._gameoverscreen, self._screen_rect)
                else:
                    self._screen.blit(self._loadscreen, self._screen_rect)
                    
            pygame.display.flip()
 
    def keep_going(self):
        self._game._continued = True
        self._game._message = ''

    def undo(self):
        if self._game._message != "Game Over":
            self._game.undo()
                
    def start(self):
        """
        Start the game.
        """
        self._game.reset()
        self._game._message = 'first load'
        self.main()
        
def run_gui(game):
    """
    Instantiate and run the GUI.
    """
    gui = GUI(game)
    gui.start()
