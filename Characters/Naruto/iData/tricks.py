import pygame as pg

class Attacking:
    def __init__(self,My):
        self.at = pg.Rect(0,0,1,1)
        self.MY = My
        self.FireImg = pg.image.load('Backgrounds/Effects/Fire.png').convert_alpha()
        self.Rasen = pg.image.load('Backgrounds/Effects/Rasengun.png').convert_alpha()
        self.Flash = pg.image.load('Backgrounds/Effects/Flash.png').convert_alpha()
        if self.MY.direction == 1:
            self.FireImg = pg.transform.flip(self.FireImg,1,0)
            self.Rasen = pg.transform.flip(self.Rasen,1,0)
            self.Flash = pg.transform.flip(self.Flash,1,0)
        self.JutsuAct = 0
        self.JutsuEnd = 0
        self.JutsuEnergy = 0

    def Punch(self):
        if self.MY.PROPERTY['Anim']['Punch.len']>self.MY.STATE_HS>=1:
            self.MY.STATE_HS += self.MY.AnimSpeed[3]
            if (int(self.MY.STATE_HS) == 1) and (self.MY.AnimSpeed[3]<0):
                self.MY.AnimSpeed[3]= -self.MY.AnimSpeed[3]
                self.MY.STATE_HS = self.MY.NOACTION_STATE
        elif int(self.MY.STATE_HS) == self.MY.PROPERTY['Anim']['Punch.len']:
            self.at = self.MY.PROPERTY['Anim']['Punch5'].get_rect(bottomleft=self.MY.PROPERTY['BodyRect'].bottomleft)
            if self.MY.direction == 1:
                self.at = self.MY.PROPERTY['Anim']['Punch5'].get_rect(bottomright=self.MY.PROPERTY['BodyRect'].bottomright)
            self.at.height=self.at.height//10
            self.at.width-=self.at.height
            self.at.centery+=self.at.height*5
            if self.MY.Enemy.AttackRequest(self.at, 0):
                if (self.MY.Enemy.PROPERTY['Healf']-self.MY.PROPERTY['Force']>=0):
                    self.MY.Enemy.PROPERTY['Healf']-=self.MY.PROPERTY['Force']
                    self.MY.PROPERTY['Sound']['Punch'].play()
                    if self.MY.PROPERTY['Energy']<self.MY.PROPERTY['EnergyPercent']*100:
                        self.MY.PROPERTY['Energy']+=2
                        if self.MY.Enemy.PROPERTY['Energy'] < self.MY.Enemy.PROPERTY['EnergyPercent'] * 100:
                            self.MY.Enemy.PROPERTY['Energy']+=1
                else:
                    self.MY.Enemy.PROPERTY['Healf']=0
            self.MY.AnimSpeed[3] =- self.MY.AnimSpeed[3]
            self.MY.STATE_HS += self.MY.AnimSpeed[3]

    def Rasengun(self):
        if self.MY.PROPERTY['Anim']['Kick.len']>self.MY.STATE_FS>=1:
            if self.JutsuAct==0:
                self.MY.PROPERTY['Sound']['FireBig'].play()
                self.JutsuAct=1
            self.MY.STATE_FS += self.MY.AnimSpeed[3]
            if (int(self.MY.STATE_FS) == 1) and (self.MY.AnimSpeed[3]<0):
                self.MY.AnimSpeed[3]= -self.MY.AnimSpeed[3]
                self.MY.STATE_FS = self.MY.NOACTION_STATE
                self.JutsuAct = 0
                self.JutsuEnd = 0
                self.JutsuEnergy = 0
        elif int(self.MY.STATE_FS) == self.MY.PROPERTY['Anim']['Kick.len']:
            if self.JutsuEnd==0:
                self.at = self.MY.PROPERTY['Anim']['Punch5'].get_rect(bottomleft=self.MY.PROPERTY['BodyRect'].bottomleft)
                if self.MY.direction == 1:
                    self.at = self.MY.PROPERTY['Anim']['Punch5'].get_rect(
                        bottomright=self.MY.PROPERTY['BodyRect'].bottomright)
                    self.at.centerx-=self.at.width//2-self.at.width//2.5
                self.at.centerx+=self.at.width//2.5
                self.at.height/=3
                self.at.width/=2
                self.at.centery+=self.at.height*1.5
                self.JutsuEnd = 1
            if self.JutsuEnd == 2:
                if self.MY.direction == 0:
                    self.at.centerx+=50
                else:
                    self.at.centerx-=50
            self.MY.LAYERUP.append([self.Rasen,self.at])
            if self.MY.Enemy.AttackRequest(self.at, 0):
                if self.MY.direction == 0:
                    self.at.centerx -= 50
                else:
                    self.at.centerx += 50
                if (self.MY.Enemy.PROPERTY['Healf']-self.MY.PROPERTY['Force']//20*self.JutsuEnergy>=0):
                    self.MY.Enemy.PROPERTY['Healf']-=self.MY.PROPERTY['Force']//20*self.JutsuEnergy
                else:
                    self.MY.Enemy.PROPERTY['Healf']=0
                self.MY.AnimSpeed[3] =- self.MY.AnimSpeed[3]
                self.MY.STATE_FS += self.MY.AnimSpeed[3]
            elif 0<self.at.centerx>self.MY.PROPERTY['WxH'][0]:
                self.MY.AnimSpeed[3] =- self.MY.AnimSpeed[3]
                self.MY.STATE_FS += self.MY.AnimSpeed[3]
            if 'Kick' in self.MY.KEYS:
                self.JutsuEnergy += 1 if self.MY.PROPERTY['Energy']>0 else 0
                self.MY.PROPERTY['Energy']-=1 if self.MY.PROPERTY['Energy']>0 else 0
            else:
                self.MY.PROPERTY['Sound']['FireBig'].stop()
                self.JutsuEnd = 2