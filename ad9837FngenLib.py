import sys
# sys.path.append('home/pi/Documents/RaspberryPiCommon/pidev/Cyprus_Commands')
import spidev
from time import sleep

## SPI
# To see SPI buses and devices on RPi, type "ls /dev/*spi*" in the terminal.
# Typically, the bus is always 0, and the device may be 0 (if wired to clock pin 24) or 1 (pin 26).
spiBus = 0
device = 0
spi = spidev.SpiDev()
spi.open(spiBus, device)
# SPI mode is 0b00. 0b + 1 because the clock polarity is high and + 0 again because the phase trigger is on the falling edge.
spi.mode = 0b10
delay = .001
spiFrequency = 1000000
freq_clock = 16000000

def break_into_list(word):
    return [word >> 8, word & 0x0FF]

def send_freq(freq):
    print("Sending frequency of {} Hz.".format(freq))
    
    # 0x2100 - Control Register
    # 0x2100 -> 0010 0001 0000 0000.
    # D15 and 14 must be zero to inform the AD9837 that the contents of the control register will be altered.
    # D13's value of 1 allows a complete word to be loaded into a frequency register in two consective writes.
    # The first write contains the 14 LSBs of the frequency word, the second the 14 MSBs.
    # D8 controls the internal reset function, and its value of 1 resets internal registers to 0, corresponding to an analog output of midscale.
    controlRegStart = 0x2100
    # For a triangular wave:
    #controlRegStart = 0x2101
    
    # The output frequenct is fclk/2^28 * FREQREG. For us, fclk is 16 MHz.
    # We can save processor time by specifying a constant for fclk/2^28 = 0.0596.
    # 0.0596 Hz is the smallest step size for adjusting the output frequency.
    #freq_word = int(round(float(freq * (2 ** 28)) / freq_clock))
    freq_word = int(freq/0.0596)
    # frequency word divide to two parts as LSB and MSB.
    # 3FFF = 0011 1111 1111 1111
    LSB = (freq_word & 0x3FFF)
    # FFFC000 >> 14 = 1111 1111 1111 11
    MSB = (freq_word & 0xFFFC000) >> 14
    # DB15 and DB14 are set to 0 and 1 in order to write to frequency register 0 (FREQ0).
    LSB |= 0x4000
    MSB |= 0x4000

    # DB15, DB14, DB13, DB12 = 110X according to the documentation,
    # respectively, for the address for Phase Register 0.
    # The remaining 12 bits are the data bits and are all 0s in this case
    phase = 0
    phase |= 0xC000
    
    # As per figure 23 in AD9837 data sheet, we need to set the reset bit to 0 as well as select the frequency and phase registers.
    # Our value doesn't change save for D13, which we change to 0 to avoid an internal reset.
    controlRegEnd = 0x2000
    
    dataArray = [controlRegStart, LSB, MSB, phase, controlRegEnd]

    for data in dataArray:
        spi.xfer(break_into_list(data), spiFrequency)
        sleep(2*delay)
    print("Sent frequency of {} Hz.".format(freq))

def fiveTones(tempo):
    # An average tempo: 0.5.
    for octave in range(1, 4, 1):
        print("Sending Five Tones with a Tempo of {}!".format(tempo))
        send_freq(293.7*octave)
        sleep(tempo)
        send_freq(329.63*octave)
        sleep(tempo)
        send_freq(261.7*octave)
        sleep(tempo)
        send_freq(130.81*octave)
        sleep(tempo)
        send_freq(196.0*octave)
        sleep(tempo*2)
        send_freq(0)
    

