import pygame

class Myplane(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1=pygame.image.load("images/me_1.png").convert_alpha()
        self.image2=pygame.image.load("images/me_2.png").convert_alpha()
        self.rect=self.image1.get_rect()
        self.width,self.height=bg_size[0],bg_size[1]
        self.rect.left,self.rect.top=\
                        (self.width-self.rect.width)//2,\
                        self.height-self.rect.height-60

        self.invincible_image=pygame.image.load("images/invincible.png").convert_alpha()
        self.invincible_image_rect=self.invincible_image.get_rect()

        self.destroy_images=[]
        self.destroy_images.extend([\
            pygame.image.load("images/me_down_1.png").convert_alpha(),\
            pygame.image.load("images/me_down_2.png").convert_alpha(),\
            pygame.image.load("images/me_down_3.png").convert_alpha(),\
            pygame.image.load("images/me_down_4.png").convert_alpha() \
                                ])

        self.speed=10
        self.active=True
        self.invincible=False
        self.masks=[pygame.mask.from_surface(self.image1),pygame.mask.from_surface(self.invincible_image)]
        self.mask=self.masks[0]

    def reset(self):
        self.rect.left,self.rect.top=\
                        (self.width-self.rect.width)//2,\
                        self.height-self.rect.height-60

        self.active=True

    def move(self,direction):
        if direction=="Up":
            if self.rect.top>0:
                self.rect.top-=self.speed
            else:
                self.rect.top=0
        elif direction=="Down":
            if self.rect.bottom<self.height-60:
                self.rect.top+=self.speed
            else:
                self.rect.bottom=self.height-60
        elif direction=="Left":
            if self.rect.left>0:
                self.rect.left-=self.speed
            else:
                self.rect.left=0

        elif direction=="Right":
            if self.rect.right<self.width:
                self.rect.right+=self.speed
            else:
                self.rect.right=self.width
