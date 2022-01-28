import smbus2
import time
import numpy as np
from static import IC2_BRIDGE_ADDRESS
from static import START_MARKER
from static import END_MARKER
from static import SEPERATOR


class I2CCom:

    def __init__(self, **kwargs):
        self.address = IC2_BRIDGE_ADDRESS
        self.number = 0
        self.bus = smbus2.SMBus(1)
        self.startmarker = START_MARKER
        self.endmarker = END_MARKER
        self.seperator = SEPERATOR

    def write_number(self, value):
        self.bus.write_byte(self.address, int(value))
        return -1

    def read_number(self):
        self.number = self.bus.read_byte(self.address)
        return self.number

    def read_char(self):
        self.number = self.bus.read_byte(self.address)
        return chr(self.number)

    def string_to_bytes(self, val):
        retVal = []
        for c in val:
            retVal.append(ord(c))
        return retVal

    def send_data_to_i2c(self, data):
        byteData = self.string_to_bytes(data)
        self.bus.write_i2c_block_data(self.address, 0x00, byteData)
        return -1

    def read_data_from_i2c(self):

        tmp_byte_array = self.bus.read_i2c_block_data(self.address, 0, 32)
        tmp_str_array = []
        for element in tmp_byte_array:
            tmp_str_array.append(chr(element))

        start = tmp_str_array.index(self.startmarker) + len(self.startmarker)
        end = tmp_str_array.index(self.endmarker, start)

        tmp_array = []

        str = ''
        for element in tmp_str_array[start:end]:
            if element is not ':':
                str += element
            else:
                tmp_array.append(int(str))
                str = ''

        return  tmp_array

    def log_data(self, header, data_to_log):
        print(header, data_to_log)

    def send_data_to_slave(self, data_to_send, interval):
        self.send_data_to_i2c(data_to_send)
        time.sleep(interval)

    def parse_i2c_data(self):
        tmp_data = np.array()
