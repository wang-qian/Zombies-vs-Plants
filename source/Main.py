# -*- coding: utf-8 -*-
### Version : "v0.0.5 Beta"
### Python Version : 2.7
### Pygame Version : 1.9.1
### SGC Vresion : 0.2.1
### Author : Qian.wang
### Email : wangqian.net@foxmail.com
### License : GNU

import time,datetime
import pygame,sys,random,ImageControl
from pygame.locals import *
import sgc
from sgc.locals import *



background_image_filename = ['images/interface/Surface.png','images/interface/background1.jpg']
welcome_image_filename= 'images/interface/SelectorScreen_WoodSign1_8.png'
startGame_image_filename = {'image':'images/interface/SelectorScreenStartAdventur01.png','down':'images/interface/SelectorScreenStartAdventur02.png'}
smallGame_image_filename = {'image':'images/interface/SelectorScreenSurvival01.png','down':'images/interface/SelectorScreenSurvival02.png'}
puzzleGame_image_filename = {'image':'images/interface/SelectorScreenChallenges01.png','down':'images/interface/SelectorScreenChallenges02.png'}


music_filenames=["other/Faster.ogg","other/losemusic.ogg","other/evillaugh.ogg","other/grasswalk.mp3"]
clock = pygame.time.Clock()

#颜色        R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

startGameX,startGameY = 466,80
smallGameX,smallGameY = 466,200
puzzleGameX,puzzleGameY = 470,300
WINDOWWIDTH = 860
WINDOWHEIGHT = 600

class BtnDialog(sgc.Button):
    def on_click(self):
        global dialogExist
        dialogExist = True
        images={"image":"images/interface/dialog.png","close_off":"images/interface/colse.png"}
        dialogs.append(sgc.Dialog(images,widget=dialog_container))
        dialogs[-1].rect.center = screen.rect.center
        dialogs[-1].add()


#初始化游戏
pygame.init()
pygame.mixer.music.load(music_filenames[0])
screen = sgc.surface.Screen((WINDOWWIDTH, WINDOWHEIGHT), pygame.DOUBLEBUF|0, 32)
pygame.display.set_caption((u"植物大战僵尸学习版").encode('utf-8'))
pygame.display.set_icon(pygame.image.load("images/interface/icon.png"))
background = pygame.image.load(background_image_filename[0]).convert()
yardBackground = pygame.image.load(background_image_filename[1]).convert_alpha()
welcome = pygame.image.load(welcome_image_filename).convert_alpha()
font = pygame.font.Font("other/simsun.ttc",16)
gameOverFont = pygame.font.Font("other/simsun.ttc",60)
text_userName = font.render(u"游客", True, WHITE)
#循环播放背景音乐
pygame.mixer.music.play(-1)
loseSound = pygame.mixer.Sound(music_filenames[1])
evillaughSound = pygame.mixer.Sound(music_filenames[2])

# 以下是自定义对话框中label和button设置
label = sgc.Label(text="unlock!",pos=(160,120),col=WHITE,font=font)
def print_pass():
    dialogs[-1].remove()
btn_ok = sgc.Button("images/interface/LongButton.png",label="ok", pos=(80,210))
btn_ok.on_click = print_pass
dialog_container = sgc.Container(widgets=(label,btn_ok), border=10)
dialogs = []



#开始标志
startflag = False
#添加对话框

startGameButton = sgc.Button(startGame_image_filename,label="", pos=(startGameX,startGameY))
startGameButton.add()
smallGameDialog = BtnDialog(smallGame_image_filename,label="", pos=(smallGameX,smallGameY))
smallGameDialog.modal = True
smallGameDialog.add()
pazzleGameDialog = BtnDialog(puzzleGame_image_filename,label="", pos=(puzzleGameX,puzzleGameY))
pazzleGameDialog.modal = True
pazzleGameDialog.add()

timeClock = clock.tick(30)
oldTime = newTime = datetime.datetime.now()
while True:
    screen.blit(background, (0,0))
    screen.blit(welcome,(0,0))
    screen.blit(text_userName, (140, 100))
    soundPlay = None
    for event in pygame.event.get():
        sgc.event(event)
        if event.type == QUIT:
            exit()
        if event.type == GUI:
            # if event.widget_type is sgc.Button:
            #     print "Button event"
            if event.widget is startGameButton and event.gui_type == "click":
                pygame.mixer.music.stop()
                #开始游戏的声音
                loseSound.play()
                evillaughSound.set_volume(0.2)
                soundPlay=evillaughSound.play()
                startflag = True
                oldTime = datetime.datetime.now()
        #测试坐标
        if event.type == MOUSEBUTTONDOWN:
            #坐标在“开始冒险”图像的范围内
            x, y = pygame.mouse.get_pos()
            #print(x,y)
    if startflag:
        newTime = datetime.datetime.now()
    if (newTime-oldTime).seconds >5:
        break
        
           
    sgc.update(timeClock)
    pygame.display.flip()
    pygame.display.update()

#移动画面显示环境和僵尸
x=0
isRightMove=False
isFirst = True
oldTime = None
zombieImg = pygame.image.load("images/Zombies/Zombie/stand.gif").convert()
#画面移动的速度 像素/秒
backendSpeed = 1
print timeClock
timePassSecond = timeClock/1000.0
distanceMoved = timePassSecond * backendSpeed
myMoved = distanceMoved

#展示环境和出场僵尸
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(yardBackground, (x,0))
    yardBackground.blit(zombieImg, (1100, 100))
    
    x -=myMoved
    if x<-500:
        myMoved=0
        if isFirst:
            isFirst = False
            oldTime = datetime.datetime.now()
        newTime = datetime.datetime.now()
        if (newTime - oldTime).seconds > 2:
            isRightMove = True
    if isRightMove:
        myMoved=-distanceMoved
    if x>-200 and isRightMove:
        break
    pygame.display.flip()


#游戏主体部分
sunBox = pygame.image.load("images/interface/SunBank.png").convert()
oneBox = pygame.image.load("images/interface/Peashooter.gif").convert()
sunFlowerImage = pygame.image.load("images/interface/Sun.gif").convert()
graspedPeaImage = pygame.image.load("images/Plants/Peashooter.gif").convert()
bulletImage = pygame.image.load("images/Plants/PB01.gif").convert()
Peashooter = ImageControl.GIFImage("images/Plants/Peashooter.gif")
moveZombie = ImageControl.GIFImage("images/Zombies/Zombie/moveZobie.gif")
sunFlowers = []
zombies = []
bullets = []
#抓在手里的临时豌豆
graspedPea = None
pedShoters = []

SUN_FLOWER_WIDTH = 76
SUN_FLOWER_HEIGHT = 75
PEA_WIDTH = 63
PEA_HEIGHT = 70
oldTime = datetime.datetime.now()
sunFlowerApperaTime = 5
#标志位
peaFlag = True
#太阳花的个数
sunFlowerCount = 0
#僵尸的个数
zombieCount = 0
#子弹的个数。由于僵尸20秒后才出现，所以赋20的初值
bulletCount = 20
#j僵尸的移动速度
NORMALZOMBIESPEED = 1
#太阳花获得的总数值
sunFlowerNumber = 0
#植物应该出现位置的边界
LEFT_BOUNDARY = 60
TOP_BOUNDARY = 90
#地图上每个格子的大小
GRID_WIDTH=80
GRID_HEIGHT=100
#植物或僵尸可以出现的坐标
allPoints =[]
#标志位判断僵尸是否过了花园
zombiePassGarden =  False
#结束后画面显示的结果
resultText = u'僵尸攻入了你的花园'
for y in xrange(1,6):
    for x in xrange(1,10):
        allPoints.append(((x-1)*GRID_WIDTH+LEFT_BOUNDARY,(y-1)*GRID_HEIGHT+TOP_BOUNDARY))

screen.blit(sunBox, (0,0))
screen.blit(oneBox, (78,0))
screen.blit(font.render(str(sunFlowerNumber), True, BLACK),(35,65))

pygame.mixer.music.load(music_filenames[3])
pygame.mixer.music.play(-1)

while True:
    newTime = datetime.datetime.now()
    # 刚开始种豌豆的时候
    if len(pedShoters) ==1 and peaFlag:
        peaFlag =False
        if (newTime - oldTime).seconds < bulletCount:
            pass
        else:
            bulletCount = (newTime - oldTime).seconds
    #落太阳花
    #地图随机掉落，在一定范围内点击，太阳花消失
    if (newTime - oldTime).seconds > sunFlowerApperaTime * sunFlowerCount  and (newTime - oldTime).seconds % sunFlowerApperaTime==0:
        newSunFlower = {'rect': pygame.Rect(random.randint(80,WINDOWWIDTH-SUN_FLOWER_WIDTH
        -80), random.randint(70,WINDOWHEIGHT-SUN_FLOWER_HEIGHT-70), SUN_FLOWER_WIDTH
    , SUN_FLOWER_HEIGHT),
                        'surface':pygame.transform.scale(sunFlowerImage, (SUN_FLOWER_WIDTH
                        , SUN_FLOWER_HEIGHT)),
                        'showTime':datetime.datetime.now(),
                        }
        sunFlowers.append(newSunFlower)
        sunFlowerCount = sunFlowerCount + 1
    #20秒后僵尸出现,5分钟后不出现新僵尸
    if (newTime - oldTime).seconds >= 20*(zombieCount+1) and (newTime - oldTime).seconds % 20==0 and (newTime - oldTime).seconds < 300 :
        newZombie = {'rect' : pygame.Rect(840, random.randint(1,5)*100-70, 62, 128),
                        'hp' : 4,
                        }
        zombies.append(newZombie)
        zombieCount = zombieCount + 1

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONUP:
            if graspedPea:
                hasPeaShoter = False
                x, y = pygame.mouse.get_pos()
                #得到临时豌豆接近根部的坐标用来判断，以便更好的放置豌豆
                x,y = x,y+60
                for point in allPoints:
                    #豌豆在这个格子的范围内
                    if x in range(point[0],point[0]+GRID_WIDTH) and y in range(point[1],point[1]+GRID_HEIGHT):
                        if pedShoters:
                            for p in pedShoters:
                                #这个格子有其他的豌豆
                                if p['rect'].left == point[0] and p['rect'].top == point[1]:
                                    hasPeaShoter = True
                        if not pedShoters or not hasPeaShoter:
                            graspedPea['rect'].topleft = (point[0], point[1])
                            pedShoters.append(graspedPea)
                            #临时的豌豆消失
                            graspedPea = None
                            hasPeaShoter = False
                            #太阳花数减少
                            sunFlowerNumber -=100
        if event.type == MOUSEMOTION:
            if graspedPea:
                x, y = pygame.mouse.get_pos()
                graspedPea['rect'].topleft = (x, y)
        if event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x in range(70,120) and y in range(0,70):
                if sunFlowerNumber>=100:
                    #生成临时豌豆
                    print "pea get"
                    graspedPea={'rect': pygame.Rect(x, y, PEA_WIDTH, PEA_HEIGHT
                    ),
                        'surface':pygame.transform.scale(graspedPeaImage, (PEA_WIDTH, PEA_HEIGHT
                        )),
                        'hp':1,
                        }
            print(x,y)
            #点击的坐票在太阳花的坐标内，太阳花消失
            for s in sunFlowers:
                #print s['rect'].left
                if x in range(s['rect'].left,s['rect'].left+s['rect'].width) and y in range(s['rect'].top,s['rect'].top+s['rect'].height):
                    #太阳花消失，显示的数目加50
                    sunFlowers.remove(s)
                    sunFlowerNumber += 50


    #和植物同一条直线上有僵尸，就发射子弹
    #僵尸的坐标比植物的坐标低70，因此计算的时候加上
    if  (newTime - oldTime).seconds > 1 * bulletCount :
        for p in pedShoters:
            bulletCount +=1
                
            for z in zombies:
                if z['rect'].top+60 == p['rect'].top:
                    newBullet = {'rect': pygame.Rect(p['rect'].left+p['rect'].width,p['rect'].top , 24, 24),
                            'surface':pygame.transform.scale(bulletImage, (24, 24)),
                            }
                    bullets.append(newBullet)
                    bulletCount += 1
                    break    
                    
    if (newTime-oldTime).microseconds %10000 ==0:
        for z in zombies:
            z['rect'].move_ip(-1*NORMALZOMBIESPEED, 0)
    for b in bullets:
        b['rect'].move_ip(NORMALZOMBIESPEED*2, 0)

    #画图
    screen.blit(yardBackground, (-200,0))
    screen.blit(sunBox, (0,0))
    screen.blit(oneBox, (78,0))
    screen.blit(font.render(str(sunFlowerNumber), True, BLACK),(30,65))
    if graspedPea:
        screen.blit(graspedPeaImage, graspedPea['rect'])
    for s in sunFlowers:
            #20秒以后花消失
            if (datetime.datetime.now()-s['showTime']).seconds > 20:
                sunFlowers.remove(s)
            else:
                screen.blit(s['surface'], s['rect'])
    for p in pedShoters:
            #豌豆和僵尸的碰撞侦测
            for z in zombies:
                if p['rect'].collidepoint(z['rect'].left+40,z['rect'].top+z['rect'].width):
                    p['hp'] -=1
            if p['hp'] <=0:
                pedShoters.remove(p)
            else:
                Peashooter.render(screen,p['rect'].topleft)
    for z in zombies:
            #碰撞侦测
            for b in bullets:
                if z['rect'].collidepoint(b['rect'].left - 40,b['rect'].top):
                    bullets.remove(b)
                    z['hp'] -= 1
            #僵尸越过了花园
            if z['rect'].left+z['rect'].width < 0:
                zombiePassGarden = True
            if z['hp']<=0:
                zombies.remove(z)
            else:
                moveZombie.render(screen,z['rect'].topleft)
    for b in bullets:
        screen.blit(b['surface'], b['rect'])

    if zombiePassGarden:
        break
    if len(zombies) == 0 and (newTime-oldTime).seconds > 300:
        resultText = u'你赢了'
        break
    
    # update the display
    pygame.display.update()
    pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(yardBackground, (-200,0))
    screen.blit(gameOverFont.render(resultText, True, BLACK),(100,300))
    pygame.display.flip()
    pygame.display.update()

    
