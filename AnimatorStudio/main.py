import pygame as pg
import os, sys
from PIL import Image
import cv2, os, shutil

pg.mixer.pre_init(44100, -16, 2, 512)
pg.mixer.init()
pg.init()

screen_size = pg.display.Info()
w = int(screen_size.current_w/1.2)
h = int(screen_size.current_h/1.2)
screen_size = (w, h)
screen = pg.display.set_mode(screen_size)#, pg.NOFRAME)#pg.FULLSCREEN|pg.HWSURFACE|pg.DOUBLEBUF)
pg.display.set_caption('Animator')
#pg.mixer.music.load(os.path.join('Backgrounds/musics', 'bg.mp3'))
#Loading animation files and paths
PATH = "C:/Users/79224/Desktop/docs/Projects/AnimaWar2/android/assets/persons/Sasuke"
PATH2 = "C:/Users/79224/Desktop/docs/Projects/AnimaWar2/android/assets/persons/Naruto"
PATH3 = "C:/Users/79224/Desktop/docs/Projects/AnimaWar2/android/assets/persons/HarryPotter"

def loadAnim(path,dellist):
    Names = os.listdir(path)
    Names.sort()
    for i in dellist:
        try:
            Names.remove(i)
        except:
            pass
    ImgRes = {i:[] for i in Names}
    for i in Names:
        NamesI = os.listdir(os.path.join(path,i))
        NamesI.sort()
        for j in NamesI:
            ImgRes[i].append(pg.image.load(os.path.join(path,i,j)));
    return ImgRes,Names,path.split('/')[-1]

def getFrame(video):
    vidcap = cv2.VideoCapture(video)
    outpath = video.split('.')[0]
    count = 0
    if os.path.isdir(outpath):
        shutil.rmtree(outpath)
    os.mkdir(outpath)
    while vidcap.isOpened():
        success, image = vidcap.read()
        if success:
            cv2.imwrite(os.path.join(outpath, '%d.png') % count, image)
            count += 1
        else:
            break
    cv2.destroyAllWindows()
    vidcap.release()

def Image_Crop(path, size=0, width=0, alpha=0):
    for file in os.listdir(path):
        name, action, num = file.split('_')
        num = int(num.split('.')[0])
        im = Image.open(os.path.join(path,file)).convert('RGBA')
        w,h = im.size
        if alpha:
            bg = im.getpixel((2,2))
            imdata_old = im.getdata()
            imdata_new = []
            for item in imdata_old:
                if item == bg:
                    imdata_new.append((255,255,255,0))
                else:
                    imdata_new.append(item)
            im.putdata(imdata_new)
        if width:
            im = im.crop((0, 0, width, h))
            w,h = im.size
        if size:
            im = im.resize((int(size*(w/h)),int(size)), Image.ANTIALIAS)
        if not os.path.isdir(os.path.join(path,name,action)):
            if not os.path.isdir(os.path.join(path, name)):
                os.mkdir(os.path.join(path, name))
            os.mkdir(os.path.join(path,name,action))
        im.save(os.path.join(path,name,action,str(num-1)+'.png'),'PNG',quality=100)

def ImageResize(path,width,height):
    for file in os.listdir(path):
        if '.png' in file:
            im = Image.open(os.path.join(path,file)).convert("RGBA").resize((width,height), Image.ANTIALIAS).save(os.path.join(path,file),"PNG",quality=100)

#ImageResize("assets/a",45,45)
#getFrame('vid.mp4')
#Image_Crop(sys.argv[1],size=250)

isRUN = True

Img,Id,Name = loadAnim(PATH,["iData","Prev.png"])
Img2,Id2,Name2 = loadAnim(PATH2,["iData","Prev.png"])
Img3,Id3,Name3 = loadAnim(PATH3,["iData","Prev.png"])
Bot = 'bot'

#Colors
white = (200, 200, 200)
RectColorNormal = (15,15,15)
RectColorFocused = (30,30,30)
RectColorSelected = (12,60,255)
TextColorNormal = (255,255,255)
GridColor = [225,225,255]
MiniPanelColor = [150,150,220]

#Menu ids
MENUID = 0
MENUIDC = 0

#FONTS
minifont = pg.font.Font("assets/6.ttf",11)
font = pg.font.Font("assets/5.ttf",30)
medfont = pg.font.Font("assets/0.otf",18)
bigfont = pg.font.Font("assets/1.ttf",100)

#Sizes
nPad = 10
nRect = (w/4+nPad*2,h/(len(Id)+4))
cof = 7
gcof = 7

#Coords
ImgPos = {
    Name: [w/6,h/5],
    Bot: [w/4,h/4],
    Name2: [w/2,h/5],
    Name3: [w/2,h/3]
}
MP = (0,0)
x,y = 0,0

#FPS
FPS = 30
clock = pg.time.Clock()

#Anim
START_ANIM = False
MAX_ANIM = len(Img[Id[MENUIDC]])
CUR_ANIM = 0
SPEED_ANIM = 1

#...
ScaleRects = [[],[],[]]
kk=0
mClick = -1
sClick = -1
MouseClicked = False
onLoupe = True
Scale = {
    Name:250,
    Name2:250,
    Name3:250,
    Bot:100
}

#About
WaterMark = minifont.render("Python Programm by @happyend",1,TextColorNormal)

PlayerIcons = {'play': pg.image.load("assets/player_play.png"),
               'pause': pg.image.load("assets/player_pause.png"),
                'add': pg.image.load("assets/notification_add.png"),
                'remove': pg.image.load("assets/notification_remove.png"),
                'left': pg.image.load("assets/direction_left.png"),
                'right': pg.image.load("assets/direction_right.png"),
               'up': pg.image.load("assets/direction_up.png"),
               'down': pg.image.load("assets/direction_down.png")}

def addSprite(image,name):
    imgrect = image.get_rect()
    imgrect[0:2] = ImgPos[name]
    SpriteList.append([image,imgrect[0:2],name])

def SizeVectors(image,pos):
    WIDTHPIC = font.render(str(image.get_rect().width) + " px", 1, RectColorNormal)
    HEIGHTPIC = font.render(str(image.get_rect().height) + " px", 1, RectColorNormal)
    ImgRect = image.get_rect()
    ImgRect[0:2] = pos
    pg.draw.line(screen, RectColorNormal, [ImgRect[0] + 1, ImgRect[1] + ImgRect[3] + nPad * 2],
                 [ImgRect[0] + ImgRect[2] - 1, ImgRect[1] + ImgRect[3] + nPad * 2], 2)
    pg.draw.lines(screen, RectColorNormal, 0, [[ImgRect[0] + nPad, ImgRect[1] + ImgRect[3] + nPad * 1.5],
                                               [ImgRect[0], ImgRect[1] + ImgRect[3] + nPad * 2],
                                               [ImgRect[0] + nPad, ImgRect[1] + ImgRect[3] + nPad * 2.5]], 2)
    pg.draw.lines(screen, RectColorNormal, 0, [[ImgRect[0] + ImgRect[2] - nPad, ImgRect[1] + ImgRect[3] + nPad * 1.5],
                                               [ImgRect[0] + ImgRect[2], ImgRect[1] + ImgRect[3] + nPad * 2],
                                               [ImgRect[0] + ImgRect[2] - nPad, ImgRect[1] + ImgRect[3] + nPad * 2.5]],
                  2)
    screen.blit(WIDTHPIC,
                (ImgRect[0] + ImgRect[2] / 2 - WIDTHPIC.get_rect().width / 2, ImgRect[1] + ImgRect[3] + nPad * 4))
    pg.draw.line(screen, RectColorNormal, [ImgRect.left - nPad * 2, ImgRect.top + 1],
                 [ImgRect.left - nPad * 2, ImgRect.bottom - 1], 2)
    pg.draw.lines(screen, RectColorNormal, 0,
                  [[ImgRect.left - nPad * 2.5, ImgRect.top + nPad], [ImgRect.left - nPad * 2, ImgRect.top],
                   [ImgRect.left - nPad * 1.5, ImgRect.top + nPad]], 2)
    pg.draw.lines(screen, RectColorNormal, 0,
                  [[ImgRect.left - nPad * 2.5, ImgRect.bottom - nPad], [ImgRect.left - nPad * 2, ImgRect.bottom],
                   [ImgRect.left - nPad * 1.5, ImgRect.bottom - nPad]], 2)
    screen.blit(pg.transform.rotate(HEIGHTPIC, 90), (ImgRect.left - nPad * 3 - HEIGHTPIC.get_height(),
                                                     ImgRect.top + ImgRect.height / 2 - HEIGHTPIC.get_width() / 2))
    ScaleRects[kk] = pg.draw.rect(screen,RectColorNormal,(ImgRect.left-nPad*2,ImgRect.bottom+nPad,nPad,nPad),2)

def Loupe(image,pos):
    ImgRect = image.get_rect()
    ImgRect[0:2] = pos
    if ImgRect.collidepoint(MP) and onLoupe:
        pg.draw.rect(screen, RectColorFocused, [ImgRect.right + nPad * 3, ImgRect.bottom, nPad * 4 * cof, nPad * 2])
        screen.blit(minifont.render("X: " + str(MP[0] - ImgRect.left) + " Y: " + str(MP[1] - ImgRect.top) + " ЦВЕТ: " + str(
                    image.get_at((MP[0] - ImgRect.left, MP[1] - ImgRect.top))), 1, TextColorNormal),
                    (ImgRect.right + nPad * 5, ImgRect.bottom + nPad / 2))
        for i in range(MP[0] - ImgRect.left - nPad * 2, MP[0] - ImgRect.left + nPad * 2):
            for j in range(MP[1] - ImgRect.top - nPad * 2, MP[1] - ImgRect.top + nPad * 2):
                try:
                    color = image.get_at((i, j))
                except:
                    color = (0, 0, 0, 0)
                if color != (0, 0, 0, 0):
                    x1 = MP[0] - ImgRect.left + nPad * 2 - i
                    y1 = MP[1] - ImgRect.top + nPad * 2 - j
                    x2 = nPad * 4 * cof + nPad * 3 + ImgRect.right - x1 * cof
                    y2 = ImgRect.bottom - y1 * cof
                    pg.draw.rect(screen, color, (x2, y2, cof, cof))
        pg.draw.rect(screen, RectColorFocused,
                 (ImgRect.right + nPad * 3 + nPad * 4 * cof / 2, ImgRect.bottom - nPad * 4 * cof / 2, cof, cof), 2)
        pg.draw.rect(screen, RectColorNormal, (
                    ImgRect.right + nPad * 3, ImgRect.bottom - nPad * 4 * cof, nPad * 4 * cof, nPad * 4 * cof + nPad * 2), 4)

def Moving(image,pos,opos):
    ImgRect = image.get_rect()
    ImgRect[0:2] = pos
    Position = [MP[0]-x,MP[1]-y]
    pg.draw.rect(screen,RectColorNormal,ImgRect,1)
    ImgPos[opos] = Position

def Resize(image,size):
    if size!=image.get_width():
        return pg.transform.scale(image,(int(image.get_width()/image.get_height()*size),size))
    return image

while isRUN:
    #Фон
    screen.fill(white)

    #Сетка
    for i in range(int(h/cof)):
        pg.draw.line(screen,GridColor,[0,i*gcof],[w,i*gcof])
    for j in range(int(w/cof)):
        pg.draw.line(screen,GridColor,[j*gcof,0],[j*gcof,h])

    #Списки
    RectList = []
    SpriteList = []

    #Панель управления
    MenuRects = []
    pg.draw.rect(screen, RectColorNormal, (0,h/1.25,w,nPad*3))
    pg.draw.rect(screen, RectColorFocused, (0,h/1.2,w,h/5))
    Cur = medfont.render("Персонаж: ".upper()+PATH.split('/')[-1].upper(), 1, TextColorNormal)
    CurAnim = medfont.render("КАДР: "+str(CUR_ANIM+1)+" из "+str(MAX_ANIM), 1, TextColorNormal)
    screen.blit(Cur,(nPad,h-nPad*5-CurAnim.get_rect().height*2))
    screen.blit(CurAnim,(nPad,h-nPad*5-CurAnim.get_rect().height/2))
    MenuRects.append(pg.Rect(w/2-nPad*24,h/1.2+nPad,nPad*8,nPad*8))
    screen.blit(PlayerIcons['down'],MenuRects[-1])
    MenuRects.append(pg.Rect(w/2-nPad*14,h/1.2+nPad,nPad*8,nPad*8))
    screen.blit(PlayerIcons['left'],MenuRects[-1])
    MenuRects.append(pg.Rect(w/2-nPad*4,h/1.2+nPad,nPad*8,nPad*8))
    screen.blit(PlayerIcons['pause' if START_ANIM else 'play'],MenuRects[-1])
    MenuRects.append(pg.Rect(w/2+nPad*6,h/1.2+nPad,nPad*8,nPad*8))
    screen.blit(PlayerIcons['right'],MenuRects[-1])
    MenuRects.append(pg.Rect(w/2+nPad*16,h/1.2+nPad,nPad*8,nPad*8))
    screen.blit(PlayerIcons['up'],MenuRects[-1])
    MenuRects.append(pg.Rect(w-nPad*26,h/1.2+nPad*3,nPad*5,nPad*5))
    screen.blit(PlayerIcons['remove'],MenuRects[-1])
    MenuRects.append(pg.Rect(w-nPad*8,h/1.2+nPad*3,nPad*5,nPad*5))
    screen.blit(PlayerIcons['add'],MenuRects[-1])
    FPSTEXT = bigfont.render(str(FPS),1,TextColorNormal)
    screen.blit(minifont.render("КАДРОВ В СЕКУНДУ",1,TextColorNormal),(w-nPad*15-FPSTEXT.get_rect().width//2,h-nPad*1.5))
    screen.blit(FPSTEXT,(w-nPad*15-FPSTEXT.get_rect().width//2,h-nPad*5-FPSTEXT.get_rect().height//2))

    #Список анимаций
    screen.blit(font.render("Анимации:",1,RectColorFocused),(w-w/4-nPad,nPad))
    for i in range(len(Id)):
        RectList.append(pg.Rect(w-w/4,nPad*4+(nPad+nRect[1])*i,nRect[0],nRect[1]))

    #Кадр
    #CurImg = Img[Id[MENUIDC]][CUR_ANIM]
    addSprite(Img[Id[MENUIDC]][CUR_ANIM], Name)
    addSprite(Img2[Id2[MENUIDC]][CUR_ANIM],Name2)
    addSprite(Img3[Id3[MENUIDC]][CUR_ANIM],Name3)
    #addSprite(PlayerIcons['pause'],Bot)
    for i in SpriteList:
        i[0] = Resize(i[0],Scale[i[2]])
        screen.blit(i[0],i[1])

    if MAX_ANIM == 1 or  not START_ANIM:
        SPEED_ANIM = 0
    elif CUR_ANIM==MAX_ANIM-1:
        SPEED_ANIM = -1
    elif CUR_ANIM == 0:
        SPEED_ANIM = 1
    CUR_ANIM += SPEED_ANIM
    for e in pg.event.get():
        if e.type == pg.QUIT:
            isRUN = False
        if e.type == pg.MOUSEMOTION:
            MP = pg.mouse.get_pos()
            MousePos = pg.Rect(MP[0], MP[1], 1, 1).collidelist(RectList)
            if MousePos >= 0:
                MENUID = MousePos
        if e.type == pg.MOUSEBUTTONDOWN:
            MouseClicked = True
            MP = pg.mouse.get_pos()
            kk = len(SpriteList)-1
            for i,j,k in SpriteList[::-1]:
                if ScaleRects[kk].collidepoint(MP):
                    sClick = kk
                    x = MP[0]
                    y = MP[1]
                    break
                elif pg.Rect(j[0],j[1],i.get_width(),i.get_height()).collidepoint(MP):
                    mClick = kk
                    x = MP[0]-pg.Rect(j[0],j[1],i.get_width(),i.get_height()).left
                    y = MP[1]-pg.Rect(j[0],j[1],i.get_width(),i.get_height()).top
                    break
                kk-=1
            if (pg.Rect(MP[0], MP[1], 1, 1).collidelist(RectList) >= 0) and e.button == 1:
                MENUIDC = MENUID
                CUR_ANIM = 0
                SPEED_ANIM = 0
                MAX_ANIM = len(Img[Id[MENUIDC]])
            elif (pg.Rect(MP,(1,1)).collidelist(MenuRects) >= 0) and e.button == 1:
                _ID = pg.Rect(MP,(1,1)).collidelist(MenuRects)
                if _ID==0:
                    CUR_ANIM = 0
                    START_ANIM = False
                elif _ID==1:
                    if CUR_ANIM==0:
                        CUR_ANIM = MAX_ANIM
                    CUR_ANIM-=1 if CUR_ANIM>=1 else 0
                    START_ANIM = False
                elif _ID==2:
                    if START_ANIM:
                        START_ANIM = False
                    else:
                        START_ANIM = True
                        if CUR_ANIM<MAX_ANIM-1:
                            SPEED_ANIM=1
                        else:
                            SPEED_ANIM=-1
                elif _ID==3:
                    if CUR_ANIM==MAX_ANIM-1:
                        CUR_ANIM = -1
                    CUR_ANIM+=1 if CUR_ANIM<MAX_ANIM-1 else 0
                    START_ANIM = False
                elif _ID==4:
                    CUR_ANIM = MAX_ANIM - 1
                    START_ANIM = False
                elif _ID==5:
                    if FPS>0:
                        FPS-=1
                elif _ID==6:
                    if FPS<99:
                        FPS+=1
        elif e.type == pg.MOUSEBUTTONUP:
            MouseClicked = False
            mClick = -1
            sClick = -1
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                isRUN = False
            elif e.key == 270:
                if FPS < 99:
                    FPS += 1
            elif e.key == 269:
                if FPS > 0:
                    FPS -= 1
    RectList[MENUID][0]-=nPad
    kk=0
    for Sprite in SpriteList:
        Loupe(Sprite[0], Sprite[1][0:2])
        if mClick==kk:
            Moving(Sprite[0],Sprite[1][0:2],Sprite[2])
        SizeVectors(Sprite[0],Sprite[1][0:2])
        if sClick==kk:
            Scale[Sprite[2]]+= MP[0]-x
            x = MP[0]
            y = MP[1]
        kk+=1
    #Список анимаций
    for i in range(len(Id)):
        pg.draw.rect(screen,RectColorNormal if MENUIDC!=i else RectColorSelected,RectList[i])
        text = font.render(Id[i].upper(),1,TextColorNormal)
        screen.blit(text,(RectList[i][0]+nPad*2,RectList[i][1]+nPad*2))
    screen.blit(medfont.render("ЧАСТОТА КАДРОВ: "+str(clock)[11:15],1,TextColorNormal),(nPad,h-nPad*3))
    EXIT = pg.draw.rect(screen,RectColorNormal,[0,nPad*2,nPad*10,nPad*3])
    screen.blit(medfont.render("Выход",1,TextColorNormal),(nPad,nPad*2.4))
    if MP[0]<w-w/3:
        MENUID = MENUIDC
    screen.blit(minifont.render(("Путь: "+PATH#+"     "+
                                 #"Имя анимации: "+str(Id[MENUIDC])+"       "+
                                 #"Имя изображения: "+str(CUR_ANIM)+".png"+"       "
                                 #"Размеры: " + str(CurImg.get_width()) + "x" + str(CurImg.get_height())
                                     ), 1, TextColorNormal), (nPad, h / 1.24))
    screen.blit(WaterMark,(w-nPad-WaterMark.get_width(),h/1.24))
    if EXIT.collidepoint(MP) and MouseClicked:
        isRUN = False
    clock.tick(FPS)
    pg.display.update()