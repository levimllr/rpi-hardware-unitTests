import sys
# sys.path.append('home/pi/Documents/RaspberryPiCommon/pidev/Cyprus_Commands')
import smbus
from time import sleep

## I2C
# I2C channel 1 is connected to the GPIO pins
channel = 1

# Look this guy up using "i2cdetect -l" and "i2cdetect -y #" in the terminal!
address = 0x4b

# Initialize I2C (SMBus)
i2cBus = smbus.SMBus(channel)

def setVolume(volume):
    # Volume should be a hex value between 0x05 and 0x3f.
    # Recommended > 0x20 <0x40
    print("Setting volume to {}!".format(hex(volume)))
    volumeData = [0] + [volume]
    i2cBus.write_i2c_block_data(address, 0, volumeData)
    print("Volume set to {}.".format(hex(volume)))
