import string
import csv
import os.path
import sys
import serial

class RFIDReader:

    def __init__(self, device, rate):
        self.dev = serial.Serial(device,rate)
        
    def readCard(self):
        stri=''
        key = ''
        
        while key == '':
            ID = ""
            read_byte = self.dev.read()
            if read_byte=="\x02":
                for Counter in range(12):
                    read_byte=self.dev.read()
                    ID = ID + str(read_byte)
                key = ID
        return key

       


