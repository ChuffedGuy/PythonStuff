import pygame
import math
from sys import exit


def circularPath(centerX, centerY, width, height, phaseShift, speed):
    t = pygame.time.get_ticks()/1000
    x = centerX + width * math.sin(speed * t + phaseShift)
    y = centerY + height * math.cos(speed * t + phaseShift)
    
    return x,y


def drawCube(centerX, centerY, width, height, angle, speed, color, dots):
    pointsUpper = []
    for num in range(4):
        pointsUpper.append(circularPath(centerX, centerY - height/2, width, angle, num * math.pi/2, speed))

    pointsLower= []
    for num in range(4):
        pointsLower.append(circularPath(centerX, centerY + height/2, width, angle, num * math.pi/2, speed))

    pygame.draw.lines(screen, color, 1, pointsUpper, 2)
    pygame.draw.lines(screen, color, 1, pointsLower, 2)

    for num in range(4):
        pygame.draw.line(screen, color, pointsUpper[num], pointsLower[num], 2)

    if dots:
        for x in pointsUpper:
            pygame.draw.circle(screen, color, x, 4)

        for x in pointsLower:
            pygame.draw.circle(screen, color, x, 4)


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Cube')
clock = pygame.time.Clock()
bg = pygame.Rect(0 , 0, 800, 400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.draw.rect(screen, 'white', bg)

    t = pygame.time.get_ticks()/1000
    sin = math.sin(2*t)

    drawCube(400, 200, 50, 60, 0 + 20 * sin, 2, 'red', 1)
    drawCube(200, 100 + 15 * sin, 50, 60, 25, 1.5, 'blue', 1)
    drawCube(580, 300, 30, 60, 20, 3, 'purple', 1)
    drawCube(160 + 40 * sin, 275, 50, 25, 40, 1.8, 'orange', 1)
    drawCube(600, 100, 75, 45 + 30 * sin, 13, 1.3, 'turquoise', 1)
    
    pygame.display.update()
    clock.tick(60)
