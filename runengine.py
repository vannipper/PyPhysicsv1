import os
import pygame
import time
from datetime import datetime

def anchorTransform(screen, anchororig, res, zoom): # convert screen coordinates to anchor coordinates (constant runtime)
    anchor = int(((screen - res/2) / zoom) + anchororig)
    return (anchor)

def invAnchorTransform(anchor, anchororig, res, zoom): # convert anchor coordinates to screen choordinates (constant runtime)
    screen = int(zoom*(anchor - anchororig) + (res / 2))
    return (screen)

def bodyIntersects(obj1x, obj1y, obj2x, obj2y, d1, d2): # returns true if the mouse cursor is intersecting with the body (constant runtime)
    if ((obj1x + (d1 / 2) >= obj1y - (d2 / 2) and obj1x - (d1 / 2) <= obj2x + (d2 / 2)) and (obj1y + (d1 / 2) >= obj2y - (d2 / 2) and obj1y - (d1 / 2) <= obj2y + (d2 / 2))):
        return (True)

def round(num, rf): # round (constant runtime)
    modnum = num % rf
    if modnum >= rf / 2:
        return (num + (rf - modnum))
    else:
        return (num - modnum)
    
def find_nth(s, char, n): # find nth occurance of a character in a string (linear runtime)
    count = 0
    for i, c in enumerate(s):
        if c == char:
            count += 1
            if count == n:
                return i
    return -1

def root(num, rootnum): # returns the root of a number (contant runtime)
    return(num**(1/rootnum))
    
def drawtext(text, locx, locy, color): # draws text on the screen (constant runtime)
    textRender = font.render(text, True, color) # display anchor location
    screen.blit(textRender, (locx, locy))

def gravAccel(p1, p2): # newtonian gravity (SI) (constant runtime)
    g = 6.67430e-11
    dist = distance(p1, p2)
    if p1 == p2:
        return (0, 0)
    else:
        accel = (g*p2.mass) / ((dist*1000)**2)
        return (accel * (p2.locx - p1.locx) / dist, accel * (p2.locy - p1.locy) / dist)

def distance(p1, p2): # calculates euclidian distance between two bodies (constant runtime)
    return (root((p1.locx - p2.locx)**2 + (p1.locy - p2.locy)**2, 2))

class Planet():
    
    def __init__(self, name, mass, diameter, startx, starty, velox, veloy, color):
        self.name = name
        self.mass = mass
        self.diameter = diameter
        self.locx = startx
        self.locy = starty
        self.velox = velox
        self.veloy = veloy
        self.color = color

# SCREENINFO / MONITORS INITIALIZATION
from screeninfo import get_monitors
monitors = get_monitors()

# DISPLAY INITIALIZATION
resx = monitors[0].width - 100
resy = monitors[0].height - 100
anchorx = 0
anchory = 0
bounds = (2000000000, 2000000000) # user cannot exit these bounds

# PYGAME INITIALIZATION
pygame.init()
screen = pygame.display.set_mode((resx, resy))
pygame.display.set_caption('PyPhysics')
FPS = 60
counter = 0
background = pygame.image.load('bgimg.jpg')
scaledimage = pygame.transform.scale(background,(resx*1.5, resy*1.5))

# COLOR / FONT INITIALIZATION
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DKGRAY = (120, 120, 120)
font = pygame.font.SysFont('Arial', 30)

# SIMULATION VARIABLES
dragging = False
startx, starty = None, None
mousex, mousey = None, None

current_datetime = datetime.now() # set up time for display
current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
year = int(current_datetime[0:current_datetime.find('-')])
month = int(current_datetime[current_datetime.find('-') + 1:find_nth(current_datetime, '-', 2)])
day = int(current_datetime[find_nth(current_datetime, '-', 2) + 1:current_datetime.find(' ')])
hour = int(current_datetime[current_datetime.find(' ') + 1:current_datetime.find(':')])
minute = int(current_datetime[current_datetime.find(':') + 1:find_nth(current_datetime, ':', 2)])
second = int(current_datetime[find_nth(current_datetime, ':', 2) + 1:])

scrollval = 3
zooms = [(pow(root(10, scrollval), i)*0.0000001) for i in range(scrollval*7)]
zoom = zooms[9]
tf = 1
times = [0, 1, 60, 3600, 86400, 2592000]

# IMPORT PLANETS
planets, images, paths = [], [], []
follow = "None"
with open("planetdata.dat") as file:
    planetfile = file.readlines()
    for line in planetfile:
        planetdata = line.split(',')
        planets.append(Planet(planetdata[0], (float(planetdata[1])*pow(10, int(planetdata[2]))), int(planetdata[3]), float(planetdata[4]), float(planetdata[5]), float(planetdata[6]), float(planetdata[7]), tuple(map(int, planetdata[8].split()))))
        paths.append(list((int(planetdata[4]), int(planetdata[5])) for _ in range (12))) # set up paths

# GAME LOOP
running = True
while running: # runtime will be measured in units per tick/frame

    start_time = time.time() # measure how long it takes to run all calculations (1)

    # EVENT DETECTION (input)
    for event in pygame.event.get():

        if event.type == pygame.QUIT: # quit detection (+e)
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN: # detect dragging (+8en + 2e)
            if event.button == 1: # left click
                follow = "None"
                startx, starty = event.pos
                gamestartx, gamestarty = anchorTransform(startx, anchorx, resx, zoom), anchorTransform(starty, anchory, resy, zoom) # +2

                for planet in planets: # +4n
                    if bodyIntersects(gamestartx, gamestarty, planet.locx, planet.locy, 0, planet.diameter) or bodyIntersects(startx, starty, invAnchorTransform(planet.locx, anchorx, resx, zoom), invAnchorTransform(planet.locy, anchory, resy, zoom), 8, 8): # +4
                        follow = planet.name

                dragging = True

            if event.button == 4 and zoom != zooms[-1]: # scroll up (zoom in) 
                zoom = zooms[zooms.index(zoom) + 1] # +len(zooms)

            if event.button == 5 and zoom != zooms[0]: # scroll down (zoom out)
                zoom = zooms[zooms.index(zoom) - 1] # +len(zooms)

        if event.type == pygame.MOUSEMOTION: # while dragging (+e)
            x, y = event.pos
            mousex = anchorTransform(x, anchorx, resx, zoom) # +1
            mousey = anchorTransform(y, anchory, resy, zoom) # +1
            
            if dragging: # +1
                endx, endy = event.pos
                anchorx -= int(1.5*(endx - startx) / zoom)
                anchory -= int(1.5*(endy - starty) / zoom)
                startx = endx
                starty = endy

        if event.type == pygame.MOUSEBUTTONUP: # after dragging
            if event.button == 1 and dragging:
                dragging = False

                if anchorx > bounds[0]: # snap camera back if out of bounds
                    anchorx = bounds[0]
                elif anchorx < -bounds[0]:
                    anchorx = -bounds[0]
                if anchory > bounds[1]:
                    anchory = bounds[1]
                elif anchory < -bounds[1]:
                    anchory = -bounds[1]

                startx, starty = None, None
            
        if event.type == pygame.KEYDOWN: # check for specific key presses
            if event.key == pygame.K_SPACE:  # reset anchor
                anchorx = 0
                anchory = 0

            if event.key == pygame.K_ESCAPE:  # Check if 'ESC' key is pressed
                running = False  # Exit the loop and quit the game

            if event.key == pygame.K_MINUS: # Check if '-' key is pressed
                if zoom != zooms[0]:
                    zoom = zooms[zooms.index(zoom) - 1]
            
            if event.key == pygame.K_EQUALS: # Check if '=' key is pressed
                if zoom != zooms[-1]:
                    zoom = zooms[zooms.index(zoom) + 1]

            if event.key == pygame.K_COMMA:
                if tf != times[0]:
                    tf = times[times.index(tf) - 1]
                    paths = [list((int(planetdata[4]), int(planetdata[5])) for _ in range (12)) for _ in range(len(planets))]
                              
            if event.key == pygame.K_PERIOD:
                if tf != times[-1]:
                    tf = times[times.index(tf) + 1]
                    paths = [list((int(planetdata[4]), int(planetdata[5])) for _ in range (12)) for _ in range(len(planets))]
   
    # TIME LOGIC (FIX THIS)
    counter += tf
    if counter >= FPS: # every 60 frames
        second += counter // FPS
        counter = 0
        for i in range(len(planets)): # every second, update paths list
            paths[i].pop(0)
            paths[i].append((planets[i].locx, planets[i].locy))

    if second >= 60: # push increments
        minute += (second // 60)
        second = int(second) % 60
    if minute >= 60:
        hour += (minute // 60)
        minute = int(minute) % 60
    if hour >= 24:
        day += (hour // 24)
        hour = int(hour) % 24
    if (day >= 29 and month == 2 and not year % 4 == 0): # february
        month += (day // 28)
        day = int(day) % 28
    elif (day >= 30 and month == 2 and year % 4 == 0): # leap year
        month += (day // 29)
        day = int(day) % 29
    elif day >= 32 and month in [1, 3, 5, 7, 8, 10, 12]: # long months
        month += (day // 31)
        day = int(day) % 31
    elif day >= 31 and month in [4, 6, 9, 11]: # short months
        month += (day // 30)
        day = int(day) % 30
    if month >= 13:
        year += (month // 12)
        month = int(month) % 12

    # USEFUL VARIABLES
    screenx = (anchorTransform(0, anchorx, resx, zoom), anchorTransform(resx, anchorx, resx, zoom)) # range of anchor coords of screen bounds
    screeny = (anchorTransform(0, anchory, resy, zoom), anchorTransform(resy, anchory, resy, zoom))
    leftboundscreen = invAnchorTransform(-bounds[0], anchorx, resx, zoom) # screen coordinates of xy bounds
    topboundscreen = invAnchorTransform(-bounds[1], anchory, resy, zoom)
    rightboundscreen = invAnchorTransform(bounds[0], anchorx, resx, zoom) # screen coordinates of xy bounds
    bottomboundscreen = invAnchorTransform(bounds[1], anchory, resy, zoom)

    # SCREEN / DISPLAY LOGIC
    screen.fill((0, 0, 0))  # Clear screen
    screen.blit(scaledimage, (0 - resx//4,0 - resy//4))

    # GRID
    if zoom >= 0.1:
        gridstep = 1000
        gridsizetext = font.render("= 1000 km by 1000 km", True, GRAY) # display anchor location
    elif zoom >= 0.001:
        gridstep = 100000
        gridsizetext = font.render("= 100 Thousand km by 100 Thousand km", True, GRAY) # display anchor location
    elif zoom >= 0.00001:
        gridstep = 10000000
        gridsizetext = font.render("= 10 Million km by 10 Million km", True, GRAY) # display anchor location
    else:
        gridstep = 1000000000
        gridsizetext = font.render("= 1 Billion km by 1 Billion km", True, GRAY) # display anchor location
    for pixel in range(screenx[0] - gridstep, screenx[1] + gridstep, gridstep):
        newp = round(pixel, gridstep)
        if -bounds[0] <= newp and newp <= bounds[0]:
            pygame.draw.rect(screen, GRAY, pygame.Rect(invAnchorTransform(newp, anchorx, resx, zoom), topboundscreen, 1, (bottomboundscreen-topboundscreen)))
    for pixel in range(screeny[0] - gridstep, screeny[1] + gridstep, gridstep):
       newp = round(pixel, gridstep)
       if -bounds[1] <= newp and newp <= bounds[1]:
            pygame.draw.rect(screen, GRAY, pygame.Rect(leftboundscreen, invAnchorTransform(newp, anchory, resy, zoom), (rightboundscreen - leftboundscreen), 1))

    # BOUNDING BOX
    if bounds[0] in range(screenx[0], screenx[1]) or bounds[1] in range(screeny[0], screeny[1]) or -bounds[0] in range(screenx[0], screenx[1]) or -bounds[1] in range(screeny[0], screeny[1]):
        pygame.draw.rect(screen, WHITE, pygame.Rect(leftboundscreen, topboundscreen, bounds[0]*zoom*2, bounds[1]*zoom*2), 5)

    # PLANET LOGIC
    for i, p1 in enumerate(planets):
        for p2 in planets: # determine forces, velocities, positions
            tempaccelx, tempaccely = gravAccel(p1, p2) # in SI
            p1.velox += (tempaccelx*tf)/(FPS*1000) # convert to km/s^2
            p1.veloy += (tempaccely*tf)/(FPS*1000)
        p1.locx += (p1.velox*tf)/(FPS)
        p1.locy += (p1.veloy*tf)/(FPS)
        if p1.name == follow: # update cursor position for following
            anchorx, anchory = p1.locx, p1.locy
        if abs(p1.locx) > bounds[0] or abs(p1.locy) > bounds[1]: # if planet leaves bounding box, remove it
            planets.pop(i)
            paths.pop(i)
        planetscreenx, planetscreeny = invAnchorTransform(p1.locx, anchorx, resx, zoom), invAnchorTransform(p1.locy, anchory, resy, zoom) # determine positions, draw on screen
        # for i in range(len(paths)): # +12n
        #     for j in range(12):
        #         pygame.draw.circle(screen, WHITE, (invAnchorTransform(paths[i][j][0], anchorx, resx, zoom), invAnchorTransform(paths[i][j][1], anchory, resy, zoom)), 2)
        # pygame.draw.circle(screen, p1.color, (planetscreenx, planetscreeny), (p1.diameter // 2) * zoom)
        pygame.draw.circle(screen, p1.color, (planetscreenx, planetscreeny), 3)
        drawtext(p1.name, planetscreenx, planetscreeny, p1.color)
    
    # PERMANENT OBJECTS (text, interactable features)
    drawtext("Cursor X: " + str(int(anchorx)) + " Y: " + str(int(anchory)), 25, (resy - 200), GRAY)
    drawtext("Focused on: " + str(follow), 25, resy - 150, GRAY)
    pygame.draw.rect(screen, GRAY, pygame.Rect(25, resy - 100, 75, 75), 1)
    screen.blit(gridsizetext, (125, resy - 75))
    pygame.draw.circle(screen, WHITE, (resx/2, resy/2), 2) # crosshair
    
    # TIME LOGIC
    drawtext("Time: ", resx - 385, resy - 100, GRAY)
    drawtext(str(int(year)) + '-' + str(int(month)) + '-' + str(int(day)) + ' ' + str(int(hour)) + ':' + str(int(minute)) + ':' + str(int(second)), resx - 300, resy - 100, WHITE)
    if tf == times[0]: # print tf
        drawtext("(0s / s)", resx - 125, resy - 60, GRAY)        
    elif tf == times[1]:
        drawtext("(1s / s)", resx - 125, resy - 60, GRAY)
    elif tf == times[2]:
        drawtext("(1m / s)", resx - 125, resy - 60, GRAY)
    elif tf == times[3]:
        drawtext("(1h / s)", resx - 125, resy - 60, GRAY)
    elif tf == times[4]:
        drawtext("(1d / s)", resx - 125, resy - 60, GRAY)
    elif tf == times[5]:
        drawtext("(30d / s)", resx - 125, resy - 60, GRAY)
    elif tf == times[6]:
        drawtext("(1y / s)", resx - 125, resy - 60, GRAY)
    else:
        drawtext("(10y / s)", resx - 125, resy - 60, GRAY)

    # SLIDER LOGIC
    pygame.draw.rect(screen, WHITE, pygame.Rect(resx - 350, resy - 50, 200, 20)) 
    for displacement in range(10, 200, 200 // len(times)):
        pygame.draw.rect(screen, BLACK, pygame.Rect(resx - 350 + displacement, resy - 50, 5, 20))
    pygame.draw.rect(screen, BLUE, pygame.Rect(resx - 345 + int(200 * times.index(tf) / len(times)), resy - 60, 20, 40))

    # GAME TICK UPDATE
    savetime = time.time() - start_time
    time.sleep(max(1/FPS - time.time() + start_time - 0.0017, 0))
    pygame.display.flip() # Update display

# lines = []
# with open('savetime.txt', 'r') as f:
#     lines = f.readlines()
# lines.append(f'{savetime}, {len(planets)}\n')# 

# with open('savetime.txt', 'w') as f:
#     for line in lines:
#         f.write(line)
os.system('clear')
pygame.quit()