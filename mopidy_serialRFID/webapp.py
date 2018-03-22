from __future__ import absolute_import, unicode_literals
import logging
import os
import csv
import tornado.web
import json

from .rfidReader import RFIDReader


from mopidy import ext

logger = logging.getLogger(__name__)

class CSVTable(tornado.web.RequestHandler):
    def initialize(self, config, core):
        self.core = core

    def get(self):
        path = os.path.dirname(__file__)
        
        if not os.path.isfile(path+'/cardList.csv'):  
            open(path + '/cardList.csv', 'a').close()
        
        self.content_type = 'application/json'
        
        with open(path + '/cardList.csv', mode='r') as infile:
            reader = csv.reader(infile)
            cardList = []
            for row in reader: # each row is a list
                cardList.append(row)
            infile.close()
            
        self.write(json.dumps(cardList))
        
    def post(self):
        path = os.path.dirname(__file__)
        
        if not os.path.isfile(path+'/cardList.csv'):  
            open(path + '/cardList.csv', 'a').close()
        
        self.content_type = 'application/json'
  
        card=self.get_argument('rfidTag')
        playlist=self.get_argument('playlist')
        exists = False
        index=0
        
        with open(path + '/cardList.csv', mode='r') as infile:
            reader = csv.reader(infile)
            cardList = []
            for row in reader: # each row is a list
                cardList.append(row)
                if row[0] == card:
                    exists=True
                    index = len(cardList)-1
            infile.close()
            
            
        if exists:
            logger.info('card exists, updating entry')
            cardList[index][0] = card
            cardList[index][1] = playlist
            with open(path + '/cardList.csv', mode='wb') as infile:
                writer = csv.writer(infile)
                writer.writerows(cardList)
                infile.close()
            
        else:
            with open(path + '/cardList.csv', mode='a') as infile:
                infile.write(card+','+playlist)
                infile.close()
            

class RFIDManager(tornado.web.RequestHandler):
    def initialize(self, config, core):
        self.core = core
        self.deviceName = config['serialRFID']['device']
        self.rate = config['serialRFID']['rate']
        self.rfidReader = RFIDReader(self.deviceName, self.rate)

    def get(self):
        card = self.rfidReader.readCard()
        logger.info(card)
        self.write(card)



