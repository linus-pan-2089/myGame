import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        #load image and setup image properties
        self.image = pygame.image.load('images/alien.bmp')
        #self.image = pygame.image.load('images/TAlien.png')
        self.rect = self.image.get_rect()
        
        #place alien to northwest corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #store alien's precision place
        self.x = float(self.rect.x)
        
    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
        
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right or self.rect.left <= screen_rect.left)