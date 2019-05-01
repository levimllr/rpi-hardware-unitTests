import sys
import max9744AmpLib as amp
import ad9837FngenLib as fngen
import ds1807Lib as pot
from time import sleep

amp.setVolume(0x3f)

fngen.send_freq(200)

for i in range(0, 40):
    pot.setGain(i)
    sleep(0.05)
    
for j in range(40, -1, -1):
    pot.setGain(j)
    sleep(0.05)   
    