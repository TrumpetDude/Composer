import pygame, sys
from pygame.locals import *

def drawText(window, text, size, color, centerX, centerY):
    font=pygame.font.Font("PressStart2P.ttf", size)
    renderedText=font.render(text,True,color)
    textpos=renderedText.get_rect()
    textpos.centerx=centerX
    textpos.centery=centerY
    window.blit(renderedText, textpos)

tempo = 120

pygame.init()
window = pygame.display.set_mode((1300,700))

rect = (tempo*2.5, 0, 100, 50)

while True:
    window.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            programQuit = True
            pygame.quit()
            sys.exit(0)

    mousePos=pygame.mouse.get_pos()
    mousePressed=pygame.mouse.get_pressed()

    pygame.draw.rect(window, (50,50,50), (88,10, 1022,30), 0)
    pygame.draw.rect(window, (255,255,255), rect, 0)
    drawText(window, str(tempo), 20, (0,0,0), rect[0]+rect[2]/2, rect[1]+rect[3]/2)
    drawText(window, "Tempo", 20, (255,255,255), 1205,25)


    if mousePos[0]>rect[0] and mousePos[0]<rect[0]+rect[2] and mousePos[1]>rect[1] and mousePos[1]<rect[1]+rect[3]:
        pygame.draw.rect(window, (200,200,200), rect,0)
        drawText(window, str(tempo),20,(0,0,0),rect[0]+rect[2]/2, rect[1]+rect[3]/2)
        offset = mousePos[0]-rect[0]
        while ((mousePressed[0] or mousePressed[1] or mousePressed[2])):
            mousePressed=pygame.mouse.get_pressed()
            pygame.draw.rect(window, (0,0,0), rect,0)
            draggingMousePos = pygame.mouse.get_pos()
            if draggingMousePos[0]-offset>=98 and draggingMousePos[0]-offset<=1000:
                rect = [draggingMousePos[0]-offset, rect[1], rect[2], rect[3]]
            tempo = round(rect[0]/2.5)
            pygame.draw.rect(window, (50,50,50), (88,10, 1022,30), 0)
            pygame.draw.rect(window, (100,100,100), rect,0)
            drawText(window, str(tempo),20,(255,255,255),rect[0]+rect[2]/2, rect[1]+rect[3]/2)
            drawText(window, "Tempo", 20, (255,255,255), 1205,25)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    programQuit = True
                    pygame.quit()
                    sys.exit(0)

    pygame.display.update()
