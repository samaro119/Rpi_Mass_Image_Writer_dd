#!/usr/bin/env python3

import smbus

# ===========================================================================
# Adafruit_I2C Class
# ===========================================================================

class Adafruit_I2C(object):

  @staticmethod
  def getPiRevision():
    "Gets the version number of the Raspberry Pi board"
    try:
      with open('/proc/cpuinfo','r') as f:
        for line in f:
          if line.startswith('Revision'):
            return 1 if line.rstrip()[-1] in ['2','3'] else 2
    except:
      return 0

  @staticmethod
  def getPiI2CBusNumber():
    return 1 if Adafruit_I2C.getPiRevision() > 1 else 0

  def __init__(self, address, busnum=-1, debug=False):
    self.address = address
    self.bus = smbus.SMBus(busnum if busnum >= 0 else Adafruit_I2C.getPiI2CBusNumber())
    self.debug = debug

  def reverseByteOrder(self, data):
    byteCount = len(hex(data)[2:].replace('L','')[::2])
    val       = 0
    for i in range(byteCount):
      val    = (val << 8) | (data & 0xff)
      data >>= 8
    return val

  def errMsg(self):
    print(f"Error accessing 0x{self.address:02X}: Check your I2C address")
    return -1

  def write8(self, reg, value):
    try:
      self.bus.write_byte_data(self.address, reg, value)
      if self.debug:
        print(f"I2C: Wrote 0x{value:02X} to register 0x{reg:02X}")
    except IOError as err:
      return self.errMsg()

  def write16(self, reg, value):
    try:
      self.bus.write_word_data(self.address, reg, value)
      if self.debug:
        print(f"I2C: Wrote 0x{value:02X} to register pair 0x{reg:02X}, 0x{reg+1:02X}")
    except IOError as err:
      return self.errMsg()

  def writeRaw8(self, value):
    try:
      self.bus.write_byte(self.address, value)
      if self.debug:
        print(f"I2C: Wrote 0x{value:02X}")
    except IOError as err:
      return self.errMsg()

  def writeList(self, reg, list):
    try:
      if self.debug:
        print(f"I2C: Writing list to register 0x{reg:02X}:")
        print(list)
      self.bus.write_i2c_block_data(self.address, reg, list)
    except IOError as err:
      return self.errMsg()

  def readList(self, reg, length):
    try:
      results = self.bus.read_i2c_block_data(self.address, reg, length)
      if self.debug:
        print(f"I2C: Device 0x{self.address:02X} returned the following from reg 0x{reg:02X}")
        print(results)
      return results
    except IOError as err:
      return self.errMsg()

  def readU8(self, reg):
    try:
      result = self.bus.read_byte_data(self.address, reg)
      if self.debug:
        print(f"I2C: Device 0x{self.address:02X} returned 0x{result & 0xFF:02X} from reg 0x{reg:02X}")
      return result
    except IOError as err:
      return self.errMsg()

  def readS8(self, reg):
    try:
      result = self.bus.read_byte_data(self.address, reg)
      if result > 127: result -= 256
      if self.debug:
        print(f"I2C: Device 0x{self.address:02X} returned 0x{result & 0xFF:02X} from reg 0x{reg:02X}")
      return result
    except IOError as err:
      return self.errMsg()

  def readU16(self, reg, little_endian=True):
    try:
      result = self.bus.read_word_data(self.address,reg)
      if not little_endian:
        result = ((result << 8) & 0xFF00) + (result >> 8)
      if (self.debug):
        print(f"I2C: Device 0x{self.address:02X} returned 0x{result & 0xFFFF:04X} from reg 0x{reg:02X}")
      return result
    except IOError as err:
      return self.errMsg()

  def readS16(self, reg, little_endian=True):
    try:
      result = self.readU16(reg,little_endian)
      if result > 32767: result -= 65536
      return result
    except IOError as err:
      return self.errMsg()


if __name__ == '__main__':
  try:
    bus = Adafruit_I2C(address=0)
    print("Default I2C bus is accessible")
  except:
    print("Error accessing default I2C bus")
