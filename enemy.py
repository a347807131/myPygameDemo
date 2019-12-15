import pygame
from random import *

class S_enemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("images/S_enemy.png").convert_alpha()
        self.destroy_images=[]
        self.destroy_images.extend([\
            pygame.image.load("images/S_enemy_down_1.png").convert_alpha(),\
            pygame.image.load("images/S_enemy_down_2.png").convert_alpha(),\
            pygame.image.load("images/S_enemy_down_3.png").convert_alpha(),\
            pygame.image.load("images/S_enemy_down_4.png").convert_alpha() \
            ])

        self.rect=self.image.get_rect()
        self.width,self.height=bg_size[0],bg_size[1]
        self.speed=3
        self.active=True
        self.mask=pygame.mask.from_surface(self.image)

        self.rect.left,self.rect.top=\
                        randint(0,self.width-self.rect.width),\
                        randint(-5*self.height,0)
    def reset(self):
        self.rect.left,self.rect.top=\
                        randint(0,self.width-self.rect.width),\
                        randint(-5*self.height,0)
        self.active=True

    def move(self):
        if self.rect.top<self.height:
            self.rect.top+=self.speed
        else:
            self.reset()

class M_enemy(pygame.sprite.Sprite):
    HP=8

    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("images/M_enemy.png").convert_alpha()
        self.image_hit=pygame.image.load("images/M_enemy_hit.png").convert_alpha()
        self.destroy_images=[]
        self.destroy_images.extend([\
            pygame.image.load("images/M_enemy_down_1.png").convert_alpha(),\
            pygame.image.load("images/M_enemy_down_2.png").convert_alpha(),\
            pygame.image.load("images/M_enemy_down_3.png").convert_alpha(),\
            pygame.image.load("images/M_enemy_down_4.png").convert_alpha() \
                                ])

        self.rect=self.image.get_rect()
        self.width,self.height=bg_size[0],bg_size[1]
        self.speed=1
        self.active=True
        self.mask=pygame.mask.from_surface(self.image)
        self.HP=M_enemy.HP
        self.hit=False
        self.rect.left,self.rect.top=\
                        randint(0,self.width-self.rect.width),\
                        randint(-7*self.height,0)
    def reset(self):
        self.rect.left,self.rect.top=\
                        randint(0,self.width-self.rect.width),\
                        randint(-7*self.height,0)
        self.active=True
        self.HP=M_enemy.HP

    def move(self):
        if self.rect.top<self.height:
            self.rect.top+=self.speed
        else:
            self.reset()

class X_enemy(pygame.sprite.Sprite):
    HP=20

    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("images/X_enemy.png").convert_alpha()

        self.fly_images=[]
        self.fly_images.extend([\
            pygame.image.load("images/X_fly_1.png").convert_alpha(),\
            pygame.image.load("images/X_fly_2.png").convert_alpha(),\
            pygame.image.load("images/X_fly_3.png").convert_alpha(),\
            pygame.image.load("images/X_fly_4.png").convert_alpha(),\
            pygame.image.load("images/X_fly.png").convert_alpha() \
            ])
        self.fly_image_rect=self.fly_images[1].get_rect()
        self.destroy_images=[]
        self.destroy_images.extend([\
            pygame.image.load("images/me_down_1.png").convert_alpha(),\
            pygame.image.load("images/me_down_2.png").convert_alpha(),\
            pygame.image.load("images/me_down_3.png").convert_alpha(),\
            pygame.image.load("images/me_down_4.png").convert_alpha() \
            ])

        self.rect=self.image.get_rect()
        self.width,self.height=bg_size[0],bg_size[1]
        self.speed=1
        self.active=True
        self.mask=pygame.mask.from_surface(self.image)
        self.HP=X_enemy.HP
        self.hit=False
        self.rect.left,self.rect.top=\
                        randint(0,self.width-self.rect.width),\
                        randint(-10*self.height,0)
    def reset(self):
        self.rect.left,self.rect.top=\
                        randint(0,self.width-self.rect.width),\
                        randint(-10*self.height,0)
        self.HP=X_enemy.HP
        self.active=True

    def move(self):
        if self.rect.top<self.height:
            self.rect.top+=self.speed
        else:
            self.reset()
