import sys
# sys.path.append('home/pi/Documents/RaspberryPiCommon/pidev/Cyprus_Commands')
import smbus
from time import sleep

## I2C
# I2C channel 1 is connected to the GPIO pins
channel = 1

# Look this guy up using "i2cdetect -l" and "i2cdetect -y #" in the terminal!
address = 0x28

# Initialize I2C (SMBus)
i2cBus = smbus.SMBus(channel)

def setGain(gain):
    # Gain should be a hex value between 0x00 and 0x40.
    # Each increment corresponds to an attenuation of 1 dB.
    print("Setting digital potentiometer gain to {}!".format(hex(gain)))
    # Convert gain into a list so jive with the .write_i2c_block_data method.
    gainData = [gain]
    # 1010 1001 (0xa9) is the command word for writing to potentiometer 0.
    # 1010 1010 (0xaa) is the command word for writing to potentiometer 1.
    # 1010 1111 (0xaf) is the command word for writing to both pots.
    cmdWord = 0xaf
    i2cBus.write_i2c_block_data(address, cmdWord, gainData)
    print("Set digital potentiometer gain to {}.".format(hex(gain)))

setGain(0x06)
