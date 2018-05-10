import _thread as thread
from random import randint
import pyaudio
import numpy as np
from time import sleep
import pygame, sys
from pygame.locals import *
pygame.mixer.init()
pygame.mixer.music.load("Bass Drum.mp3")
pygame.mixer.music.play()
