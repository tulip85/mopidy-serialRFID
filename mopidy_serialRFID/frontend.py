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


logger = logging.getLogger(__name__)


class RFIDThread(Thread):
    def __init__(self, device, core):
        Thread.__init__(self)
        self.dev = device
        #getList of cards
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.cardList = self.readList()
        self.lastCard = ''
        self.core = core

    def start(self):
        super(RFIDThread, self).start()
    
    def readCard(self):
        key = ''
        
        while key == '' or key == self.lastCard or len(key) < 12:
            ID = ""
            read_byte = self.dev.read()
            if read_byte=="\x02":
                for Counter in range(12):
                    read_byte=self.dev.read()
                    ID = ID + str(read_byte)
                key = ID
        self.lastCard = key
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
        time.sleep(5)

            
    def run(self):
        while True:
            try:
                self.card = self.readCard()
                logger.info('Read card '+self.card)
                self.plist = self.getPlaylist(self.card)
                logger.info('Playlist'+self.plist)
                if self.plist != '':
                    self.play(self.plist)
                time.sleep(5) 
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
            
    
                    
class serialRFID(pykka.ThreadingActor, core.CoreListener):
    
    def __init__(self, config, core):
        super(serialRFID, self).__init__()
        self.menu = False
        self.core = core
        self.config = config
        self.deviceName = config['serialRFID']['device']
        self.rate = config['serialRFID']['rate']
        #initialize device
        self.dev = serial.Serial(self.deviceName,self.rate)
        
        self.workerThread = RFIDThread(self.dev, self.core)
        self.workerThread.start()

   


