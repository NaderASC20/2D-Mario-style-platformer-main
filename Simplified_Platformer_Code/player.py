import pygame
from tiles import Tile
class Player(pygame.sprie.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image-pygame.Surface((34,64))
        self.image.fill('red')
        self.rect=self.image.get_rect(topLeft=pos)


