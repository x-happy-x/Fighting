import pygame as pg
import csv

pg.init()

white = (200, 200, 200)
FPS = 40

w = 225
h = 225
screen_size = (w, h)
screen = pg.display.set_mode(screen_size, pg.NOFRAME)
pg.display.set_caption('Keys')
f2 = pg.font.Font(None, 28)
def CS_Screen():
    global running
    running = True
    TapedKey = '---'
    while running:
        pg.mixer.music.stop()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == 27:
                    running = False
                for KEY in csv.DictReader(open('ControlKeys.data'), delimiter=','):
                    TapedKey = KEY[str(event.key)] + ' - ' + str(event.key)
        screen.fill(white)
        TK_text = f2.render(TapedKey,1,(0,0,0))
        screen.blit(TK_text,(w//2-TK_text.get_rect().width//2,h//2-TK_text.get_rect().height//2))
        pg.display.flip()
CS_Screen()
pg.quit()