import sys
import max9744AmpLib as amp
import ad9837FngenLib as fngen
from time import sleep

amp.setVolume(0x25)

fngen.fiveTones(1)
    