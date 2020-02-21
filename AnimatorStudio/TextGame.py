import time
import random as r
from msvcrt import getch
w,h = 150,36
screen = []
players = [["     O     ", #Обычное состояние 0
            "    /|\    ",
            "   / | \   ",
            "  & _|_ &  ",
            "    | |    ",
            "   _| |_   "],
           ["     O     ", #Удар рукой R 1
            "    /|----o",
            "   / |     ",
            "  & _|_    ",
            "    | |    ",
            "   _| |_   "],
           ["     O     ", #Удар рукой L 2
            "o----|\    ",
            "     | \   ",
            "    _|_ &  ",
            "    | |    ",
            "   _| |_   "],
           ["     O     ", #Удар ногой R 3
            "    /|\    ",
            "   / | \   ",
            "  & _|__&_|",
            "    |      ",
            "   _|      "],
           ["     O     ", #Удар ногой L 4
            "    /|\    ",
            "   / | \   ",
            "|_&__|_ &  ",
            "      |    ",
            "      |_   "],
           ["           ", #Присев 5
            "           ",
            "    _O_    ",
            "   / | \   ",
            "  & _|_ &  ",
            "   _\ /_   "]
           ]
player = players[0]
def inList(texture):
    for i in range(len(texture)):
        texture[i] = list(texture[i])
    return texture
def new_screen():
    global screen
    screen = []
    for i in range(h):
        if i==0 or i==h-1:
            screen.append(['#']*w)
        else:
            screen.append(["#"]+[" "]*148+["#"])
def setInScreen(x,y,texture):
    for i in range(len(texture)):
        for j in range(len(texture[i])):
            screen[y+i][x+j]=texture[i][j]
def render():
    global screen
    for iline in screen:
        for jline in iline:
            print(jline, end='')
        print()
while True:
    time.sleep(1/60)
    new_screen()
    setInScreen(r.randint(1,w-15),h-7,player)
    print()
    render()