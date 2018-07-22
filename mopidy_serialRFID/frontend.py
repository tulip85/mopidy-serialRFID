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

from smbus import SMBus


from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1322, ssd1325, ssd1331, sh1106
from luma.core.virtual import viewport

from PIL import ImageFont, Image, ImageSequence


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
        
        if self.oledEnabled:
            self.set_image("detecting.gif")
            
            
        logger.info("reading rfid card")
        #initialize device
        self.dev = serial.Serial(self.deviceName,self.rate)
  
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.card = self.readCard()
        logger.info('Read card '+self.card)
        self.plist = self.getPlaylist(self.card)
        logger.info('Playlist'+self.plist)
        if self.plist != '':
            if self.oledEnabled:
                self.set_image("detected.gif")
            self.play(self.plist)
        else:
            if self.oledEnabled:
                self.set_image("error.gif")
        #close port
        self.dev.close()
                
    
    
    def __init__(self, config, core):
        super(serialRFID, self).__init__()
        self.menu = False
        self.core = core
        self.config = config
        self.deviceName = config['serialRFID']['device']
        self.rate = config['serialRFID']['rate']
        self.oledEnabled = config['serialRFID']['oled_enabled']
        #if screen is used 
        if self.oledEnabled:
            if config['serialRFID']['oled_bus'] and config['serialRFID']['oled_address']:
                self.serial = i2c(bus=SMBus(config['serialRFID']['oled_bus']), address=config['serialRFID']['oled_address'])
            self.driver = config['serialRFID']['oled_driver']
            if self.driver == 'ssd1306':
                self.device = ssd1306(self.serial)
            elif self.driver == 'ssd1322':
                self.device = ssd1322(self.serial)
            elif self.driver == 'ssd1325':
                self.device = ssd1325(self.serial)
            elif self.driver == 'ssd1331':    
                self.device = ssd1331(self.serial)
            elif self.driver == 'sh1106':
                self.device = sh1106(self.serial)
            else:
                self.device = ssd1306(self.serial)
        
        GPIO.setmode(GPIO.BOARD)
        
        #register buttons
        if config['serialRFID']['button']:
            GPIO.setup(config['serialRFID']['button'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(config['serialRFID']['button'], GPIO.RISING, bouncetime=600)
            GPIO.add_event_callback(config['serialRFID']['button'], self.eventDetected)

        if self.oledEnabled:
             self.set_image("radio.gif")

    def set_image(self, image):
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', image))
        imageLoaded = Image.open(img_path)
        size = [min(*self.device.size)] * 2
        posn = ((self.device.width - size[0]) // 2, self.device.height - size[1])
            
        background = Image.new(self.device.mode, self.device.size, "black")
        background.paste(imageLoaded.resize(size, resample=Image.LANCZOS), posn)
        self.device.display(background.convert(self.device.mode))
            



