tempo = 120
timeSignature = 4
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
pygame.display.set_caption("Composer","Composer")

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
    global B3
    global C4
    global D4
    global E4
    global F4
    global G4
    global A4
    global B4
    global C5
    global D5
    global E5
    global F5
    global G5
    global A5
    global B5
    global C6
    global D6
    global E6
    global F6
    global G6
    global A6
    global B6
    global C7
    
    global I
    global II
    global III
    global IV
    global V
    global VI
    global VII

    global INotes
    global IINotes
    global IIINotes
    global IVNotes
    global VNotes
    global VINotes
    global VIINotes

    global melodyNotes
    
    C3 = baseNote#130.81=C3
    D3 = C3*9/8
    E3 = C3*5/4
    F3 = C3*4/3
    G3 = C3*3/2
    A3 = C3*5/3
    B3 = C3*15/8
    C4 = C3*2/1#
    D4 = C4*9/8
    E4 = C4*5/4
    F4 = C4*4/3
    G4 = C4*3/2
    A4 = C4*5/3
    B4 = C4*15/8
    C5 = C4*2/1#
    D5 = C5*9/8
    E5 = C5*5/4
    F5 = C5*4/3
    G5 = C5*3/2
    A5 = C5*5/3
    B5 = C5*15/8
    C6 = C5*2/1#
    D6 = C6*9/8
    E6 = C6*5/4
    F6 = C6*4/3
    G6 = C6*3/2
    A6 = C6*5/3
    B6 = C6*15/8
    C7 = C6*2/1#

    ###list of possible notes in the melody
    ##melodyNotes = [
    ##    [C5, 1 ],
    ##    [D5, 2 ],
    ##    [E5, 3 ],
    ##    [F5, 4 ],
    ##    [G5, 5 ],
    ##    [A5, 6 ],
    ##    [B5, 7 ],
    ##    [C6, 8 ],
    ##    [D6, 9 ],
    ##    [E6, 10],
    ##    [F6, 11],
    ##    [G6, 12],
    ##    [A6, 13],
    ##    [B6, 14],
    ##    [C7, 15]
    ##    ]

    #Dictionary of possible notes in the melody
    melodyNotes = {
        1:C5,
        2:D5,
        3:E5,
        4:F5,
        5:G5,
        6:A5,
        7:B5,
        8:C6,
        9:D6,
        10:E6,
        11:F6,
        12:G6,
        13:A6,
        14:B6,
        15:C7
        }

    INotes   = {1:C5, 3:E5, 5:G5, 8:C6,  10:E6, 12:G6, 15:C7}
    IINotes  = {2:D5, 4:F5, 6:A5, 9:D6,  11:F6, 13:A6}
    IIINotes = {3:E5, 5:G5, 7:B5, 10:E6, 12:G6, 14:B6}
    IVNotes  = {1:C5, 4:F5, 6:A5, 8:C6,  11:F6, 13:A6, 15:C7}
    VNotes   = {2:D5, 5:G5, 7:B5, 9:D6,  12:G6, 14:B6}
    VINotes  = {1:C5, 3:E5, 6:A5, 8:C6,  10:E6, 13:A6, 15:C7}
    VIINotes = {2:D5, 4:F5, 7:B5, 9:D6,  11:F6, 14:B6}

    '''
    Chord = [
        [inverson a]
        [inversion b]
        ]
    '''
    I   = [
        [G3, C4, E4],
        [C4, E4, G4],
        ]
    II = [
        [A3, D4, F4],
        [D4, F4, A4],
        ]
    III  = [
        [B3, E4, G4],
        [E4, G4, B4],
        ]
    IV   = [
        [A3, C4, F4],
        [C4, F4, A4],
        ]
    V  = [
        [G3, B3, D4],
        [B3, D4, G4],
        ]
    VI = [
        [A3, C4, E4],
        [C4, E4, A4],
        ]
    VII  = [
        [F3, B3, D4],
        [B3, D4, F4],
        ]

setPitchCenter(130.81)

def drawText(window, text, color, centerX, centerY):
    font=pygame.font.Font("Apple Chancery.ttf", 36)
    renderedText=font.render(text,True,color)
    textpos=renderedText.get_rect()
    textpos.centerx=centerX
    textpos.centery=centerY-1
    window.blit(renderedText, textpos)

def pickChord(oldChord, oldChordIndicator):
        
    if oldChordIndicator == 1:#detect if old chord was I chord
            n = randint(0,6)
            mode = [I,II,III,IV,V,VI,VII][n]#choose mode
            chordIndicator = n+1#keep track of what chord is being played
            newChord = mode[randint(0,len(mode)-2)]#new chord = random inversion of the selected mode
            #len(mode)-2 because the last element of each chord list is the melodychord tones, not an inversion of the chord
            newChord.append(chordIndicator)#sneak out the chord indicator while still only returning one variable
    #the rest of these work the same as above
    if oldChordIndicator == 2:
            n = randint(0,2)
            mode = [IV,V,VII][n]
            if n == 0:
                chordIndicator=4
            if n == 1:
                chordIndicator=5
            if n == 2:
                chordIndicator=7
            newChord = mode[randint(0,len(mode)-2)]
            newChord.append(chordIndicator)
    if oldChordIndicator == 3:
            n = randint(0,2)
            mode = [II,IV,VI][n]
            if n == 0:
                chordIndicator=2
            if n == 1:
                chordIndicator=4
            if n == 2:
                chordIndicator=6
            newChord = mode[randint(0,len(mode)-2)]
            newChord.append(chordIndicator)
    if oldChordIndicator == 4:
            n = randint(0,3)
            mode = [I,III,V,VII][n]
            if n == 0:
                chordIndicator=1
            if n == 1:
                chordIndicator=3
            if n == 2:
                chordIndicator=5
            if n == 3:
                chordIndicator=7
            newChord = mode[randint(0,len(mode)-2)]
            newChord.append(chordIndicator)
    if oldChordIndicator == 5:
            mode = [I][0]
            chordIndicator = 1
            newChord = mode[randint(0,len(mode)-2)]
            newChord.append(chordIndicator)
    if oldChordIndicator == 6:
            n = randint(0,3)
            mode = [I,II,IV,V][n]
            if n == 0:
                chordIndicator=1
            if n == 1:
                chordIndicator=2
            if n == 2:
                chordIndicator=4
            if n == 3:
                chordIndicator=5
            newChord = mode[randint(0,len(mode)-2)]
            newChord.append(chordIndicator)
    if oldChordIndicator == 7:
            n = randint(0,1)
            mode = [I,II][n]
            chordIndicator = n+1
            newChord = mode[randint(0,len(mode)-2)]
            newChord.append(chordIndicator)
            
    return newChord



#the following 4 methods are the same, just used for different notes played at the same time

def chordBottom(chord, length):#play bottom note of chord
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
    
def chordMiddle(chord, length):#play middle note of chord
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
    
def chordTop(chord, length):#play top note of chord
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
    thread.start_new_thread(chordBottom, (chord, length))#play  bottom note
    thread.start_new_thread(chordMiddle, (chord, length))#play  middle note
    thread.start_new_thread(chordTop, (chord, length))   #play  top note

def playMelody(beat, previousInterval, chordIndicator):#pass the current chord and current beat
    inRange = False
    tryAgain = False
    while not(inRange):#repeats until the note picked is within the range of notes available
        interval=previousInterval+randint(0,maxMelodyJump)-randint(0,maxMelodyJump)#add or subtract between 1 and the max melody jump to the note
        if beat%2:#if on odd-numbered beat
            closest = 16
            if chordIndicator==1:
                for chordTone in INotes:#for each chord tone,
                    distance = abs(chordTone-interval)#find the distance between the note picked and the chord tone.
                    if distance == 1:#if the chord tone is close,
                        interval+=[-1,1][randint(0,1)]#change the pitch.
                        tryAgain = True#in case tone was 6th or 7th and changed to 6th or 7th instead of 5th or 8th
                    elif distance==0:
                        tryAgain = False
                        
            if chordIndicator==2:#2
                for chordTone in IINotes:
                    distance = abs(chordTone-interval)
                    if distance == 1:
                        interval+=[-1,1][randint(0,1)]
                        tryAgain = True
                    elif distance==0:
                        tryAgain = False
            if chordIndicator==3:#3
                for chordTone in IIINotes:
                    distance = abs(chordTone-interval)
                    if distance == 1:
                        interval+=[-1,1][randint(0,1)]
                        tryAgain = True
                    elif distance==0:
                        tryAgain = False
            if chordIndicator==4:#4
                for chordTone in IVNotes:
                    distance = abs(chordTone-interval)
                    if distance == 1:
                        interval+=[-1,1][randint(0,1)]
                        tryAgain = True
                    elif distance==0:
                        tryAgain = False
            if chordIndicator==5:#5
                for chordTone in VNotes:
                    distance = abs(chordTone-interval)
                    if distance == 1:
                        interval+=[-1,1][randint(0,1)]
                        tryAgain = True
                    elif distance==0:
                        tryAgain = False
            if chordIndicator==6:#6
                for chordTone in VINotes:
                    distance = abs(chordTone-interval)
                    if distance == 1:
                        interval+=[-1,1][randint(0,1)]
                        tryAgain = True
                    elif distance==0:
                        tryAgain = False
            if chordIndicator==7:#7
                for chordTone in VIINotes:
                    distance = abs(chordTone-interval)
                    if distance == 1:
                        interval+=[-1,1][randint(0,1)]
                        tryAgain = True
                    elif distance==0:
                        tryAgain = False

        if 1<=interval and interval<=15 and not(tryAgain):#check if note is within range
            inRange = True
                                   
    pitch = melodyNotes[interval]#set the pitch to the hertz value that corresponds to the interval chosen
    thread.start_new_thread(melodyNote, (pitch, beatLength))#play the melody pitch
    return interval#return the interval chosen   

interval = 8

def musicThread():
    #let the chord selection metod know that this is the first chord of the song
    chord = [1,1,1]
    chordIndicator = 5#V always leads to I, so song will start on I chord
    while not(programQuit):
        if musicPlaying: 
            chord = pickChord(chord, chordIndicator)#select a chord based on the previous chord
            chordIndicator = chord[len(chord)-1]
            #print("Chord: "+str(chordIndicator))
            playChord(chord,timeSignature*beatLength)#play the chord
            
            for beat in range(timeSignature):#go through each beat of the measure
                playMelody(beat+1,interval, chordIndicator)#play a melody note for that beat
                sleep(beatLength)#wait for one beat
                #melody note can change after one beat of waiting, chord changes after all beats in a measure of waiting

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
keyRect = ((C3+185)/5.2+435, 465, 100, 50)
    
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
    top = 540
    left = 90
    width = 50
    for n in range(1,13):
        if n == timeSignature:
            pygame.draw.rect(window, (50,50,50), (left,top,width,60), 0)
        if button(str(n), (255,255,255), (left,top,width,60), mousePos):
            timeSignature = n
        left+=80
    drawText(window, "Beats per Chord", (255,255,255), 1160,570)
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
            pygame.draw.rect(window, (50,50,50), (88,475, 980,30), 0)
            pygame.draw.rect(window, (255,255,255), keyRect, 0)
            drawText(window, str(round(C3)), (0,0,0), keyRect[0]+keyRect[2]/2, keyRect[1]+keyRect[3]/2)
            drawText(window, "Pitch Center", (255,255,255), 1185,490)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    programQuit = True
                    pygame.quit()
                    sys.exit(0)
    ########################################################
    pygame.draw.rect(window, (50,50,50), (88,475, 980,30), 0)
    pygame.draw.rect(window, (255,255,255), keyRect, 0)
    drawText(window, str(round(C3)), (0,0,0), keyRect[0]+keyRect[2]/2, keyRect[1]+keyRect[3]/2)
    drawText(window, "Pitch Center", (255,255,255), 1185,490)
    if mousePos[0]>keyRect[0] and mousePos[0]<keyRect[0]+keyRect[2] and mousePos[1]>keyRect[1] and mousePos[1]<keyRect[1]+keyRect[3]:
        pygame.draw.rect(window, (200,200,200), keyRect,0)
        drawText(window, str(round(C3)),(0,0,0),keyRect[0]+keyRect[2]/2, keyRect[1]+keyRect[3]/2)
        offset = mousePos[0]-keyRect[0]
        while ((mousePressed[0] or mousePressed[1] or mousePressed[2])):
            mousePressed=pygame.mouse.get_pressed()
            pygame.draw.rect(window, (0,0,0), keyRect,0)
            draggingMousePos = pygame.mouse.get_pos()
            if draggingMousePos[0]-offset>=98 and draggingMousePos[0]-offset<=958:
                keyRect = [draggingMousePos[0]-offset, keyRect[1], keyRect[2], keyRect[3]]
            C3 = (keyRect[0]+185)/5.2
            setPitchCenter(C3)
            pygame.draw.rect(window, (50,50,50), (88,475, 980,30), 0)
            pygame.draw.rect(window, (100,100,100), keyRect,0)
            drawText(window, str(round(C3)), (255,255,255),keyRect[0]+keyRect[2]/2, keyRect[1]+keyRect[3]/2)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    programQuit = True
                    pygame.quit()
                    sys.exit(0)
    ########################################################

    pygame.display.update()
