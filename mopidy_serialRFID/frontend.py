from __future__ import unicode_literals
import logging
import traceback

from mopidy import core
import serial
import time,os
from threading import Thread
import threading
import csv
import pykka

import RPi.GPIO as GPIO
logger = logging.getLogger(__name__)


                    
class serialRFID(pykka.ThreadingActor, core.CoreListener):
    
   
  
    def readCard(self):
        key = ''
        
        while key == '' or len(key) < 12:
            ID = ""
            read_byte = self.dev.read()
            if read_byte=="\x02":
                for Counter in range(12):
                    read_byte=self.dev.read()
                    ID = ID + str(read_byte)
                key = ID
        return key
 
    def readList(self):
        with open(self.path + '/cardList.csv', mode='r') as infile:
            reader = csv.reader(infile)
            cardList = {rows[0]:rows[1] for rows in reader}
            infile.close()
        return cardList
    
    def getPlaylist(self,card):
        try:
            self.cardList = self.readList()
            return self.cardList[card]
        except:
            logger.info('Card is not card list: '+ card)
            return ''
            
    def play(self, plist):
        try:
            logger.info('Playing '+plist)
            self.core.playback.stop()
            self.core.tracklist.clear()
            self.core.tracklist.add(uri=plist)
            self.core.playback.play()
        except:
            logger.error('Could not play playlist '+plist)
            logger.error(sys.exc_info()[0])

           
            
    
    def eventDetected(self, channel):
        logger.info("reading rfid card")
        #initialize device
        self.dev = serial.Serial(self.deviceName,self.rate)
  
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.card = self.readCard()
        logger.info('Read card '+self.card)
        self.plist = self.getPlaylist(self.card)
        logger.info('Playlist'+self.plist)
        if self.plist != '':
            self.play(self.plist)
        #close port
        self.dev.close()
                
    
    
    def __init__(self, config, core):
        super(serialRFID, self).__init__()
        self.menu = False
        self.core = core
        self.config = config
        self.deviceName = config['serialRFID']['device']
        self.rate = config['serialRFID']['rate']
        
        
        GPIO.setmode(GPIO.BOARD)
        logger.info("Started setup")
        
        #register buttons
        if config['serialRFID']['button']:
            GPIO.setup(config['serialRFID']['button'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(config['serialRFID']['button'], GPIO.RISING, bouncetime=200)
            GPIO.add_event_callback(config['serialRFID']['button'], self.eventDetected)




