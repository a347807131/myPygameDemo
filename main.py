import pygame
import sys
import traceback
from pygame.locals import *
import myplane
import enemy
import bullet
import supply
import ground
from random import *


pygame.init()
pygame.mixer.init()

bg_size=width,height=480,700
screen=pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战--FishC Demo")

background1=ground.Back((0,700),bg_size)
background2=ground.Back((0,background1.rect.top),bg_size)

cloud1=ground.Cloud(bg_size)
cloud2=ground.Cloud(bg_size)

white=(0,0,0)
black=(0,0,0)
green=(0,255,0)
red=(255,0,0)
#载入游戏音乐
pygame.mixer.music.load("sounds/game_music.wav")
pygame.mixer.music.set_volume(0.2)
bullet_sound=pygame.mixer.Sound("sounds/bullet.wav")
bullet_sound.set_volume(0.2)
S_enemy_down=pygame.mixer.Sound("sounds/S_enemy_down.wav")
X_enemy_out=pygame.mixer.Sound("sounds/X_enemy_out.wav")
X_enemy_out.set_volume(0.2)
X_enemy_down=pygame.mixer.Sound("sounds/X_enemy_down.wav")
X_enemy_down.set_volume(0.2)
me_down=pygame.mixer.Sound("sounds/me_down.wav")
upgrade_sound=pygame.mixer.Sound("sounds/upgrade_sound.wav")
use_bomb_sound=pygame.mixer.Sound("sounds/use_bomb.wav")
get_supply_sound=pygame.mixer.Sound("sounds/get_supply.wav")
supply_sound=pygame.mixer.Sound("sounds/supply.wav")
game_over_sound=pygame.mixer.Sound("sounds/game_over.wav")

def add_S_enemies(group1,group2,num):
    for i in range(num):
        e1=enemy.S_enemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_M_enemies(group1,group2,num):
    for i in range(num):
        e2=enemy.M_enemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_X_enemies(group1,group2,num):
    for i in range(num):
        e3=enemy.X_enemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def inc_speed(target,inc):
    for each in target:
        each.speed+=inc


def main():
    pygame.mixer.music.play(-1)

    #生成我方飞机
    me=myplane.Myplane(bg_size)

    enemies=pygame.sprite.Group()

    #生成敌方小型飞机
    S_enemies=pygame.sprite.Group()
    add_S_enemies(S_enemies,enemies,15)
    #生成敌方中型飞机
    M_enemies=pygame.sprite.Group()
    add_M_enemies(M_enemies,enemies,5)
    #生成敌方大型飞机
    X_enemies=pygame.sprite.Group()
    add_X_enemies(X_enemies,enemies,2)

    #生成普通子弹
    bullet1=[]
    bullet1_index=0
    BULLET_NUM=5
    for i in range(BULLET_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    #生成超级子弹
    bullet2=[]
    double_bullet=False
    bullet2_index=0
    BULLET2_NUM=10
    for i in range(BULLET2_NUM//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx-33,me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx+30,me.rect.centery)))



    clock=pygame.time.Clock()

    #毁灭图片索引
    e1_destory_index=0
    e2_destory_index=0
    e3_destory_index=0
    me_destory_index=0

    #统计得分
    score=0


    #设置游戏难度
    level=1

    #设置全屏炸弹
    bomb_image=pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect=bomb_image.get_rect()
    bomb_num=3
    bomb_rect.left,bomb_rect.bottom=0,height

    #每10秒发放一个补给包
    bullet_supply=supply.Bullet_supply(bg_size)
    bomb_supply=supply.Bomb_supply(bg_size)
    SUPPLY_TIME=USEREVENT
    pygame.time.set_timer(SUPPLY_TIME,15*1000)

    #用于解除超级子弹状态定时器
    DOUBLE_BULLET_TIME=USEREVENT+1


    #用于切换我方飞机图片
    switch_image=True

    #用于绘制暂停按钮
    paused=False
    pause_image1=pygame.image.load("images/pause1.png").convert_alpha()
    pause_image=pygame.image.load("images/pause2.png").convert_alpha()
    pause_rect=pause_image.get_rect()
    pause_rect.right,pause_rect.top=width,0

    #生命数量
    life_num=3
    life_image=pygame.image.load("images/life_image.png").convert_alpha()
    life_rect=life_image.get_rect()
    life_rect.right,life_rect.bottom=width,height

    #用于绘制结束画面
    game_over_image1=pygame.image.load("images/game_over2.png").convert_alpha()
    game_over_image2=pygame.image.load("images/game_over1.png").convert_alpha()
    game_over_image_rect=game_over_image1.get_rect()
    game_over_image_rect.centerx,game_over_image_rect.centery=width/2,height/2


    #用于阻止重复打开recored
    recoreded=False

    #用于延迟
    delay=100

    running=True

    while running:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1 and pause_rect.collidepoint(event.pos):
                    paused= not paused
                    pause_image,pause_image1=pause_image1,pause_image

                elif event.button==1 and game_over_image_rect.collidepoint(event.pos) and life_num==0:
                    main()

            elif event.type==SUPPLY_TIME:
                if not paused:
                    supply_sound.play()
                    if choice([True,False]):
                        bomb_supply.reset()
                    else:
                        bullet_supply.reset()

            elif event.type==DOUBLE_BULLET_TIME:
                double_bullet=False
                pygame.time.set_timer(DOUBLE_BULLET_TIME,0)

            elif event.type==KEYDOWN:
                if event.key==K_SPACE:
                    if bomb_num:
                        bomb_num-=1
                        use_bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom>0:
                                each.active=False

        screen.blit(background1.image,background1.rect)
        screen.blit(background2.image,background2.rect)
        screen.blit(cloud1.image_s,cloud1.image_rect)
        screen.blit(cloud2.image_s,cloud2.image_rect)

        #绘制界面UI
        if life_num:
            #绘制暂停按钮
            screen.blit(pause_image,pause_rect)

            #绘制全屏炸弹示意图
            for i in range(bomb_num):
                bomb_rect.left=bomb_rect.left+i*bomb_rect.width
                screen.blit(bomb_image,bomb_rect)
                bomb_rect.left=0
            #绘制剩余生命示意图
            for i in range(life_num):
                life_rect.right=life_rect.right-i*life_rect.width
                screen.blit(life_image,life_rect)
                life_rect.right=width
            #绘制结束画面
        else:
            #停止播放背景音乐
            pygame.mixer.music.stop()
            #停止播放全部营销
            pygame.mixer.stop()
            #停止发放补给
            pygame.time.set_timer(SUPPLY_TIME,0)
            screen.blit(game_over_image1,game_over_image_rect)
            screen.blit(game_over_image2,(game_over_image_rect.left,game_over_image_rect.top+64))

            #读取历史最高得分
            if not recoreded:
                recoreded=True
                with open("record.txt","r") as f:
                    record_score=int(f.read())
                if score>record_score:
                    with open("record.txt","w") as f:
                        f.write(str(score))

        #根据用户的得分增加难度
        if level==1 and score==5000:
            level=2
            upgrade_sound.play()
            #增加 3架小型敌机、两两架中型敌机和一架大型敌机
            add_S_enemies(S_enemies,enemies,5)
            add_M_enemies(M_enemies,enemies,3)
            add_X_enemies(X_enemies,enemies,1)
            #提升小型敌机的速度
            inc_speed(S_enemies,1)
        elif level==2 and score>30000:
            level=3
            upgrade_sound.play()
            #增加3架小型敌机、两两架中型敌机和一架大型敌机
            add_S_enemies(S_enemies,enemies,5)
            add_M_enemies(M_enemies,enemies,3)
            add_X_enemies(X_enemies,enemies,1)
            #提升小型敌机的速度
            inc_speed(S_enemies,2)
            inc_speed(M_enemies,3)
        elif level==3 and score>100000:
            level=4
            upgrade_sound.play()
            #增加3架小型敌机、两两架中型敌机和一架大型敌机
            add_S_enemies(S_enemies,enemies,10)
            add_M_enemies(M_enemies,enemies,5)
            add_X_enemies(X_enemies,enemies,3)
            #提升小型敌机的速度
            inc_speed(S_enemies,1)
            inc_speed(M_enemies,1)




        if not paused and life_num:

            #背景移动
            background1.move()
            background2.move()
            cloud1.move()
            cloud2.move()

            #检测键盘输入
            key_pressed=pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.move("Up")
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.move("Down")
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.move("Left")
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.move("Right")

            #用于设置护盾
            if key_pressed[K_LCTRL] or key_pressed[K_RCTRL]:
                me.invincible=True
            else:
                me.invincible=False


            #绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    get_supply_sound.play()
                    if bomb_num<3:
                        bomb_num+=1
                    bomb_supply.active=False
            #超级子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    get_supply_sound.play()
                    double_bullet=True
                    bullet_supply.active=False
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,5*1000)

            #发射子弹
            if not(delay%10):
                if double_bullet:
                    bullets=bullet2
                    bullets[bullet2_index].reset((me.rect.centerx-20,me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx+20,me.rect.centery))
                    bullet2_index=(bullet2_index+2)%BULLET2_NUM
                else:
                    bullets=bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index=(bullet1_index+1)%BULLET_NUM

            #检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit=pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active=False
                        for e in enemy_hit:
                            if e in M_enemies or e in X_enemies:
                                e.HP-=1
                                e.hit=True
                                if e.HP==0:
                                    e.active=False
                            else:
                                e.active=False

            #绘制大型敌机
            for each in X_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                    each.fly_image_rect.center=each.rect.center
                    screen.blit(each.fly_images[4],each.fly_image_rect)
                    if not(delay%2):
                        screen.blit(each.fly_images[e3_destory_index],each.fly_image_rect)
                        e3_destory_index=(e3_destory_index+1)%4

                    #绘制大型敌机HP
                    pygame.draw.line(screen,black,\
                                    (each.rect.left,each.rect.top-5),\
                                    (each.rect.right,each.rect.top-5),2)
                    #当生命大于百分之20显示绿色，否则显示红色
                    HP_remain=each.HP/enemy.X_enemy.HP
                    if HP_remain>0.2:
                        HP_color=green
                    else:
                        HP_color=red
                    pygame.draw.line(screen,HP_color,\
                                    (each.rect.left,each.rect.top-5),\
                                    (each.rect.left+each.rect.width*HP_remain,\
                                    each.rect.top-5),2)

                    if each.rect.bottom==-50:
                        X_enemy_out.play(-1)
                else:
                    #毁灭
                    if not(delay%3):
                        screen.blit(each.destroy_images[e3_destory_index],each.rect)
                        e3_destory_index=(e3_destory_index+1)%4
                        if e3_destory_index==0:
                            X_enemy_out.stop()
                            X_enemy_down.play()
                            score+=10000
                            each.reset()

            #绘制中型敌机
            for each in M_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit,each.rect)
                        each.hit=False
                    else:
                        screen.blit(each.image,each.rect)
                    #绘制大型敌机HP
                    pygame.draw.line(screen,black,\
                                    (each.rect.left,each.rect.top-5),\
                                    (each.rect.right,each.rect.top-5),2)
                    #当生命大于百分之20显示绿色，否则显示红色
                    HP_remain=each.HP/enemy.M_enemy.HP
                    if HP_remain>0.2:
                        HP_color=green
                    else:
                        HP_color=red
                    pygame.draw.line(screen,HP_color,\
                                    (each.rect.left,each.rect.top-5),\
                                    (each.rect.left+each.rect.width*HP_remain,\
                                    each.rect.top-5),2)

                else:
                    #毁灭
                    if not(delay%3):
                        screen.blit(each.destroy_images[e3_destory_index],each.rect)
                        e2_destory_index=(e2_destory_index+1)%4
                        if e2_destory_index==0:
                            S_enemy_down.play()
                            score+=3000
                            each.reset()

            #绘制小型敌机
            for each in S_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                else:
                    #毁灭
                    if not(delay%6):
                        screen.blit(each.destroy_images[e3_destory_index],each.rect)
                        e1_destory_index=(e1_destory_index+1)%4
                        S_enemy_down.play()
                        if e1_destory_index==0:
                            score+=1000
                            each.reset()

            #j检测我方飞机是否被撞
            if me.invincible:
                me.mask=me.masks[1]
            else:
                me.mask=me.masks[0]
            enemies_down=pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
            if enemies_down:
                if not me.invincible:
                    me.active=False
                for e in  enemies_down:
                    e.active=False

            #绘制我方飞机动画
            if me.active:
                if me.invincible:
                    me.invincible_image_rect.center=me.rect.center
                    screen.blit(me.invincible_image,me.invincible_image_rect)
                if switch_image:
                    screen.blit(me.image1,me.rect)
                else:
                    screen.blit(me.image2,me.rect)
            else:
                #我方毁灭
                if not(delay%3):
                    screen.blit(each.destroy_images[me_destory_index],each.rect)
                    me_destory_index=(me_destory_index+1)%4
                    if me_destory_index==0:
                        me_down.play()
                        if life_num:
                            life_num-=1
                            me.reset()
            screen.blit(cloud1.image_s,cloud1.image_rect)
            screen.blit(cloud2.image_s,cloud2.image_rect)

            #切换图片
            if not(delay%5):
                switch_image=not switch_image
            delay-=1
            if not delay:
                delay=100
                print("战争文本 Score:%d 炸弹数量:%d 剩余数量%d"%(score,bomb_num,life_num))

        pygame.display.flip()

        clock.tick(60)

if __name__=="__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
