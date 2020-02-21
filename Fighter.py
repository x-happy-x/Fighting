import pygame as pg
import os, time, sys

class Fighter:
    NOACTION_STATE, LMOVE_STATE, RMOVE_STATE, LRUN_STATE, RRUN_STATE = range(5)
    JUMPING_STATE, FALLING_STATE, FLYING_STATE, REBOUND_STATE        = range(5,9)
    LIVING_STATE, ATTACKED_STATE, DEFENDED_STATE, DEAD_STATE         = range(9,13)
    def __init__(self, DataPack):
        self.STATE_MOVE = self.NOACTION_STATE
        self.STATE_LIVE = self.LIVING_STATE
        self.STATE_JUMP = self.NOACTION_STATE
        self.STATE_HS   = self.NOACTION_STATE
        self.STATE_FS   = self.NOACTION_STATE
        self.PROPERTY = DataPack
        self.PROPERTY['HealfPercent'] = self.PROPERTY['Healf']/100
        self.PROPERTY['EnergyPercent'] = self.PROPERTY['Energy']/100
        self.PROPERTY['Gravity'] = self.PROPERTY['Weight']
        self.PROPERTY['SPEED'] =  self.PROPERTY['Speed']
        self.direction = 0
        ############## = [ NA,   MV,   JP,   AT,    BL]
        self.AnimState = [  1,    1,    0,    0,     0]
        self.AnimSpeed = [0.5,  0.5,  0.5,  0.7,  0.5]
        self.LAYERUP, self.LAYERDOWN = [],[]
        self.PROPERTY['Anim'] = {}
        self.PROPERTY['Sound'] = {}
        self.PROPERTY['Sound']['Jump'] = pg.mixer.Sound('Sounds/Jump.wav')
        self.PROPERTY['Sound']['Punch'] = pg.mixer.Sound('Sounds/Punch.wav')
        self.PROPERTY['Sound']['FireBig'] = pg.mixer.Sound('Sounds/FireBig.wav')
        Actions = os.listdir(os.path.join('Characters',self.PROPERTY['Name']))
        tricks = __import__('Characters.'+self.PROPERTY['Name']+'.iData.'+'tricks',fromlist=['Characters.'+self.PROPERTY['Name']+'.iData'])
        Actions.remove('Prev.png')
        Actions.remove('iData')
        for action in Actions:
            for num in os.listdir(os.path.join('Characters',self.PROPERTY['Name'],action)):
                self.PROPERTY['Anim'][action+num.split('.')[0]] = pg.image.load(os.path.join('Characters',self.PROPERTY['Name'],action,num)).convert_alpha()
            self.PROPERTY['Anim'][action+'.len'] = len(os.listdir(os.path.join('Characters',self.PROPERTY['Name'],action)))-1
        self.PROPERTY['Image'] = self.PROPERTY['Anim']['NoAction0']
        if self.PROPERTY['ControlID']==0:
            self.PROPERTY['BodyRect'] = self.PROPERTY['Anim']['NoAction0'].get_rect(bottomleft=(self.PROPERTY['CoordsX'],self.PROPERTY['CoordsY']))
        else:
            self.PROPERTY['BodyRect'] = self.PROPERTY['Anim']['NoAction0'].get_rect(bottomright=(self.PROPERTY['CoordsX'],self.PROPERTY['CoordsY']))
        self.PROPERTY['BodyRect'][2]-=40
        self.ATTACK = tricks.Attacking(self)

    def AddParam(self,DataPack):
        self.NEW_PROPERTY = DataPack

    #Jump
    def jump(self):
        if self.STATE_JUMP==self.JUMPING_STATE:
            self.PROPERTY['BodyRect'].bottom -= self.PROPERTY['Gravity']
            self.PROPERTY['Gravity'] -= 1 if self.PROPERTY['Gravity']>=3 else 0
            if self.PROPERTY['BodyRect'].bottom <= self.PROPERTY['CoordsX']-self.PROPERTY['Weight']*5:
                self.STATE_JUMP = self.FALLING_STATE
            elif self.PROPERTY['BodyRect'].colliderect(self.Enemy.PROPERTY['BodyRect']) and (self.Enemy.STATE_LIVE != self.Enemy.DEAD_STATE):
                self.PROPERTY['BodyRect'].bottom += self.PROPERTY['Gravity']
                self.STATE_JUMP = self.FALLING_STATE

        if self.STATE_JUMP == self.FALLING_STATE:
            self.PROPERTY['BodyRect'].bottom += self.PROPERTY['Gravity']
            self.PROPERTY['Gravity'] +=1
            if self.PROPERTY['BodyRect'].colliderect(self.Enemy.PROPERTY['BodyRect']) and (self.Enemy.STATE_LIVE != self.Enemy.DEAD_STATE):
                self.PROPERTY['BodyRect'].bottom -= self.PROPERTY['Gravity']
                self.STATE_JUMP = self.NOACTION_STATE
                self.PROPERTY['Gravity'] = self.PROPERTY['Weight']
                self.AnimSpeed[2] = 0.5
                self.AnimState[2] = 0
            if self.PROPERTY['BodyRect'].bottom >= self.PROPERTY['CoordsY']:
                self.STATE_JUMP = self.NOACTION_STATE
                self.PROPERTY['Gravity'] = self.PROPERTY['Weight']
                self.AnimState[2] = 0

    def AttackRequest(self, Zone, Type=0):
        if Zone.colliderect(self.PROPERTY['BodyRect']) and (self.STATE_LIVE != self.DEAD_STATE):
            if Type==0 and self.STATE_LIVE == self.DEFENDED_STATE:
                return False
            else:
                self.PROPERTY['BodyRect'].centerx+= self.PROPERTY['SPEED']*2 *(1 if self.direction==1 else -1) * (0 if (150>=self.PROPERTY['BodyRect'].centerx) or (self.PROPERTY['BodyRect'].centerx>=self.PROPERTY['WxH'][0]-150) else 1)
                self.STATE_LIVE = self.ATTACKED_STATE
                self.AttackedTime = pg.time.get_ticks()
                return True
        else:
            return False
    #Moving
    def move(self):
        self.PROPERTY['BodyRect'].centerx+=self.PROPERTY['Speed']
        if self.PROPERTY['Speed']!=0:
            self.STATE_MOVE = self.RMOVE_STATE
        else:
            self.STATE_MOVE = self.NOACTION_STATE
            self.AnimState[1] = 1
            self.AnimSpeed[1] = 0.5
        if self.PROPERTY['BodyRect'].colliderect(self.Enemy.PROPERTY['BodyRect']) and (self.Enemy.STATE_LIVE != self.Enemy.DEAD_STATE):
            self.PROPERTY['BodyRect'].centerx-=self.PROPERTY['Speed']
        if (100>=self.PROPERTY['BodyRect'].centerx) or (self.PROPERTY['BodyRect'].centerx>=self.PROPERTY['WxH'][0]-100):
            self.PROPERTY['BodyRect'].centerx-=self.PROPERTY['Speed']
        self.PROPERTY['Speed'] = 0

    #Punch
    def attack(self, Actions):
        self.KEYS = Actions
        if self.STATE_HS != self.NOACTION_STATE:
            self.ATTACK.Punch()
        elif self.STATE_FS != self.NOACTION_STATE:
            if self.PROPERTY['PersonID']==0:
                if self.PROPERTY['Energy']/self.PROPERTY['EnergyPercent']==101:
                    self.ATTACK.Capture()
                else:
                    self.ATTACK.Rasengun()
            elif self.PROPERTY['PersonID']==1:
                if self.PROPERTY['Energy']/self.PROPERTY['EnergyPercent']==101:
                    self.ATTACK.Capture()
                else:
                    self.ATTACK.FireJutsu()

    #Rotate
    def flip(self):
        for image in self.PROPERTY['Anim']:
            if not image.endswith('len'):
                self.PROPERTY['Anim'][image] = pg.transform.flip(self.PROPERTY['Anim'][image], 1, 0)
        self.direction = abs(self.direction-1)

    #Control
    def control(self,Actions):
        if self.STATE_LIVE != self.ATTACKED_STATE:
            for Action in Actions:
                if Action == 'Block' and (self.STATE_HS == self.NOACTION_STATE == self.STATE_FS):
                    self.STATE_LIVE = self.DEFENDED_STATE
                elif Action == 'Punch' and (self.STATE_HS == self.NOACTION_STATE == self.STATE_FS):
                    self.STATE_HS = 1
                elif Action == 'Kick' and (self.STATE_HS == self.NOACTION_STATE == self.STATE_FS):
                    self.STATE_FS = 1
                if (self.NOACTION_STATE == self.STATE_FS):
                    if Action == 'Left':
                        self.PROPERTY['Speed'] = -self.PROPERTY['SPEED'] - (0 if self.STATE_JUMP==self.NOACTION_STATE else 4)
                    elif Action == 'Right':
                        self.PROPERTY['Speed'] = self.PROPERTY['SPEED'] + (0 if self.STATE_JUMP==self.NOACTION_STATE else 4)
                    if Action == 'Up' and self.STATE_JUMP==self.NOACTION_STATE:
                        self.STATE_JUMP = self.JUMPING_STATE
                        self.PROPERTY['CoordsX'] = self.PROPERTY['BodyRect'].bottom
                        self.PROPERTY['Sound']['Jump'].play()
                    elif Action == 'Down' and self.STATE_JUMP < self.FALLING_STATE:
                        pass
                    if Action == 'Recovery':
                        if self.PROPERTY['Energy']<self.PROPERTY['EnergyPercent']*100:
                            self.PROPERTY['Energy']+=0.3
                    else:
                        self.PROPERTY['Energy']=int(self.PROPERTY['Energy'])
        else:
            if 'Block' in Actions:
                self.STATE_LIVE = self.DEFENDED_STATE

    #Draw person
    def draw(self,Enemy,Actions=[]):
        self.LAYERDOWN, self.LAYERUP = [], []
        self.Enemy = Enemy
        if self.PROPERTY['Healf']>0:
            if Actions!=[]:
                if (self.STATE_LIVE == self.DEFENDED_STATE) and ('Block' not in Actions):
                    self.STATE_LIVE = self.LIVING_STATE
                    self.AnimState[4] = 0
                self.control(Actions)
            elif Actions==[] and self.STATE_LIVE == self.DEFENDED_STATE:
                self.STATE_LIVE = self.LIVING_STATE
                self.AnimState[4] = 0
            if self.STATE_LIVE == self.ATTACKED_STATE:
                if pg.time.get_ticks() - self.AttackedTime >= 250:
                    self.STATE_LIVE = self.LIVING_STATE
            self.jump()
            self.move()
            self.attack(Actions)
            if self.STATE_LIVE == self.DEFENDED_STATE:
                self.PROPERTY['Image'] = self.PROPERTY['Anim']['Block'+str(int(self.AnimState[4]))]
                if self.PROPERTY['Anim']['Block.len']!=int(self.AnimState[4]):
                    self.AnimState[4]+=self.AnimSpeed[4]
            elif self.STATE_MOVE == self.NOACTION_STATE == self.STATE_JUMP == self.STATE_FS == self.STATE_HS:
                if int(self.AnimState[0]) == self.PROPERTY['Anim']['NoAction.len'] or int(self.AnimState[0])==0:
                    self.AnimSpeed[0] = -self.AnimSpeed[0]
                self.PROPERTY['Image'] = self.PROPERTY['Anim']['NoAction'+str(int(self.AnimState[0]))]
                self.AnimState[0]+=self.AnimSpeed[0]
            elif self.STATE_HS != self.NOACTION_STATE:
                self.PROPERTY['Image'] = self.PROPERTY['Anim']['Punch'+str(int(self.STATE_HS))]
            elif self.STATE_FS != self.NOACTION_STATE:
                self.PROPERTY['Image'] = self.PROPERTY['Anim']['Kick'+str(int(self.STATE_FS))]
            elif self.STATE_JUMP == self.JUMPING_STATE:
                if int(self.AnimState[2])==self.PROPERTY['Anim']['Jump.len']:
                    self.AnimState[2]-=self.AnimSpeed[2]
                self.PROPERTY['Image'] = self.PROPERTY['Anim']['Jump'+str(int(self.AnimState[2]))]
                self.AnimState[2]+=self.AnimSpeed[2]
            elif  self.STATE_JUMP== self.FALLING_STATE:
                if int(self.AnimState[2])==0:
                    self.AnimState[2]+=self.AnimSpeed[2]
                self.PROPERTY['Image'] = self.PROPERTY['Anim']['Jump'+str(int(self.AnimState[2]))]
                self.AnimState[2]-=self.AnimSpeed[2]
            elif self.STATE_MOVE != self.NOACTION_STATE:
                if int(self.AnimState[1])==self.PROPERTY['Anim']['Move.len'] or int(self.AnimState[1])==0:
                    self.AnimSpeed[1] = -self.AnimSpeed[1]
                self.PROPERTY['Image'] = self.PROPERTY['Anim']['Move'+str(int(self.AnimState[1]))]
                self.AnimState[1]+=self.AnimSpeed[1]
            self.LAYERDOWN.append([self.PROPERTY['Image'],self.PROPERTY['BodyRect']])
        else:
            self.PROPERTY['Image'] = self.PROPERTY['Anim']['Dead0']
            self.STATE_LIVE = self.DEAD_STATE
            self.LAYERDOWN.append([self.PROPERTY['Image'],self.PROPERTY['BodyRect']])