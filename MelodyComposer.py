#imports
import _thread as thread
from random import randint
import pyaudio
import numpy as np
from time import sleep

tempo = 40
timeSignature = 4
maxMelodyJump = 6

beatLength = 1/(tempo/60) #convert beats per minute to seconds per beat

p = pyaudio.PyAudio()#initialize audio track
fs = 44100       # sampling rate, Hz, must be integer
volume = 0.5     # range [0.0, 1.0]

#set pitch values
#this will become a method later on if key changes are introduced
C3 = 130.81#
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

INotes = {1:C5, 3:E5, 5:G5, 8:C6, 10:E6, 12:G6, 15:C7}

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

def playMelody(previousInterval):#pass the current chord and current beat
    inRange = False
    tryAgain = False
    while not(inRange):
        interval=previousInterval+randint(1,maxMelodyJump)-randint(1,maxMelodyJump)
        if True:#beat%2:
            closest = 16
            for chordTone in INotes:
                distance = abs(chordTone-interval)
                if distance == 1:
                    interval+=[-1,1][randint(0,1)]
                    tryAgain = True
        if 1<=interval and interval<=15 and not(tryAgain):
            inRange = True
    pitch = melodyNotes[interval]
    thread.start_new_thread(melodyNote, (pitch, beatLength))
    return interval

interval = 0
while True:
    for beat in range(timeSignature):#go through each beat of the measure
        interval = playMelody(interval)#play a melody note
        sleep(beatLength)#wait for one beat
        #melody note can change after one beat of waiting, chord changes after all beats in a measure of waiting

