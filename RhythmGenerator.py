from random import randint
import _thread as thread
from random import randint
import pyaudio
import numpy as np
from time import sleep
import pygame, sys
from pygame.locals import *
from math import ceil

'''
0=rest/end note
1=start/change note
2=continue note
'''

tempo = 120
beatLength = 1/(tempo/60) #convert beats per minute to seconds per beat

p = pyaudio.PyAudio()#initialize audio track
fs = 44100       # sampling rate, Hz, must be integer
volume = 0.5     # range [0.0, 1.0]



r=0
iterations = 8
rhythm = ""
for subdivision in range(0,iterations):
    if r==0:
        r=[0,1,1,1][randint(0,3)]
    else:
        r=[0,1,2,2,2][randint(0,4)]
    rhythm = rhythm+str(r)
print(rhythm)


while True:
    for subdivision in range(0,iterations):
        if r==0:
            r=[0,1,1,1][randint(0,3)]
        else:
            r=[0,1,2,2,2][randint(0,4)]
        rhythm = rhythm+str(r)+"3"

                
def note(note, length):#play a melody note
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

note(randint(220,880), 2)
