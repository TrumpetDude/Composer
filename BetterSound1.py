import numpy
from numpy.fft import fft, ifft
from numpy.random import random_sample
from alsaaudio import PCM, PCM_NONBLOCK, PCM_FORMAT_FLOAT_LE

pcm = PCM()#mode=PCM_NONBLOCK)
pcm.setrate(44100)
pcm.setformat(PCM_FORMAT_FLOAT_LE)
pcm.setchannels(1)
pcm.setperiodsize(4096)

def sine_wave(x, freq=100):
    sample = numpy.arange(x*4096, (x+1)*4096, dtype=numpy.float32)
    sample *= numpy.pi * 2 / 44100
    sample *= freq
    return numpy.sin(sample)

for x in xrange(1000):
    sample = sine_wave(x, 100)
    pcm.write(sample.tostring())
