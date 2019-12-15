import pygame

class Bullet1(pygame.sprite.Sprite):
    def __init__(self,position):
        self.image=pygame.image.load("images/bullet1.png").convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=position
        self.speed=12
        self.active=False
        self.mask=pygame.mask.from_surface(self.image)

    def reset(self,position):
        self.rect.center=position
        self.active=True


    def move(self):
        self.rect.top-=self.speed

        if self.rect.bottom<0:
            self.active=False

class Bullet2(pygame.sprite.Sprite):
    def __init__(self,position):
        self.image=pygame.image.load("images/bullet2.png").convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=position
        self.speed=12
        self.active=False
        self.mask=pygame.mask.from_surface(self.image)

    def reset(self,position):
        self.rect.center=position
        self.active=True


    def move(self):
        self.rect.top-=self.speed

        if self.rect.bottom<0:
            self.active=False
