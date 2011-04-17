'''
domecontroller - module to control the minirti dome

@author: Michael Hodgson
'''

import serial
import time
import logging

class DomeController:
    def __init__(self):
        self.currentLED = 0
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        # if we try to send data before this delay bytes get lost for some reason
        time.sleep(1.5) 
        
    def activateLED(self, ledIndex):
        """Activate the single LED given by the ledIndex, NB: The index starts at 0
        ie first LED = 0"""
        if ledIndex >= 64:
            raise Exception("LED index out of bounds")
        seg = ledIndex // 8
        bitPos = ledIndex % 8
        ledData = []
        for iSeg in range(8):
            byteString = ''
            for iLed in range(8):
                #if iSeg == seg and iLed == bitPos:
                if iLed == bitPos and iSeg == seg:
                    byteString += '1'
                else:
                    byteString += '0'
            ledData.append(chr(int(byteString, 2)))
        self.sendLEDData(ledData)

    def nextLED(self):
        #time.sleep(0.5)
        self.activateLED(self.currentLED)
        self.currentLED += 1
        if self.currentLED >= 64:
            self.currentLED = 0

    def resetSequenceClearLEDs(self):
        self.currentLED = 0
        ledData = []
        for i in range(8):
            ledData.append(chr(int('0x00', 16)))
        self.sendLEDData(ledData)
            
    def activateAllLEDs(self):
        self.currentLED = 0
        ledData = []
        for i in range(8):
            ledData.append(chr(int('0xFF', 16)))
        self.sendLEDData(ledData)
           
    
    def sendLEDData(self, data):
        ser = self.ser
        ser.flushInput()
        if len(data) != 8:
            raise Exception("LED Data not correct length")
        #time.sleep(1.5)
        #ser.flush()
        ser.write(chr(int('0x42', 16)))
        #ser.flush()
        for d in data:
            #time.sleep(2)
            ser.write(d)
            #ser.flush()
        logging.debug("awaiting response...")
        while ser.read(1) != chr(int('0x01', 16)):
            pass
        logging.debug("response received")  

    def close(self):
        self.ser.close()
        
if __name__ == '__main__':
    dc = DomeController()
    while True:
        dc.nextLED()