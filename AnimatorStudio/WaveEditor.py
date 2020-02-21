import wave
import numpy as np
import pygame as pg
pg.init()
screen_size = [1000,800]
screen = pg.display.set_mode(screen_size)
wav = wave.open("/home/anjaro/Android/Projects/AnimaWar/android/assets/Sounds/FireBig.wav", mode="r")
nchannels,sampwidth,framerate,nframes,comptype,compname = wav.getparams()
content = wav.readframes(nframes)
types = {
    1: np.int8,
    2: np.int16,
    3: np.int32
}
samples = np.fromstring(content, dtype=types[sampwidth])
#samples = samples[np.where(samples!=0)]
print(len(samples))
isRun = True
while isRun:
    ss = []
    for e in pg.event.get():
        if e.type == pg.QUIT:
            isRun = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                isRun = False
    screen.fill((250,250,250))
    nn = samples.max()
    mm = samples.min()
    if abs(mm)>abs(nn):
        nn = abs(mm)
    nn=(screen_size[1])/nn
    j = 0
    for i in range(len(samples)):
        j+=screen_size[0]/len(samples)
        ss.append([int(j),int(screen_size[1]//2 + i//nn)])
    pg.draw.lines(screen,(30,30,30),0,ss)
    pg.display.flip()
    isRun = False
while True:
    pass