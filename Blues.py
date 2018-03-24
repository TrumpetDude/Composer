tempo = 120
maxMelodyJump = 2

beatLength = 1/(tempo/60) #convert beats per minute to seconds per beat

#imports
import _thread as thread
from random import randint
import pyaudio
import numpy as np
from time import sleep
import pygame, sys
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((1300,700))
pygame.display.set_caption("Blues","Blues")

p = pyaudio.PyAudio()#initialize audio track
fs = 44100       # sampling rate, Hz, must be integer
volume = 0.5     # range [0.0, 1.0]

#set pitch values
def setPitchCenter(baseNote):
    global C3
    global D3
    global E3
    global F3
    global G3
    global A3
    global Bb3
    global B3
    global C4
    global D4
    global Eb4
    global E4
    global F4
    global G4
    global A4
    global B4
    global C5
    global D5
    global Eb5
    global E5
    global F5
    global Gb5
    global G5
    global A5
    global Bb5
    global B5
    global C6
    global D6
    global Eb6
    global E6
    global F6
    global Gb6
    global G6
    global A6
    global Bb6
    global B6
    global C7
    
    global I
    global IV
    global V

    global INotes
    global IVNotes
    global VNotes

    global melodyNotes
    
    C3  = baseNote#130.81=C3
    D3  = C3*9/8
    E3  = C3*5/4
    F3  = C3*4/3
    G3  = C3*3/2
    A3  = C3*5/3
    Bb3 = C3*16/9
    B3  = C3*15/8
    C4  = C3*2/1#
    D4  = C4*9/8
    Eb4 = C4*19/16
    E4  = C4*5/4
    F4  = C4*4/3
    G4  = C4*3/2
    A4  = C4*5/3
    B4  = C4*15/8
    C5  = C4*2/1#
    D5  = C5*9/8
    Eb5 = C5*19/16
    E5  = C5*5/4
    F5  = C5*4/3
    Gb5 = C5*7/5
    G5  = C5*3/2
    A5  = C5*5/3
    Bb5 = C5*16/9
    B5  = C5*15/8
    C6  = C5*2/1#
    D6  = C6*9/8
    Eb6 = C6*19/16
    E6  = C6*5/4
    F6  = C6*4/3
    Gb6 = C6*7/5
    G6  = C6*3/2
    A6  = C6*5/3
    Bb6 = C6*16/9
    B6  = C6*15/8
    C7  = C6*2/1#

    '''#Dictionary of possible notes in the melody
    melodyNotes = {
        1:C5,
        2:D5,
        3:Eb5,
        4:E5,
        5:F5,
        6:Gb5,
        7:G5,
        8:A5,
        9:Bb5,
        10:B5,
        11:C6,
        12:D6,
        13:Eb6,
        14:E6,
        15:F6,
        16:Gb6,
        17:G6,
        18:A6,
        19:Bb6,
        20:B6,
        21:C7
        }'''

    global BluesNotes

    BluesNotes   = {1:C5,
                    2:Eb5,
                    3:F5,
                    4:Gb5,
                    5:G5,
                    6:Bb5,
                    7:B5,
                    8:C6,
                    9:Eb6,
                    10:F6,
                    11:Gb6,
                    12:G6,
                    13:Bb6,
                    14:B6,
                    15:C7}

    '''
    Chord = [
        [inverson a]
        [inversion b]
        ]
    '''
    I   = [C3, E3, G3, Bb3]
    IV  = [F3, A3, C4, Eb4]
    V   = [G3, B3, D4, F4]

setPitchCenter(220)

def drawText(window, text, color, centerX, centerY):
    font=pygame.font.Font("Apple Chancery.ttf", 36)
    renderedText=font.render(text,True,color)
    textpos=renderedText.get_rect()
    textpos.centerx=centerX
    textpos.centery=centerY-1
    window.blit(renderedText, textpos)

#the following 4 methods are the same, just used for different notes played at the same time

def chordRoot(chord, length):#play bottom note of chord
    duration = length    # in seconds, may be float
    f = chord[0]        # sine frequency, Hz, may be float
    duration*=4
    # generate samples, note conversion to float32 array
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)
    # play. May repeat with different volume values (if done interactively) 
    stream.write(volume*samples)
    stream.stop_stream()
    stream.close()
    
def chordThird(chord, length):
    duration = length
    f = chord[1]
    duration*=4
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)
    stream.write(volume*samples)
    stream.stop_stream()
    stream.close()
    
def chordFifth(chord, length):
    duration = length
    f = chord[2]
    duration*=4
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)
    stream.write(volume*samples)
    stream.stop_stream()
    stream.close()

def chordFlatSeventh(chord, length):
    duration = length
    f = chord[3]
    duration*=4
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)
    stream.write(volume*samples)
    stream.stop_stream()
    stream.close()

def melodyNote(note, length):#play a melody note
    duration = length
    f = note
    duration*=4
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)
    stream.write(volume*0.75*samples)
    stream.stop_stream()
    stream.close()

def playChord(chord, length):#pass the set of notes and duration of chord (currently 1 measure)
    thread.start_new_thread(chordRoot, (chord, length))
    thread.start_new_thread(chordThird, (chord, length))
    thread.start_new_thread(chordFifth, (chord, length))
    thread.start_new_thread(chordFlatSeventh, (chord, length))

def improvise(beat, previousInterval, chordIndicator):#pass the current chord andlast note
    inRange = False
    tryAgain = False
    while not(inRange):#repeats until the note picked is within the range of notes available
        interval=previousInterval+randint(0,maxMelodyJump)-randint(0,maxMelodyJump)#add or subtract between 1 and the max melody jump to the note
        closest = 16
        if 1<=interval and interval<=15 and not(tryAgain):#check if note is within range
            inRange = True
                                   
    pitch = BluesNotes[interval]#set the pitch to the hertz value that corresponds to the interval chosen
    thread.start_new_thread(melodyNote, (pitch, beatLength))#play the melody pitch
    return interval#return the interval chosen   

def musicThread():
    interval = 8
    measure = 1
    while not(programQuit):
        if musicPlaying:
            if (measure >= 1 and measure <= 4) or (measure >= 7 and measure <= 8) or (measure >= 11 and measure <= 12):
                playChord(I,4*beatLength)
                chordIndicator = 1
            if (measure >=5 and measure <= 6) or measure == 10:
                playChord(IV,4*beatLength)
                chordIndicator = 4
            if measure == 9:
                playChord(V,4*beatLength)
                chordIndicator = 5

            for beat in range(1,5):
                improvise(beat, interval, chordIndicator)
                sleep(beatLength)
            
            measure+=1
            if measure == 13:
                measure = 1

def button(name, color, rect, mousePos):
    pygame.draw.rect(window, color, rect, 5)
    drawText(window, name, color, rect[0]+rect[2]/2, rect[1]+rect[3]/2)
    if mousePos[0]>rect[0] and mousePos[0]<rect[0]+rect[2] and mousePos[1]>rect[1] and mousePos[1]<rect[1]+rect[3]:
        pygame.draw.rect(window, (100,100,100), rect,0)
        drawText(window, name, (255,255,255),rect[0]+rect[2]/2, rect[1]+rect[3]/2)
        if (mousePressed[0] or mousePressed[1] or mousePressed[2]):
            return True

programQuit = False
musicPlaying = False

thread.start_new_thread(musicThread, ())

tempoRect = (tempo*2.5, 625, 100, 50)

while True:
    window.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            programQuit = True
            pygame.quit()
            sys.exit(0)

    mousePos=pygame.mouse.get_pos()
    mousePressed=pygame.mouse.get_pressed()
    ########################################################
    top = 0
    left = 0
    width = 100
    if button("Exit", (255,255,255), (left,top,width,50), mousePos):
        programQuit = True
        pygame.quit()
        sys.exit(0)
    ########################################################
    top = 350
    left = 700
    width = 100
    if button("Stop", (255,255,255), (left,top,width,50), mousePos):
        musicPlaying = False
    ########################################################
    top = 350
    left = 500
    width = 120
    if button("Start", (255,255,255), (left,top,width,50), mousePos):
        musicPlaying = True
    ########################################################
    pygame.draw.rect(window, (50,50,50), (88,635, 1022,30), 0)
    pygame.draw.rect(window, (255,255,255), tempoRect, 0)
    drawText(window, str(tempo), (0,0,0), tempoRect[0]+tempoRect[2]/2, tempoRect[1]+tempoRect[3]/2)
    drawText(window, "Tempo", (255,255,255), 1205,650)
    if mousePos[0]>tempoRect[0] and mousePos[0]<tempoRect[0]+tempoRect[2] and mousePos[1]>tempoRect[1] and mousePos[1]<tempoRect[1]+tempoRect[3]:
        pygame.draw.rect(window, (200,200,200), tempoRect,0)
        drawText(window, str(tempo),(0,0,0),tempoRect[0]+tempoRect[2]/2, tempoRect[1]+tempoRect[3]/2)
        offset = mousePos[0]-tempoRect[0]
        while ((mousePressed[0] or mousePressed[1] or mousePressed[2])):
            mousePressed=pygame.mouse.get_pressed()
            pygame.draw.rect(window, (0,0,0), tempoRect,0)
            draggingMousePos = pygame.mouse.get_pos()
            if draggingMousePos[0]-offset>=98 and draggingMousePos[0]-offset<=1000:
                tempoRect = [draggingMousePos[0]-offset, tempoRect[1], tempoRect[2], tempoRect[3]]
            tempo = round(tempoRect[0]/2.5)
            beatLength = 1/(tempo/60)
            pygame.draw.rect(window, (50,50,50), (88,635, 1022,30), 0)
            pygame.draw.rect(window, (100,100,100), tempoRect,0)
            drawText(window, str(tempo), (255,255,255),tempoRect[0]+tempoRect[2]/2, tempoRect[1]+tempoRect[3]/2)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    programQuit = True
                    pygame.quit()
                    sys.exit(0)
    ########################################################

    pygame.display.update()
