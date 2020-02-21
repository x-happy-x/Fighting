import csv, os
from random import randint as rd
from time import sleep

import pygame as pg

from Backgrounds.object.Background import Background as BG
from Fighter import *

pg.mixer.pre_init(44100, -16, 2, 512)
pg.mixer.init()
pg.init()
white = (200, 200, 200)
StandardSR = 1.779
screen_size = pg.display.Info()
w = int(screen_size.current_w)
h = int(screen_size.current_h)
# w,h = 1000,700
screen_size = (w, h)
screen = pg.display.set_mode((screen_size), pg.FULLSCREEN)
pg.display.set_caption('Fighting')
pg.mixer.music.load(os.path.join('Backgrounds/musics', 'bg.mp3'))
screen_ratio = round(w / h, 3)
if screen_ratio > StandardSR:
    w = int(h * StandardSR)
elif screen_ratio < StandardSR:
    h = int(w / StandardSR)
StandardFS = int(h / 10)
FS = [StandardFS * 2, StandardFS, int(StandardFS - StandardFS / 6), int(StandardFS - StandardFS / 3),
      int(StandardFS / 1.8), int(StandardFS / 2.2), int(StandardFS / 3)]
RESOURCES = {'Sounds': {'Fight': pg.mixer.Sound('Sounds/Fight.ogg'),
                        'Select': pg.mixer.Sound('Sounds/Select.wav'),
                        'Round1': pg.mixer.Sound('Sounds/RoundOne.ogg'),
                        'Round2': pg.mixer.Sound('Sounds/RoundTwo.ogg'),
                        'Round3': pg.mixer.Sound('Sounds/RoundThree.ogg')},
             'Fonts': {
                 'F0 Large2': pg.font.Font('Fonts/0.ttf', FS[1]),
                 'F1 Large2': pg.font.Font('Fonts/1.otf', FS[1]),
                 'F1 Large3': pg.font.Font('Fonts/1.otf', FS[0]),
                 'F2 Large2': pg.font.Font('Fonts/2.ttf', FS[1]),
                 'F0 Medium2': pg.font.Font('Fonts/0.ttf', FS[3]),
                 'F1 Medium2': pg.font.Font('Fonts/1.otf', FS[3]),
                 'F2 Medium2': pg.font.Font('Fonts/2.ttf', FS[3]),
                 'F0 Small2': pg.font.Font('Fonts/0.ttf', FS[5]),
                 'F1 Small2': pg.font.Font('Fonts/1.otf', FS[5]),
                 'F2 Small2': pg.font.Font('Fonts/2.ttf', FS[5]),
                 'F0 Large': pg.font.Font('Fonts/0.ttf', FS[2]),
                 'F1 Large': pg.font.Font('Fonts/1.otf', FS[2]),
                 'F2 Large': pg.font.Font('Fonts/2.ttf', FS[2]),
                 'F0 Medium': pg.font.Font('Fonts/0.ttf', FS[4]),
                 'F1 Medium': pg.font.Font('Fonts/1.otf', FS[4]),
                 'F2 Medium': pg.font.Font('Fonts/2.ttf', FS[4]),
                 'F0 Small': pg.font.Font('Fonts/0.ttf', FS[6]),
                 'F1 Small': pg.font.Font('Fonts/1.otf', FS[6]),
                 'F2 Small': pg.font.Font('Fonts/2.ttf', FS[6])}}
bg = BG('bg2.jpg', (0, 0), screen_size)
CharMatrix    = [[1, 2, 0],
              [0, 0, 0],
              [0, 0, 0],
              [0, 0, 0],
              [0, 0, 0]]
CharactersIds = ['Naruto', 'Sasuke', 'JakeTheDog',
                 'TorVar', 'HarryPotter', 'None',
                 'None', 'None', 'None',
                 'None', 'None', 'None',
                 'None', 'None', 'None']
CharDoneIds = CharactersIds.copy()
while 'None' in CharDoneIds:
    CharDoneIds.remove('None')
CharactersNames = ['Игрок 1', 'Игрок 2', 'Jake',
                   'TorVar', 'Гарри', 'Нету',
                   'Нету', 'Нету', 'Нету',
                   'Нету', 'Нету', 'Нету',
                   'Нету', 'Нету', 'Нету']
START_SCR, FIGHTING_SCR, CHARSEL_SCR, SETTING_SCR, GAMEOVER_SCR, EXIT_SCR = range(
    2, 8)
SCREENS = [START_SCR, 0, 0, 0]
DEFAULT_PLAYERS = [[0, 0], [1, 1]]
clock = pg.time.Clock()
def GSReader():
    GS = csv.DictReader(open("GameSettings.data"), delimiter=',')
    Data = {}
    for GSi in GS:
        for Params in GSi:
            try:
                Data[Params] = int(GSi[Params])
            except ValueError:
                Data[Params] = GSi[Params]
        break
    return Data
GSs = GSReader()
def GSWriter(DataPack):
    GS = list(csv.reader(open("GameSettings.data")))
    GS[1] = DataPack
    CSVwriter = csv.writer(open("GameSettings.data", 'w', newline=''))
    for GSi in GS:
        CSVwriter.writerow(GSi)
def DataReader(DFP):
    if len(DFP)==2:
        PersonID, ControlID = DFP
    else:
        PersonID, ControlID, cd = DFP
    Data = {}
    if PersonID != -1:
        CharactersData = csv.DictReader(
            open("Characters/CharactersParam.data"), delimiter=',')
        DataID = 0
        Data['WxH'] = (w, h)
        Data['PersonID'] = PersonID
        for CharacterData in CharactersData:
            if DataID == PersonID:
                for Params in CharacterData:
                    try:
                        Data[Params] = int(CharacterData[Params])
                    except ValueError:
                        Data[Params] = CharacterData[Params]
                break
            else:
                DataID += 1
    if ControlID != -1:
        Data['ControlKeys'] = {}
        Data['ControlID'] = ControlID
        if ControlID == 0:
            Data['CoordsX'] = screen_size[0] // 5
        else:
            Data['CoordsX'] = screen_size[0] - screen_size[0] // 5
        Data['CoordsY'] = screen_size[1] - screen_size[1] // 7
        DataID = 0
        ControlsData = csv.DictReader(open('Player1.data'), delimiter=',')
        for ControlData in ControlsData:
            if DataID == ControlID:
                for Params in ControlData:
                    Data['ControlKeys'][Params] = int(ControlData[Params])
                break
            else:
                DataID += 1
    else:
        Data['ControlID'] = cd
        if cd == 0:
            Data['CoordsX'] = screen_size[0] // 5
        else:
            Data['CoordsX'] = screen_size[0] - screen_size[0] // 5
        Data['CoordsY'] = screen_size[1] - screen_size[1] // 7
    return Data
def DataWriter(DFP):
    PersonID, ControlID, DataPack = DFP
    if PersonID != -1:
        CharactersData = list(csv.reader(
            open("Characters/CharactersParam.data")))
        CharactersData[PersonID + 1] = DataPack
        CSVwriter = csv.writer(
            open("Characters/CharactersParam.data", 'w', newline=''))
        for line in CharactersData:
            CSVwriter.writerow(line)
    elif ControlID != -1:
        ControlsData = list(csv.reader(open('Player1.data')))
        ControlsData[ControlID] = DataPack
        CSVwriter = csv.writer(open('Player1.data', 'w', newline=''))
        for line in ControlsData:
            CSVwriter.writerow(line)
def ScreenChanger(_SCREENS_):
    global DEFAULT_PLAYERS, GSs
    _NEXT_ = _SCREENS_[2]
    if _SCREENS_[2] == 0:
        if _SCREENS_[0] == _SCREENS_[1]:
            _NEXT_ = EXIT_SCR
        else:
            _NEXT_ = _SCREENS_[0]
    if _NEXT_ == EXIT_SCR:
        pass
    elif _NEXT_ == CHARSEL_SCR:
        CharacterSelection()
    elif _NEXT_ == START_SCR:
        SS(9, 4)
    elif _NEXT_ == SETTING_SCR:
        Settings()
    elif _NEXT_ == FIGHTING_SCR:
        FightProcess(DEFAULT_PLAYERS[0], DEFAULT_PLAYERS[1],
                     GSs['AllRounds'], GSs['TimeRound'], _SCREENS_[3])
    elif _NEXT_ == GAMEOVER_SCR:
        GameOver(DEFAULT_PLAYERS[0], DEFAULT_PLAYERS[1], _SCREENS_[3])
def OnShow(scr, list):
    showlist3 = []
    if scr == 0:
        for surf in list:
            showlist3.append(surf[1])
        pg.display.update(showlist3)
    else:
        for surf in list:
            scr.blit(surf[0], surf[1])
def Settings():
    global SCREENS, DEFAULT_PLAYERS
    SCREENS[1] = SETTING_SCR

    def SettingItem(_Pad, _Rect, _Title, _Color, _State=-1, _Value=-1):
        SI = pg.Surface((_Rect[2], _Rect[3]), pg.SRCALPHA)
        SL = []
        pg.draw.rect(SI, _Color[0], _Rect)
        ST = RESOURCES['Fonts']['F0 Small'].render(_Title, 1, (255, 255, 255))
        SL.append(
            [ST, (_Rect.left + _Pad, _Rect.centery - ST.get_rect().height // 1.8)])
        if _State != -1:
            if _Value == -1:
                pg.draw.rect(SI, _Color[2 if _State else 1],
                             (_Rect[2] - _Rect[2] // 6, 0, _Rect[2] // 5, _Rect[3]))
                ST = RESOURCES['Fonts']['F0 Small'].render(
                    'ВКЛ.' if _State else 'ВЫКЛ.', 1, (255, 255, 255))
                SL.append([ST, (_Rect[2] - _Rect[2] // 6 + _Pad,
                                _Rect.centery - ST.get_rect().height // 1.8)])
            else:
                ST = RESOURCES['Fonts']['F0 Small'].render(
                    str(_Value), 1, (255, 255, 255))
                pg.draw.rect(SI, _Color[2 if _State else 1],
                             (_Rect[2] - (ST.get_rect().width + _Pad * 2), 0, ST.get_rect().width + _Pad * 3, _Rect[3]))
                SL.append([ST, (_Rect[2] - ST.get_rect().width - _Pad,
                                _Rect.centery - ST.get_rect().height // 1.8)])
        OnShow(SI, SL)
        return SI

    Graphic, Sound, CharParam, Control = range(1, 5)
    SettingScr = Graphic
    MITs = ['ГРАФИКА', 'АУДИО', 'ПЕРСОНАЖИ', 'УПРАВЛЕНИЕ', 'НАЗАД']
    MIL = [0 for i in range(len(MITs))]
    MIT, MITL = MIL.copy(), MIL.copy()
    MIM = [[1 if i == 0 else 0] for i in range(len(MITs))]
    MC = [[0, 0, 0], [25, 25, 25], [40, 40, 40], [
        241, 51, 19], [56, 151, 240], [255, 255, 255]]
    GOSurf = pg.Surface(
        (screen_size[0] // 3 + w // 15, screen_size[1]), pg.SRCALPHA)
    GOSL = []
    MR_height = h // 13
    MR_pad = (h // 2 - MR_height * 5) // 5
    MenuRectBG = pg.Rect(w // 15, 0, screen_size[0] // 3, screen_size[1])
    MenuRectItem = pg.Rect(MenuRectBG[0] + MR_pad // 2, MenuRectBG[1] + h // 5 + MR_pad * 2, MenuRectBG[2] - MR_pad,
                           MR_height)
    pg.draw.rect(GOSurf, MC[2], MenuRectBG)
    for i in range(len(MITs)):
        MIL[i] = pg.draw.rect(GOSurf, MC[1], MenuRectItem)
        MIT[i] = RESOURCES['Fonts']['F0 Small'].render(MITs[i], 1, MC[-1])
        MITL[i] = pg.Rect(MenuRectItem.centerx - MIT[i].get_rect().width // 2,
                          MenuRectItem.centery -
                          MIT[i].get_rect().height // 2, MIT[i].get_rect().width,
                          MIT[i].get_rect().height)
        GOSL.append([MIT[i], MITL[i]])
        MenuRectItem.y += MR_height + MR_pad
    OnShow(GOSurf, GOSL)
    WTSurf = pg.Surface((screen_size[0], h // 5), pg.SRCALPHA)
    WTSL = []
    pg.draw.rect(WTSurf, MC[-2], WTSurf.get_rect())
    Title = RESOURCES['Fonts']['F1 Large2'].render('Настройки', 1, MC[-1])
    WTSL.append([Title, (
        MenuRectItem.centerx - Title.get_rect().width // 2, WTSurf.get_rect().centery - Title.get_rect().height // 2)])
    OnShow(WTSurf, WTSL)
    SetFrame = pg.Surface((screen_size[0] - MenuRectBG[0] - MenuRectBG[2] - MR_pad * 2, h - MR_pad * 3 - h // 5),
                          pg.SRCALPHA)
    SFSL = []
    pg.draw.rect(SetFrame, MC[2], SetFrame.get_rect())
    SMP = pg.Rect(0, 0, SetFrame.get_rect().width, MR_height)
    screen.blit(
        SetFrame, (MenuRectBG[2] + MenuRectBG[0] + MR_pad, h // 5 + MR_pad * 2))
    screen.blit(GOSurf, (0, 0))
    screen.blit(WTSurf, (0, MR_pad))
    MIL.append(pg.Rect(MenuRectBG[2] + MenuRectBG[0] + MR_pad, h // 5 + MR_pad * 2, SetFrame.get_rect().width,
                       SetFrame.get_rect().height))
    pg.display.update()
    DFP = [DataReader([0, 0]), DataReader([1, 1])]
    DFP[0]['CoordsX'] = w // 15
    DFP[0]['CoordsY'] = SetFrame.get_rect().height - h // 12
    DFP[1]['CoordsX'] = SetFrame.get_rect().width - w // 12
    DFP[1]['CoordsY'] = SetFrame.get_rect().height - h // 12
    Player1 = Fighter(DFP[0])
    Player2 = Fighter(DFP[1])
    Player2.flip()
    while SettingScr:
        MCS = False
        screen.blit(GOSurf, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                GO_Run = False
                SCREENS[2] = EXIT_SCR
            if event.type == pg.MOUSEMOTION:
                MP = pg.mouse.get_pos()
                MousePos = pg.Rect(MP[0], MP[1], 1, 1).collidelist(MIL[:-1])
                if MousePos >= 0:
                    MIM[MIM.index([1])] = [0]
                    MIM[MousePos] = [1]
            if event.type == pg.MOUSEBUTTONUP:
                MP = pg.mouse.get_pos()
                if (pg.Rect(MP[0], MP[1], 1, 1).collidelist(MIL[:-1]) >= 0) and event.button == 1:
                    MCS = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    CS_Helper(1, 'Up', MIM)
                elif event.key == pg.K_DOWN:
                    CS_Helper(1, 'Down', MIM)
                elif event.key == 13:
                    MCS = True
                elif event.key == pg.K_ESCAPE:
                    SettingScr = False
                    SCREENS[2] = 0
        RectID = MIM.index([1])
        if RectID >= 0:
            pg.draw.rect(screen, MC[-2], MIL[RectID])
            screen.blit(MIT[RectID], MITL[RectID])
            if MCS:
                if RectID == 0:
                    SettingScr = Graphic
                elif RectID == 1:
                    SettingScr = Sound
                elif RectID == 2:
                    SettingScr = CharParam
                elif RectID == 3:
                    SettingScr = Control
                elif RectID == 4:
                    SettingScr = False
                    SCREENS[2] = 0
        if SettingScr == Control:
            pg.draw.rect(SetFrame, MC[2], SetFrame.get_rect())
            pg.draw.rect(SetFrame, MC[-2], SMP)
            Title = RESOURCES['Fonts']['F1 Small'].render(
                'УПРАВЛЕНИЕ', 1, MC[-1])
            SetFrame.blit(Title,
                          (SMP.centerx - Title.get_rect().width // 2, SMP.centery - Title.get_rect().height // 2))
            SetFrame.blit(
                SettingItem(MR_pad, SMP, 'ВОССТАНОВИТЬ НАСТРОЙКИ ПО УМОЛЧАНИЮ'.upper(
                ), (MC[1], MC[0], MC[-2])),
                (0, MR_height + MR_pad))
            SetFrame.blit(
                SettingItem(MR_pad, SMP, 'КАКОМУ ИГРОКУ СМЕНИТЬ УПРАВЛЕНИЕ?'.upper(), (MC[1], MC[0], MC[-2]), False,
                            str(clock)[11:-2]), (0, MR_height * 3 + MR_pad))
            SMP1 = pg.draw.rect(
                SetFrame, MC[-2], (0, MIL[-1][3] - MR_height, SMP[2] // 2, MR_height))
            Player1.draw(SetFrame, Player2)
            Player2.draw(SetFrame, Player1)
            Title = RESOURCES['Fonts']['F1 Small'].render('Игрок 1', 1, MC[-1])
            SetFrame.blit(Title,
                          (SMP1.centerx - Title.get_rect().width // 2, SMP1.centery - Title.get_rect().height // 2))
            SMP2 = pg.draw.rect(
                SetFrame, MC[-3], (SMP[2] // 2, MIL[-1][3] - MR_height, SMP[2] // 2, MR_height))
            Title = RESOURCES['Fonts']['F1 Small'].render('Игрок 2', 1, MC[-1])
            SetFrame.blit(Title,
                          (SMP2.centerx - Title.get_rect().width // 2, SMP2.centery - Title.get_rect().height // 2))
            screen.blit(
                SetFrame, (MenuRectBG[2] + MenuRectBG[0] + MR_pad, h // 5 + MR_pad * 2))
        elif SettingScr == Graphic:
            pg.draw.rect(SetFrame, MC[2], SetFrame.get_rect())
            pg.draw.rect(SetFrame, MC[-2], SMP)
            Title = RESOURCES['Fonts']['F1 Small'].render('ГРАФИКА', 1, MC[-1])
            SetFrame.blit(Title,
                          (SMP.centerx - Title.get_rect().width // 2, SMP.centery - Title.get_rect().height // 2))
            SetFrame.blit(SettingItem(MR_pad, SMP, 'Тени'.upper(), (MC[1], MC[0], MC[-2]), True),
                          (0, MR_height + MR_pad))
            SetFrame.blit(
                SettingItem(MR_pad, SMP, 'Частота кадров'.upper(),
                            (MC[1], MC[0], MC[-2]), True, str(clock)[11:-2]),
                (0, (MR_height + MR_pad) * 2))
            SetFrame.blit(SettingItem(MR_pad, SMP, 'Полноэкранный режим'.upper(), (MC[1], MC[0], MC[-2]), True),
                          (0, (MR_height + MR_pad) * 3))
            SetFrame.blit(SettingItem(MR_pad, SMP, 'Дополнительная анимация'.upper(), (MC[1], MC[0], MC[-2]), False),
                          (0, (MR_height + MR_pad) * 4))
            SetFrame.blit(SettingItem(MR_pad, SMP, 'Размеры шрифта'.upper(), (MC[1], MC[0], MC[-2])),
                          (0, (MR_height + MR_pad) * 5))
            screen.blit(
                SetFrame, (MenuRectBG[2] + MenuRectBG[0] + MR_pad, h // 5 + MR_pad * 2))
        elif SettingScr == Sound:
            pg.draw.rect(SetFrame, MC[2], SetFrame.get_rect())
            pg.draw.rect(SetFrame, MC[-2], SMP)
            Title = RESOURCES['Fonts']['F1 Small'].render('АУДИО', 1, MC[-1])
            SetFrame.blit(Title,
                          (SMP.centerx - Title.get_rect().width // 2, SMP.centery - Title.get_rect().height // 2))
            SetFrame.blit(SettingItem(MR_pad, SMP, 'Звук'.upper(), (MC[1], MC[0], MC[-2]), True),
                          (0, MR_height + MR_pad))
            SetFrame.blit(SettingItem(MR_pad, SMP, 'Общая громкость'.upper(), (MC[1], MC[0], MC[-2]), True, '     100'),
                          (0, (MR_height + MR_pad) * 2))
            SetFrame.blit(
                SettingItem(MR_pad, SMP, 'Громкость спецэффектов'.upper(
                ), (MC[1], MC[0], MC[-2]), True, '  50'),
                (0, (MR_height + MR_pad) * 3))
            SetFrame.blit(
                SettingItem(MR_pad, SMP, 'Громкость фоновой музыки'.upper(
                ), (MC[1], MC[0], MC[-2]), True, '    75'),
                (0, (MR_height + MR_pad) * 4))
            SetFrame.blit(SettingItem(MR_pad, SMP, 'Выбрать фоновую музыку'.upper(), (MC[1], MC[0], MC[-2])),
                          (0, (MR_height + MR_pad) * 5))
            screen.blit(
                SetFrame, (MenuRectBG[2] + MenuRectBG[0] + MR_pad, h // 5 + MR_pad * 2))
        elif SettingScr == CharParam:
            pg.draw.rect(SetFrame, MC[2], SetFrame.get_rect())
            pg.draw.rect(SetFrame, MC[-2], SMP)
            Title = RESOURCES['Fonts']['F1 Small'].render(
                'ПЕРСОНАЖИ', 1, MC[-1])
            SetFrame.blit(Title,
                          (SMP.centerx - Title.get_rect().width // 2, SMP.centery - Title.get_rect().height // 2))
            SetFrame.blit(SettingItem(MR_pad, SMP, 'СКОРО...'.upper(
            ), (MC[1], MC[0], MC[-2])), (0, MR_height + MR_pad))
            screen.blit(
                SetFrame, (MenuRectBG[2] + MenuRectBG[0] + MR_pad, h // 5 + MR_pad * 2))
        pg.display.update(MIL)
        clock.tick(GSs['MaxFPS'] * 2)
    ScreenChanger(SCREENS)
def FightProcess(_Player1_, _Player2_, AllRounds=3, RoundTime=99, TYPE=0):
    Layer1, Layer2, Layer3 = [],[],[]
    pg.mixer.music.load('Backgrounds/musics/1.mp3')
    global SCREENS, DEFAULT_PLAYERS
    Running, Paused, Stopped = range(3)
    Music = True
    _TIME_ = 3
    TIME_ENDING = -255
    Ctrl = 0
    Player1 = Fighter(DataReader(_Player1_))
    Player2 = Fighter(DataReader(_Player2_))
    Player2.flip()
    if SCREENS[1] == SETTING_SCR:
        surf = pg.Surface(screen_size, pg.SRCALPHA)
        pg.draw.rect(surf, (0, 0, 0, 200), surf.get_rect())
        screen.blit(bg.image, bg.rect)
        screen.blit(surf, (0, 0))
        pg.display.update()
    SCREENS[1] = FIGHTING_SCR
    MusicPos = 0.0
    FightingRun = Running
    TIME = RoundTime
    RoundWins = [0 for i in range(AllRounds)]
    Round = 1
    PAUSE = [0, 0]
    CWins = [0, 0, 0]
    HSE = True
    start_ticks = pg.time.get_ticks()
    seconds = 0
    timer = 0
    if TYPE != 0:
        MusicPos, Round, PAUSE, RoundWins, TIME, HSE, start_ticks, seconds, CWins, Player1.PROPERTY[
            'BodyRect'], Player2.PROPERTY['BodyRect'], Player1.PROPERTY['Healf'], Player2.PROPERTY['Healf'], timer = SCREENS[3]
        FightingRun = Paused
    GameOverText = RESOURCES['Fonts']['F1 Large2'].render(
        'GAME OVER', 1, (233, 33, 33))
    SoundTimes = [0, 0, 0]
    surf = pg.Surface(screen_size, pg.SRCALPHA)
    MITs = ['ПРОДОЛЖИТЬ', 'НАЧАТЬ ЗАНОВО', 'ВЫБОР ПЕРСОНАЖЕЙ',
            'НАСТРОЙКИ', 'ГЛАВНЫЙ ЭКРАН', 'ЗАВЕРШИТЬ ИГРУ']
    MIL = [0 for i in range(len(MITs))]
    MIT, MITL = MIL.copy(), MIL.copy()
    MIM = [[1 if i == 0 else 0] for i in range(len(MITs))]
    MC = [[0, 0, 0], [25, 25, 25], [40, 40, 40],
          [56, 151, 240], [255, 255, 255]]
    GOSurf = pg.Surface(
        (screen_size[0] // 3 + w // 15, screen_size[1]), pg.SRCALPHA)
    GOSL = []
    MR_height = h // 13
    MR_pad = (h // 2 - MR_height * 5) // 5
    MenuRectBG = pg.Rect(w // 15, 0, screen_size[0] // 3, screen_size[1])
    MenuRectItem = pg.Rect(MenuRectBG[0] + MR_pad // 2, MenuRectBG[1] + h // 5 + MR_pad * 2, MenuRectBG[2] - MR_pad,
                           MR_height)
    pg.draw.rect(GOSurf, MC[2], MenuRectBG)
    for i in range(len(MITs)):
        MIL[i] = pg.draw.rect(GOSurf, MC[1], MenuRectItem)
        MIT[i] = RESOURCES['Fonts']['F0 Small'].render(MITs[i], 1, MC[-1])
        MITL[i] = pg.Rect(MenuRectItem.centerx - MIT[i].get_rect().width // 2,
                          MenuRectItem.centery -
                          MIT[i].get_rect().height // 2, MIT[i].get_rect().width,
                          MIT[i].get_rect().height)
        GOSL.append([MIT[i], MITL[i]])
        MenuRectItem.y += MR_height + MR_pad
    OnShow(GOSurf, GOSL)
    WTSurf = pg.Surface((screen_size[0], h // 5), pg.SRCALPHA)
    WTSL = []
    pg.draw.rect(WTSurf, MC[-2], WTSurf.get_rect())
    Title = RESOURCES['Fonts']['F1 Large2'].render('ПАУЗА', 1, MC[-1])
    WTSL.append([Title, (
        MenuRectItem.centerx - Title.get_rect().width // 2, WTSurf.get_rect().centery - Title.get_rect().height // 2)])
    TitleVS = RESOURCES['Fonts']['F0 Small'].render('vs', 1, MC[-1])
    VSCoords = (WTSurf.get_rect().width - WTSurf.get_rect().width //
                4 - TitleVS.get_rect().width // 2, MR_pad * 1.5)
    WTSL.append([TitleVS, VSCoords])
    TitleP1 = RESOURCES['Fonts']['F1 Medium'].render(
        CharactersNames[_Player1_[0]].upper(), 1, MC[-1])
    WTSL.append(
        [TitleP1, (VSCoords[0] - MR_pad - TitleP1.get_rect().width, MR_pad * 1.5)])
    TitleP2 = RESOURCES['Fonts']['F1 Medium'].render(
        CharactersNames[_Player2_[0]].upper(), 1, MC[-1])
    WTSL.append(
        [TitleP2, (VSCoords[0] + MR_pad + TitleVS.get_rect().width, MR_pad * 1.5)])
    OnShow(WTSurf, WTSL)
    Controler1 = DataReader([-1,0])
    Controler2 = DataReader([-1,1])
    def ShowUI(Player1,Player2, _time):
        xp_l = RESOURCES['Fonts']['F0 Medium'].render(
                'HP: ' + str(Player1.PROPERTY['Healf']), 1, (255, 255, 255))
        xp_r = RESOURCES['Fonts']['F0 Medium'].render(
                'HP: ' + str(Player2.PROPERTY['Healf']), 1, (255, 255, 255))
        FPS = RESOURCES['Fonts']['F0 Small'].render(
                'FPS: ' + str(clock)[11:-2], 1, (255, 255, 255))
        # Drawing shapes
        pg.draw.rect(screen, (248, 100, 50), (20, 20, w/2.5, 30))
        pg.draw.rect(screen, (248, 100, 50),
                         (screen_size[0] - 20 - w//2.5, 20, w/2.5, 30))
        pg.draw.rect(screen, (59, 131, 189),
                         (20, 20, (Player1.PROPERTY['Healf'] // Player1.PROPERTY['HealfPercent']) * (w/2.5/100), 30))
        pg.draw.rect(screen, (59, 131, 189), (
                screen_size[0] - 20 - (Player2.PROPERTY['Healf'] //
                                       Player2.PROPERTY['HealfPercent']) * (w/2.5/100), 20,
                (Player2.PROPERTY['Healf'] // Player2.PROPERTY['HealfPercent']) * (w/2.5/100), 30))
        pg.draw.rect(screen, (78, 84, 82), (20, h-40, 100 * 4, 15))
        pg.draw.rect(screen, (78, 84, 82),
                         (screen_size[0] - 20 - 100 * 4, h-40, 100 * 4, 15))
        pg.draw.rect(screen, (215, 215, 215),
                         (20, h-40, (Player1.PROPERTY['Energy'] // Player1.PROPERTY['EnergyPercent']) * 4, 15))
        pg.draw.rect(screen, (215, 215, 215), (
                screen_size[0] - 20 - (Player2.PROPERTY['Energy'] //
                                       Player2.PROPERTY['EnergyPercent']) * 4, h-40,
                (Player2.PROPERTY['Energy'] // Player2.PROPERTY['EnergyPercent']) * 4, 15))
        # Text Surface
        timer = RESOURCES['Fonts']['F1 Large'].render(
                    str(_time), 1, (255, 255, 255))
        return [[xp_r, (screen_size[0] - 30 - xp_r.get_rect()[2], 60)],
                [xp_l, (30, 60)],
                [FPS, (w//2-FPS.get_rect().width//2, h - h // 20)],
                [timer, (screen_size[0] // 2 - (timer.get_rect().width) / 2, 20)]]
    while FightingRun != Stopped:
        if FightingRun == Running:
            screen.blit(bg.image,bg.rect)
            Actions = [[],[]]
            Layer1, Layer2, Layer3 = [],[],[]
            # Music
            if Music:
                pg.mixer.music.set_volume(1)
                pg.mixer.music.play(-1, 0.0 if MusicPos <
                                    1 else MusicPos // 1000)
                Music = False
                CWins = [0, 0, 0]
                for i in RoundWins:
                    CWins[i] += 1
            # Clicks and events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    FightingRun = Stopped
                    SCREENS[2] = EXIT_SCR
                if event.type == pg.KEYDOWN:
                    if event.key == 27:
                        FightingRun = Paused
                    elif event.key == pg.K_SPACE:
                        Player1.flip()
                        Player2.flip()
            if Ctrl==1:
                keys = pg.key.get_pressed()
                if sum(keys)!=0:
                    for key in Controler1['ControlKeys']:
                        if keys[Controler1['ControlKeys'][key]]:
                            Actions[0].append(key)
                    if not False:
                        for key in Controler2['ControlKeys']:
                            if keys[Controler2['ControlKeys'][key]]:
                                Actions[1].append(key)
                if not True:
                    Distation = Player2.PROPERTY['BodyRect'].left - Player1.PROPERTY['BodyRect'].right
                    Energy = Player2.PROPERTY['Energy']/Player2.PROPERTY['EnergyPercent']
                    if 150>=Distation>=50:
                        Actions[1].append('Left')
                    elif 300>=Distation>150 and Energy>=30:
                        Actions[1].append('Kick')
                    elif 300>=Distation>150 and Energy<30:
                        Actions[1].append('Right')
                    elif Distation>300 and Energy<70:
                        Actions[1].append('Recovery')
                    elif Distation>300 and Energy>=70:
                        Actions[1].append('Kick')
                    else:
                        Actions[1].append('Punch')
            # Time in game
            if HSE == 1:
                seconds = (pg.time.get_ticks() - start_ticks) // 1000 - _TIME_
                timer = TIME
            if seconds == TIME + _TIME_:
                timer = 'Время истекло'
                pg.mixer.music.set_volume(0.3)
            elif seconds == -2 and HSE == 1:
                TIME_ENDING = -255
                RESOURCES['Sounds']['Round' + str(Round)].play()
                SoundTimes[0] = (pg.time.get_ticks() -
                                 start_ticks) / 1000 - 1.3
                SoundTimes[2] = RESOURCES['Sounds']['Round' +
                                                    str(Round)].get_length()
                HSE = 2
            elif HSE == 2:
                SoundTimes[1] = (pg.time.get_ticks() - start_ticks) / 1000
                if SoundTimes[1] - SoundTimes[2] <= SoundTimes[0]:
                    pass
                else:
                    RESOURCES['Sounds']['Fight'].play()
                    SoundTimes[0] = (pg.time.get_ticks() -
                                     start_ticks) / 1000 - 0.7
                    SoundTimes[2] = RESOURCES['Sounds']['Fight'].get_length()
                    HSE = 3
            elif HSE == 3:
                SoundTimes[1] = (pg.time.get_ticks() - start_ticks) / 1000
                if SoundTimes[1] - SoundTimes[2] <= SoundTimes[0]:
                    pass
                else:
                    HSE = 0
                    seconds = 0
            elif seconds == 0 and HSE == 0:
                seconds = 1
                HSE = TIME_ENDING
            elif seconds > 0:
                seconds = (pg.time.get_ticks() -
                           start_ticks) // 1000 - int(SoundTimes[0])
                timer = TIME - (seconds - _TIME_)
                Ctrl = 1
            
            # The end
            if HSE == -1:
                if Round == AllRounds:
                    FightingRun = Stopped
                    SCREENS[3] = RoundWins
                    SCREENS[2] = GAMEOVER_SCR
                else:
                    start_ticks = pg.time.get_ticks()
                    Player1 = Fighter(DataReader(_Player1_))
                    Player2 = Fighter(DataReader(_Player2_))
                    Player2.flip()
                    Round += 1
                    TIME = RoundTime
                    HSE = 1
                    Music = True
            Layer1 = ShowUI(Player1,Player2,timer)
            Player1.draw(Player2, Actions[0])
            Player2.draw(Player1, Actions[1])
            Layer2.extend(Player1.LAYERDOWN)
            Layer2.extend(Player2.LAYERDOWN)
            if Player1.LAYERUP != []:
                Layer3.extend(Player1.LAYERUP)
            if Player2.LAYERUP != []:
                Layer3.extend(Player2.LAYERUP)
            if seconds >= TIME + _TIME_ or (Player2.PROPERTY['Healf'] <= 0) or (Player1.PROPERTY['Healf'] <= 0):
                if (Player1.PROPERTY['Healf'] <= 0):
                    RoundWins[Round - 1] = 2
                elif (Player2.PROPERTY['Healf'] <= 0):
                    RoundWins[Round - 1] = 1
                else:
                    if Player1.PROPERTY['Healf'] < Player2.PROPERTY['Healf']:
                        RoundWins[Round - 1] = 2
                    elif Player1.PROPERTY['Healf'] > Player2.PROPERTY['Healf']:
                        RoundWins[Round - 1] = 1
                pg.mixer.music.set_volume(0.2)
                if Round == AllRounds:
                    Layer1.append([GameOverText, (w // 2 - GameOverText.get_rect().width // 2, 75)])
                if HSE > (-255 // 8):
                    if Round == AllRounds:
                        RGBA = [0, 0, 0, 235 + HSE * 7 if 235 + HSE * 8>=0 else 0]
                    else:
                        RGBA = [0, 0, 0, 255 + HSE * 8 if 235 + HSE * 8>=0 else 0]
                    pg.draw.rect(surf, RGBA, bg.rect)
                    Layer3.append([surf, (0, 0)])
                Ctrl = 0
                HSE += 1
            if HSE == 1:
                RGBA = [0, 0, 0, -TIME_ENDING]
                pg.draw.rect(surf, RGBA, bg.rect)
                TIME_ENDING += 10 if TIME_ENDING <= -8 else 0
                Layer3.append([surf, (0, 0)])
            OnShow(screen,Layer1)
            OnShow(screen,Layer2)
            if len(Layer3)>0:
                OnShow(screen,Layer3)
            pg.display.update()
        elif FightingRun == Paused:
            MCS = False
            if PAUSE[0] == 0:
                pg.draw.rect(surf, (0, 0, 0, 200), bg.rect)
                screen.blit(surf, (0, 0))
            screen.blit(GOSurf, (0, 0))
            screen.blit(WTSurf, (0, MR_pad))
            if SCREENS[3] != 0 or PAUSE[0] == 0:
                pg.display.update()
                SCREENS[3] = 0
                Title = RESOURCES['Fonts']['F0 Large2'].render(
                    str(CWins[1]) + ' : ' + str(CWins[2]), 1, MC[-1])
                OnShow(screen, [[Title, (
                    WTSurf.get_rect().width - WTSurf.get_rect().width // 4 - Title.get_rect().width // 2, MR_pad * 3)]])
                pg.mixer.music.pause()
                PAUSE[0] = pg.time.get_ticks()
                pg.display.update()
            PAUSE[1] = (pg.time.get_ticks() - PAUSE[0]) // 1000
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    FightingRun = Stopped
                if event.type == pg.MOUSEMOTION:
                    MP = pg.mouse.get_pos()
                    MousePos = pg.Rect(MP[0], MP[1], 1, 1).collidelist(MIL)
                    if MousePos >= 0:
                        MIM[MIM.index([1])] = [0]
                        MIM[MousePos] = [1]
                if event.type == pg.MOUSEBUTTONUP:
                    MP = pg.mouse.get_pos()
                    if (pg.Rect(MP[0], MP[1], 1, 1).collidelist(MIL) >= 0) and event.button == 1:
                        MCS = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        CS_Helper(1, 'Up', MIM)
                    elif event.key == pg.K_DOWN:
                        CS_Helper(1, 'Down', MIM)
                    elif event.key == 13:
                        MCS = True
                    elif event.key == pg.K_ESCAPE:
                        FightingRun = Running
                        PAUSE[0] = 0
                        pg.mixer.music.unpause()
                        TIME += PAUSE[1]
            RectID = MIM.index([1])
            if RectID >= 0:
                pg.draw.rect(screen, MC[-2], MIL[RectID])
                screen.blit(MIT[RectID], MITL[RectID])
                if MCS:
                    if RectID == 0:
                        FightingRun = Running
                        PAUSE[0] = 0
                        pg.mixer.music.unpause()
                        TIME += PAUSE[1]
                        SCREENS[3] = 0
                    elif RectID == 1:
                        FightingRun = Stopped
                        SCREENS[2] = FIGHTING_SCR
                        SCREENS[3] = 0
                    elif RectID == 2:
                        FightingRun = Stopped
                        SCREENS[0] = START_SCR
                        SCREENS[2] = CHARSEL_SCR
                    elif RectID == 3:
                        FightingRun = Stopped
                        SCREENS[0] = FIGHTING_SCR
                        SCREENS[2] = SETTING_SCR
                        SCREENS[3] = [pg.mixer.music.get_pos(), Round, PAUSE, RoundWins, TIME, HSE, start_ticks,
                                      seconds, CWins, Player1.PROPERTY['BodyRect'], Player2.PROPERTY['BodyRect'],
                                      Player1.PROPERTY['Healf'], Player2.PROPERTY['Healf'], timer]
                    elif RectID == 4:
                        FightingRun = Stopped
                        SCREENS[0] = START_SCR
                        SCREENS[2] = 0
                    elif RectID == 5:
                        FightingRun = Stopped
                        SCREENS[2] = EXIT_SCR
            pg.display.update(MIL)
        # GSs['MaxFPS
        clock.tick(GSs['MaxFPS'])
    ScreenChanger(SCREENS)
def GameOver(_Player1_, _Player2_, _RoundWins_):
    global SCREENS, DEFAULT_PLAYERS
    if SCREENS[1] == SETTING_SCR:
        surf = pg.Surface(screen_size, pg.SRCALPHA)
        pg.draw.rect(surf, (0, 0, 0, 200), surf.get_rect())
        screen.blit(bg.image, bg.rect)
        screen.blit(surf, (0, 0))
        pg.display.update()
    SCREENS[1] = GAMEOVER_SCR
    GO_Run = True
    MITs = ['ЕЩЁ РАЗ', 'НАСТРОЙКИ', 'ВЫБОР ПЕРСОНАЖЕЙ',
            'ГЛАВНЫЙ ЭКРАН', 'ЗАВЕРШИТЬ ИГРУ']
    MIL = [0 for i in range(len(MITs))]
    MIT, MITL = MIL.copy(), MIL.copy()
    MIM = [[1 if i == 0 else 0] for i in range(len(MITs))]
    MC = [[0, 0, 0], [25, 25, 25], [40, 40, 40], [241, 51, 19], [255, 255, 255]]
    GOSurf = pg.Surface(
        (screen_size[0] // 3 + w // 15, screen_size[1]), pg.SRCALPHA)
    GOSL = []
    MR_height = h // 13
    MR_pad = (h // 2 - MR_height * 5) // 5
    MenuRectBG = pg.Rect(w // 15, 0, screen_size[0] // 3, screen_size[1])
    MenuRectItem = pg.Rect(MenuRectBG[0] + MR_pad // 2, MenuRectBG[1] + h // 5 + MR_pad * 2, MenuRectBG[2] - MR_pad,
                           MR_height)
    pg.draw.rect(GOSurf, MC[2], MenuRectBG)
    for i in range(len(MITs)):
        MIL[i] = pg.draw.rect(GOSurf, MC[1], MenuRectItem)
        MIT[i] = RESOURCES['Fonts']['F0 Small'].render(MITs[i], 1, MC[-1])
        MITL[i] = pg.Rect(MenuRectItem.centerx - MIT[i].get_rect().width // 2,
                          MenuRectItem.centery -
                          MIT[i].get_rect().height // 2, MIT[i].get_rect().width,
                          MIT[i].get_rect().height)
        GOSL.append([MIT[i], MITL[i]])
        MenuRectItem.y += MR_height + MR_pad
    OnShow(GOSurf, GOSL)
    CWins = [0, 0, 0]
    for i in _RoundWins_:
        CWins[i] += 1
    WTSurf = pg.Surface((screen_size[0], h // 5), pg.SRCALPHA)
    WTSL = []
    pg.draw.rect(WTSurf, MC[-2], WTSurf.get_rect())
    Title = RESOURCES['Fonts']['F1 Large2'].render('Игра окончена', 1, MC[-1])
    WTSL.append(
        [Title, (h // 15, WTSurf.get_rect().centery - Title.get_rect().height // 2)])
    TitleVS = RESOURCES['Fonts']['F0 Small'].render('vs', 1, MC[-1])
    VSCoords = (WTSurf.get_rect().width - WTSurf.get_rect().width //
                4 - TitleVS.get_rect().width // 2, MR_pad * 1.5)
    WTSL.append([TitleVS, VSCoords])
    TitleP1 = RESOURCES['Fonts']['F1 Medium'].render(
        CharactersNames[_Player1_[0]].upper(), 1, MC[-1])
    WTSL.append(
        [TitleP1, (VSCoords[0] - MR_pad - TitleP1.get_rect().width, MR_pad * 1.5)])
    TitleP2 = RESOURCES['Fonts']['F1 Medium'].render(
        CharactersNames[_Player2_[0]].upper(), 1, MC[-1])
    WTSL.append(
        [TitleP2, (VSCoords[0] + MR_pad + TitleVS.get_rect().width, MR_pad * 1.5)])
    Title = RESOURCES['Fonts']['F0 Large2'].render(
        str(CWins[1]) + ' : ' + str(CWins[2]), 1, MC[-1])
    WTSL.append(
        [Title, (WTSurf.get_rect().width - WTSurf.get_rect().width // 4 - Title.get_rect().width // 2, MR_pad * 3)])
    OnShow(WTSurf, WTSL)
    screen.blit(GOSurf, (0, 0))
    screen.blit(WTSurf, (0, MR_pad))
    pg.display.update()
    RectID = 0
    while GO_Run:
        MCS = False
        screen.blit(GOSurf, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                GO_Run = False
            if event.type == pg.MOUSEMOTION:
                MP = pg.mouse.get_pos()
                MousePos = pg.Rect(MP[0], MP[1], 1, 1).collidelist(MIL)
                if MousePos >= 0:
                    MIM[MIM.index([1])] = [0]
                    MIM[MousePos] = [1]
            if event.type == pg.MOUSEBUTTONUP:
                MP = pg.mouse.get_pos()
                if (pg.Rect(MP[0], MP[1], 1, 1).collidelist(MIL) >= 0) and event.button == 1:
                    MCS = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    CS_Helper(1, 'Up', MIM)
                elif event.key == pg.K_DOWN:
                    CS_Helper(1, 'Down', MIM)
                if event.key == 13:
                    MCS = True
        RectID = MIM.index([1])
        if RectID >= 0:
            pg.draw.rect(screen, MC[-2], MIL[RectID])
            screen.blit(MIT[RectID], MITL[RectID])
            if MCS:
                if RectID == 0:
                    GO_Run = False
                    SCREENS[0] = START_SCR
                    SCREENS[2] = FIGHTING_SCR
                    SCREENS[3] = 0
                elif RectID == 1:
                    GO_Run = False
                    SCREENS[0] = GAMEOVER_SCR
                    SCREENS[2] = SETTING_SCR
                elif RectID == 2:
                    GO_Run = False
                    SCREENS[0] = START_SCR
                    SCREENS[2] = CHARSEL_SCR
                elif RectID == 3:
                    GO_Run = False
                    SCREENS[0] = START_SCR
                    SCREENS[1] = START_SCR
                    SCREENS[2] = START_SCR
                    SCREENS[3] = 0
                elif RectID == 4:
                    GO_Run = False
                    SCREENS[2] = EXIT_SCR
        pg.display.update(MIL)
    ScreenChanger(SCREENS)
def SS(MISSING_TIME=0, SPROGRESS=1):
    global SCREENS, DEFAULT_PLAYERS
    SCREENS[1] = START_SCR
    # Фоновое изображение
    StartBG = BG('bg2.png', (0, 0), screen_size)
    SS_Run = True
    EnterPress = False
    # Элементы главного меню
    MIS = pg.image.load('Backgrounds/graphics/MMI_simple.png').convert_alpha()
    MIP = pg.image.load('Backgrounds/graphics/MMI_active.png').convert_alpha()
    MIL, MIM = [0, 0, 0, 0], [[1], [0], [0], [0]]
    MITs, MIT = ['Быстрая игра', 'Начать бой',
                 'Настройки (Скоро...)', 'Завершить игру'], [0, 0, 0, 0]
    # Цвета
    MC = [[0, 0, 0, 100], [25, 25, 25, 100], [40, 40, 40, 100], [15, 15, 15, 100], [255, 162, 0], [0, 162, 232],
          [255, 255, 255]]
    # Таймер
    start_ticks = pg.time.get_ticks()
    # Поверхности
    # Эффект угасания
    surf = pg.Surface(screen_size, pg.SRCALPHA)
    # Первый экран
    LogoSurf = pg.Surface(screen_size, pg.SRCALPHA)
    LogoSL = []
    SS_Title = RESOURCES['Fonts']['F1 Large3'].render('Happy END', 1, MC[-2])
    SS_SubTitle = RESOURCES['Fonts']['F1 Medium2'].render(
        'Python Gaming', 1, MC[-2])
    LogoSL.append([SS_SubTitle,
                   pg.Rect(w // 2 - SS_SubTitle.get_rect().width // 2, h // 2 + 25, SS_SubTitle.get_rect().width,
                           SS_SubTitle.get_rect().height)])
    LogoSL.append([SS_Title,
                   pg.Rect(w // 2 - SS_Title.get_rect().width // 2, h // 2 - 125, SS_Title.get_rect().width,
                           SS_Title.get_rect().height)])
    OnShow(LogoSurf, LogoSL)
    # Второй экран
    PowSurf = pg.Surface(screen_size, pg.SRCALPHA)
    PowSL = []
    SS_Title = RESOURCES['Fonts']['F1 Large2'].render(
        'КРИВОРУКАЯ АНИМАЦИЯ', 1, MC[-3])
    SS_SubTitle = RESOURCES['Fonts']['F1 Medium2'].render(
        'Powered by', 1, MC[-1])
    SS_SubTitle2 = RESOURCES['Fonts']['F1 Large'].render('And', 1, MC[-1])
    PowSL.append([SS_SubTitle, pg.Rect(w // 2 - SS_SubTitle.get_rect().width // 2, 100, SS_SubTitle.get_rect().width,
                                       SS_SubTitle.get_rect().height)])
    PowSL.append([SS_SubTitle2, (w // 2 - SS_SubTitle2.get_rect().width // 2, h // 1.8, SS_SubTitle2.get_rect().width,
                                 SS_SubTitle2.get_rect().height)])
    PowSL.append([SS_Title, (
        w // 2 - SS_Title.get_rect().width // 2, h // 4 + 50, SS_Title.get_rect().width, SS_Title.get_rect().height)])
    PG_Logo = pg.image.load('PyGame.png').convert()
    PG_Rect = PG_Logo.get_rect(center=(w // 2, h // 1.2))
    PowSL.append([PG_Logo, PG_Rect])
    OnShow(PowSurf, PowSL)
    # Третий экран
    PreSurf = pg.Surface(screen_size, pg.SRCALPHA)
    PreSL = []
    SS_Title = RESOURCES['Fonts']['F1 Large2'].render(
        'представляет', 1, MC[-1])
    PreSL.append(
        [SS_Title, pg.Rect(w // 2 - SS_Title.get_rect().width // 2, h // 2 - SS_Title.get_rect().height // 2,
                           SS_Title.get_rect().width, SS_Title.get_rect().height)])
    OnShow(PreSurf, PreSL)
    # Главный экран
    MainSurf = pg.Surface(screen_size, pg.SRCALPHA)
    MainSL = []
    MainSL.append([StartBG.image, StartBG.rect])
    SS_Player2 = pg.image.load('Backgrounds/Player2.png').convert_alpha()
    SS_Player2R = SS_Player2.get_rect(bottomleft=(w - w // 3, h))
    SS_Player1 = pg.image.load('Backgrounds/Player1.png').convert_alpha()
    SS_Player1R = SS_Player1.get_rect(bottomleft=(w // 10, h))
    MainSL.append([SS_Player2, SS_Player2R])
    MainSL.append([SS_Player1, SS_Player1R])
    SS_Title = RESOURCES['Fonts']['F1 Large3'].render('ФАЙТИНГ', 1, MC[-1])
    MainSL.append([SS_Title, pg.Rect(w // 2 - SS_Title.get_rect().width // 2, h // 10, SS_Title.get_rect().width,
                                     SS_Title.get_rect().height)])
    SS_SubTitle = RESOURCES['Fonts']['F1 Medium'].render(
        'с кривой графикой', 1, MC[-1])
    MainSL.append([SS_SubTitle,
                   pg.Rect(w // 1.8, h // 10 + SS_Title.get_rect().height // 1.2, SS_SubTitle.get_rect().width,
                           SS_SubTitle.get_rect().height)])
    SS_SubTitle2 = RESOURCES['Fonts']['F0 Small2'].render(
        'нажмите enter чтобы продолжить', 1, MC[-1])
    MainSL.append([SS_SubTitle2,
                   pg.Rect(w // 2 - SS_SubTitle2.get_rect().width // 2, h - 50, SS_SubTitle2.get_rect().width,
                           SS_SubTitle2.get_rect().height)])
    OnShow(MainSurf, MainSL)
    # Главное меню
    MainMSurf = pg.Surface(screen_size, pg.SRCALPHA)
    MainMSL = []
    MainMSL.append([StartBG.image, StartBG.rect])
    MR_height = h // 25
    MR_pad = (h // 2 - MR_height) // 3
    MenuRectBG = pg.Rect(0, 0, screen_size[0], screen_size[0])
    MenuRectItem = pg.Rect(MR_pad, MR_pad,
                           MIS.get_rect().width, MIS.get_rect().height)
    # pg.draw.rect(MainMSurf, MC[-1], MenuRectBG)
    for i in range(len(MIL)):
        MIL[i] = MIS.get_rect(center=MenuRectItem.center)
        MainMSL.append([MIS, MIL[i]])
        MIT[i] = RESOURCES['Fonts']['F1 Small'].render(MITs[i], 1, MC[-1])
        MIT[i] = [MIT[i], pg.Rect(MenuRectItem.left + MR_pad,
                                  MenuRectItem.centery -
                                  MIT[i].get_rect(
                                  ).height // 3, MIT[i].get_rect().width,
                                  MIT[i].get_rect().height)]
        MainMSL.append([MIT[i][0], MIT[i][1]])
        MenuRectItem.y += MR_height + MR_pad
    OnShow(MainMSurf, MainMSL)
    MainMSL.remove([StartBG.image, StartBG.rect])
    # Коэффициент прозрачности
    ANC = 255
    # Скорость изменения коэф. прозрачности
    ANCC = -9
    # Музыка
    pg.mixer.music.load(os.path.join('Backgrounds/musics', 'bg.mp3'))
    pg.mixer.music.set_volume(0.3)
    pg.mixer.music.play(-1)
    # Обновляемые участки поверхности
    ShowingList = LogoSL
    while SS_Run:
        screen.fill(MC[0])
        seconds = (pg.time.get_ticks() - start_ticks) // 1000 + MISSING_TIME
        showlist = []
        if SPROGRESS < 4:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    SS_Run = False
                    SCREENS[2] = EXIT_SCR
                elif event.type == pg.KEYDOWN:
                    if event.key == 13:
                        MISSING_TIME += SPROGRESS * 3 - seconds
                        EnterPress = True
                        ANC = 255 if SPROGRESS <= 4 else 0
                        SPROGRESS += 1
                    elif event.key == pg.K_ESCAPE:
                        SS_Run = False
                        SCREENS[2] = EXIT_SCR
        if seconds <= 2:
            if seconds > 1:
                ANC -= ANCC
            else:
                ANC += ANCC
            if ANC < 0:
                ANC = 0
            if ANC > 255:
                ANC = 255
            pg.draw.rect(surf, (0, 0, 0, ANC),
                         (0, 0, screen_size[0], screen_size[0]))
            showlist.append([LogoSurf, (0, 0)])
        elif seconds <= 5:
            SPROGRESS = 2
            if seconds > 4:
                ANC -= ANCC
            else:
                ANC += ANCC
            if ANC < 0:
                ANC = 0
            if ANC > 255:
                ANC = 255
            pg.draw.rect(surf, (0, 0, 0, ANC),
                         (0, 0, screen_size[0], screen_size[0]))
            showlist.append([PowSurf, (0, 0)])
            ShowingList = PowSL
        elif seconds <= 8:
            SPROGRESS = 3
            if seconds > 7:
                ANC -= ANCC
            else:
                ANC += ANCC
            if ANC < 0:
                ANC = 0
            if ANC > 255:
                ANC = 255
            pg.draw.rect(surf, (0, 0, 0, ANC),
                         (0, 0, screen_size[0], screen_size[1]))
            showlist.append([PreSurf, (0, 0)])
            ShowingList = PreSL
        else:
            if ANC > 0:
                ANC += ANCC
            elif ANC < 0:
                ANC = 0
            if SPROGRESS == 3:
                showlist.append([MainSurf, (0, 0)])
                if ANC > 0:
                    ShowingList = MainSL
                else:
                    ANCC = -20
                    ShowingList = [[0, pg.Rect(0, 0, 0, 0)]]
            elif SPROGRESS == 4:
                MCS = False
                showlist.append([MainMSurf, (0, 0)])
                if ANC > 0:
                    ShowingList = MainSL
                else:
                    ShowingList = MainMSL
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        SS_Run = False
                        SCREENS[0] = START_SCR
                        SCREENS[2] = 0
                    if event.type == pg.MOUSEMOTION:
                        MP = pg.mouse.get_pos()
                        MousePos = pg.Rect(MP[0], MP[1], 1, 1).collidelist(MIL)
                        if MousePos >= 0:
                            MIM[MIM.index([1])] = [0]
                            MIM[MousePos] = [1]
                    elif event.type == pg.MOUSEBUTTONUP:
                        MP = pg.mouse.get_pos()
                        if (pg.Rect(MP[0], MP[1], 1, 1).collidelist(MIL) >= 0) and event.button == 1:
                            MCS = True
                    elif event.type == pg.KEYDOWN:
                        if event.key == 13:
                            MCS = True
                        if event.key == 27:
                            SPROGRESS = 3
                            ANC = 255
                            ANCC = -9
                        if event.key == pg.K_UP:
                            CS_Helper(1, 'Up', MIM)
                        elif event.key == pg.K_DOWN:
                            CS_Helper(1, 'Down', MIM)
                RectID = MIM.index([1])
                if RectID >= 0:
                    showlist.append([MIP, MIL[RectID]])
                    showlist.append([MIT[RectID][0], MIT[RectID][1]])
                    if MCS:
                        if RectID == 0:
                            _Player1_ = rd(0, len(CharDoneIds) - 1)
                            _Player2_ = rd(0, len(CharDoneIds) - 1)
                            while _Player1_ == _Player2_:
                                _Player2_ = rd(0, len(CharDoneIds) - 1)
                            DEFAULT_PLAYERS = [[_Player1_, -1, 0], [_Player2_, -1, 1]]
                            SS_Run = False
                            SCREENS[0] = START_SCR
                            SCREENS[2] = FIGHTING_SCR
                        elif RectID == 1:
                            SS_Run = False
                            SCREENS[0] = START_SCR
                            SCREENS[2] = CHARSEL_SCR
                        elif RectID == 2:
                            SS_Run = False
                            SCREENS[0] = START_SCR
                            SCREENS[2] = SETTING_SCR
                        elif RectID == 3:
                            SS_Run = False
                            SCREENS[2] = EXIT_SCR
            if ANC > 0:
                pg.draw.rect(surf, (0, 0, 0, ANC), (0, 0, w, h))
        showlist.append([surf, (0, 0)])
        OnShow(screen, showlist)
        showlist.remove([surf, (0, 0)])
        if EnterPress and SPROGRESS < 4:
            EnterPress = False
            screen.fill(MC[0])
            pg.display.update()
        else:
            OnShow(0, ShowingList)
    ScreenChanger(SCREENS)
def CharacterSelection():
    global SCREENS, DEFAULT_PLAYERS
    bg = BG('bg4.jpg', (0, 0), screen_size)
    SCREENS[1] = CHARSEL_SCR
    CS_Run = True
    Players = [-1, -1]
    RectSizes = w // 3 // 4
    RectPadding = (w // 3 - RectSizes * 3) // 10
    TitleSurf = pg.Surface((w, RectSizes * 3 / 1.5), pg.SRCALPHA)
    pg.draw.rect(TitleSurf, (0, 0, 0, 175), (0, 0, w, RectSizes - RectPadding))
    Title = RESOURCES['Fonts']['F1 Large'].render(
        'ВЫБЕРИТЕ БОЙЦОВ', 1, (255, 255, 255))
    Player1_Text = RESOURCES['Fonts']['F1 Medium'].render(
        'Игрок 1', 1, (255, 255, 255))
    Player2_Text = RESOURCES['Fonts']['F1 Medium'].render(
        'Игрок 2', 1, (255, 255, 255))
    Player1_TextBG = pg.image.load(
        'Backgrounds/graphics/CS_textbg1.png').convert_alpha()
    Player1_TextBG = pg.transform.scale(Player1_TextBG, (
        Player1_Text.get_rect().width + RectPadding, Player1_Text.get_rect().height + RectPadding))
    Player2_TextBG = pg.image.load(
        'Backgrounds/graphics/CS_textbg2.png').convert_alpha()
    Player2_TextBG = pg.transform.scale(Player2_TextBG, (
        Player2_Text.get_rect().width + RectPadding * 2, Player2_Text.get_rect().height + RectPadding))
    OnShow(TitleSurf,
           [[Player1_TextBG, (w // 3 // 2 - Player1_Text.get_rect().width // 2 - RectPadding, RectSizes + RectPadding)],
            [Player2_TextBG,
             (w - w // 3 // 2 - Player2_Text.get_rect().width // 2 - RectPadding, RectSizes + RectPadding)]])
    OnShow(TitleSurf, [[Title, (w // 2 - Title.get_rect().width // 2, RectPadding * 2)],
                       [Player1_Text, (w // 3 // 2 - Player1_Text.get_rect().width //
                                       2, RectSizes + RectPadding * 2)],
                       [Player2_Text,
                        (w - w // 3 // 2 - Player2_Text.get_rect().width // 2, RectSizes + RectPadding * 2)]])
    CharSurf = pg.Surface((w // 3, h), pg.SRCALPHA)
    pg.draw.rect(CharSurf, (50, 50, 50, 120), (0, RectSizes -
                                               RectPadding, w // 3, h - RectSizes + RectPadding))
    showlist = []
    for i in range(5):
        for j in range(3):
            CharPic = pg.image.load(
                'Backgrounds/graphics/' + str(i * 3 + j) + '.png').convert()
            CharPic = pg.transform.scale(CharPic, (RectSizes, RectSizes))
            showlist.append([CharPic, (
                (RectSizes + RectPadding * 2) * j + RectPadding * 3, (RectSizes + RectPadding) * i + RectSizes)])
            # pg.draw.rect(CharSurf, (rrr(0, 255), rrr(0, 255), rrr(0, 255)), (
            # (RectSizes + RectPadding * 2) * j + RectPadding * 3, (RectSizes + RectPadding) * i + RectSizes, RectSizes,
            # RectSizes))
    OnShow(CharSurf, showlist)
    ControlData = [DataReader([-1, 0])['ControlKeys'],
                   DataReader([-1, 1])['ControlKeys']]
    DonePlayers = [False, False]
    while CS_Run:  # and CS_PROGRESS < len(KeysCS):
        showlist = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                CS_Run = False
                SCREENS[2] = EXIT_SCR
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    CS_Run = False
                    SCREENS[2] = 0
                if not DonePlayers[1]:
                    if event.key == ControlData[1]['Up']:
                        CS_Helper(2, 'Up')
                    elif event.key == ControlData[1]['Down']:
                        CS_Helper(2, 'Down')
                    elif event.key == ControlData[1]['Left']:
                        CS_Helper(2, 'Left')
                    elif event.key == ControlData[1]['Right']:
                        CS_Helper(2, 'Right')
                    elif event.key == ControlData[1]['Punch']:
                        RESOURCES['Sounds']['Select'].play()
                        DonePlayers[1] = True
                else:
                    if event.key == ControlData[1]['Kick']:
                        DonePlayers[1] = False

                if not DonePlayers[0]:
                    if event.key == ControlData[0]['Up']:
                        CS_Helper(1, 'Up')
                    elif event.key == ControlData[0]['Down']:
                        CS_Helper(1, 'Down')
                    elif event.key == ControlData[0]['Left']:
                        CS_Helper(1, 'Left')
                    elif event.key == ControlData[0]['Right']:
                        CS_Helper(1, 'Right')
                    elif event.key == ControlData[0]['Punch']:
                        RESOURCES['Sounds']['Select'].play()
                        DonePlayers[0] = True
                else:
                    if event.key == ControlData[0]['Kick']:
                        DonePlayers[0] = False
        showlist.append([bg.image, bg.rect])
        showlist.append([CharSurf, (w // 2 - w // 3 // 2, 0)])
        showlist.append([TitleSurf, (0, 0)])
        OnShow(screen, showlist)
        showlist = []
        for i in range(len(CharMatrix)):
            for j in range(len(CharMatrix[i])):
                if CharMatrix[i][j] == 1:
                    Players[0] = i * 3 + j
                    pg.draw.rect(screen, (56, 151, 240),
                                 (w // 2 - w // 3 // 2 + (RectSizes + RectPadding * 2) * j + RectPadding * 3,
                                  (RectSizes + RectPadding) * i + RectSizes, RectSizes, RectSizes), 6)
                    if DonePlayers[0]:
                        pg.draw.polygon(screen, (56, 151, 240), [
                            [RectSizes + w // 2 - w // 3 // 2 + (RectSizes + RectPadding * 2) * j + RectPadding * 3,
                             (RectSizes + RectPadding) * i + RectSizes * 2],
                            [RectSizes // 1.5 + w // 2 - w // 3 // 2 + (
                                RectSizes + RectPadding * 2) * j + RectPadding * 3,
                             (RectSizes + RectPadding) * i + RectSizes * 2],
                            [RectSizes + w // 2 - w // 3 // 2 + (RectSizes + RectPadding * 2) * j + RectPadding * 3,
                             (RectSizes + RectPadding) * i + RectSizes * 1.6]])
                    Player1_Text = RESOURCES['Fonts']['F1 Large'].render(
                        CharactersNames[i * 3 + j], 1, (240, 240, 240))
                    Player1_TextBG = pg.image.load(
                        'Backgrounds/graphics/CS_textbg1.png').convert_alpha()
                    Player1_TextBG = pg.transform.scale(Player1_TextBG, (
                        Player1_Text.get_rect().width + RectPadding * 2,
                        Player1_Text.get_rect().height + int(RectPadding // 1.5)))
                    CharPic1 = pg.image.load(
                        'Characters/' + CharactersIds[i * 3 + j] + '/Prev.png').convert_alpha()
                    CharPic1s = (
                        int(w // 4.2), int(CharPic1.get_rect().height * (w // 4.2 / CharPic1.get_rect().width)))
                    CharPic1 = pg.transform.scale(CharPic1, CharPic1s)
                    showlist.append([CharPic1, CharPic1.get_rect(
                        bottomleft=(RectSizes // 3, h - RectSizes // 4))])
                    showlist.append([Player1_TextBG, (w // 3 // 2 - Player1_Text.get_rect().width // 2 - RectPadding,
                                                      h - RectSizes // 1.5 - RectPadding)])
                    showlist.append(
                        [Player1_Text, (w // 3 // 2 - Player1_Text.get_rect().width // 2, h - RectSizes // 1.5)])
                elif CharMatrix[i][j] == 2:
                    Players[1] = i * 3 + j
                    pg.draw.rect(screen, (237, 0, 19), (
                        w // 2 - w // 3 // 2 +
                        (RectSizes + RectPadding * 2) * j + RectPadding * 3,
                        (RectSizes + RectPadding) * i + RectSizes, RectSizes, RectSizes), 6)
                    if DonePlayers[1]:
                        pg.draw.polygon(screen, (237, 0, 19), [
                            [RectSizes + w // 2 - w // 3 // 2 + (RectSizes + RectPadding * 2) * j + RectPadding * 3,
                             (RectSizes + RectPadding) * i + RectSizes * 2],
                            [RectSizes // 1.5 + w // 2 - w // 3 // 2 + (
                                RectSizes + RectPadding * 2) * j + RectPadding * 3,
                             (RectSizes + RectPadding) * i + RectSizes * 2],
                            [RectSizes + w // 2 - w // 3 // 2 + (RectSizes + RectPadding * 2) * j + RectPadding * 3,
                             (RectSizes + RectPadding) * i + RectSizes * 1.6]])
                    Player2_Text = RESOURCES['Fonts']['F1 Large'].render(
                        CharactersNames[i * 3 + j], 1, (240, 240, 240))
                    Player2_TextBG = pg.image.load(
                        'Backgrounds/graphics/CS_textbg2.png').convert_alpha()
                    Player2_TextBG = pg.transform.scale(Player2_TextBG, (
                        Player2_Text.get_rect().width + RectPadding * 2,
                        Player2_Text.get_rect().height + int(RectPadding // 1.5)))
                    CharPic2 = pg.image.load(
                        'Characters/' + CharactersIds[i * 3 + j] + '/Prev.png').convert_alpha()
                    CharPic2 = pg.transform.flip(CharPic2, 1, 0)
                    CharPic2s = (
                        int(w // 4.2), int(CharPic2.get_rect().height * (w // 4.2 / CharPic2.get_rect().width)))
                    CharPic2 = pg.transform.scale(CharPic2, CharPic2s)
                    showlist.append([CharPic2, CharPic2.get_rect(
                        bottomright=(w - RectSizes // 3, h - RectSizes // 4))])
                    showlist.append([Player2_TextBG, (
                        w - w // 3 // 2 - Player2_Text.get_rect().width // 2 - RectPadding,
                        h - RectSizes // 1.5 - RectPadding)])
                    showlist.append(
                        [Player2_Text, (w - w // 3 // 2 - Player2_Text.get_rect().width // 2, h - RectSizes // 1.5)])
        OnShow(screen, showlist)
        if DonePlayers[0] and DonePlayers[1]:
            CS_Run = False
            SCREENS[0] = FIGHTING_SCR
            SCREENS[2] = FIGHTING_SCR
            DEFAULT_PLAYERS = [[Players[0], -1, 0], [Players[1], -1, 1]]
            SCREENS[3] = 0
        pg.display.flip()
        clock.tick(GSs['MaxFPS'])
    ScreenChanger(SCREENS)
def CS_Helper(Player, cmd, list=CharMatrix):
    RESOURCES['Sounds']['Select'].play()
    Done = False
    EnPlayer = 1
    if Player == 1:
        EnPlayer = 2
    jc = 1
    for i in range(len(list)):
        for j in range(len(list[i])):
            if list[i][j] == Player:
                if (cmd == 'Up') and (i > 0):
                    if list[i - jc][j] == EnPlayer:
                        jc = 2
                    if (i - jc) < 0:
                        jc = 0
                    list[i - jc][j], list[i][j] = list[i][j], list[i - jc][j]
                elif (cmd == 'Down') and (i < len(list) - 1):
                    if list[i + jc][j] == EnPlayer:
                        jc = 2
                    if (i + jc) > len(list) - 1:
                        jc = 0
                    list[i + jc][j], list[i][j] = list[i][j], list[i + jc][j]
                elif (cmd == 'Left') and (j > 0):
                    if list[i][j - jc] == EnPlayer:
                        jc = 2
                    if (j - jc) < 0:
                        jc = 0
                    list[i][j - jc], list[i][j] = list[i][j], list[i][j - jc]
                elif (cmd == 'Right') and (j < len(list[i]) - 1):
                    if list[i][j + jc] == EnPlayer:
                        jc = 2
                    if (j + jc) > len(list[i]) - 1:
                        jc = 0
                    list[i][j + jc], list[i][j] = list[i][j], list[i][j + jc]
                Done = True
                break
        if Done:
            break
# GameOver([0,0],[1,1],[1,2,1])
#FightProcess([0,-1,0],[1,-1,1],3,20)
# Settings()
SS()

pg.quit()