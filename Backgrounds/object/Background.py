import pygame
import os

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location,scr_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('Backgrounds/graphics',image_file))
        self.image = pygame.transform.scale(self.image,scr_size)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location