import sys
from PySide import QtGui
import ui.gui
import CHDKPtp
import os
import domecontroller

import time

import logging

import lpgen

class RTICapApp:
    '''
    This will be the top level object for our application, it will start everything and handle any app specific stuff
    '''
    
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format="%(module)s - %(funcName)s - %(levelname)s - %(message)s", stream=sys.stdout)
        
        # setup the model
        rticapmodel = RTICapModel()
        
        # setup the gui
        self.gui = ui.gui.RTICapGUI(rticapmodel)
        
        # start the gui
        sys.exit(self.gui.startGUI())


class RTICapModel:
    """
    The model for RTICap, should contain anything to do with accessing data, the camera, etc, but nothing to do with presentation
    """

    #######
    #######    REMEMBER TO LOCK AUTOFOCUS!!!
    #######
    
    totalCapCount = 64
    
    def __init__(self):
        #self.cam = GCamCapture.GCamCapture()
        #self.cam = CHDKPtp.CHDKPtpCapture()
        #self.domeController = domecontroller.DomeController()
        self.cam = None
        self.domeController = None
        
    def connectedAndReady(self):
        if (self.cam != None and self.domeController != None):
            return True
        else:
            return False
        
    def connectCamera(self):
        try:
            self.cam = CHDKPtp.CHDKPtpCapture()
            self.cam.connect()
            return True
        except:
            self.cam = None
            return False
        
    def connectLighting(self):
        try:
            self.domeController = domecontroller.DomeController()
            return True
        except:
            self.domeController = None
            return False
    
    def activateAllLights(self):
        self.domeController.activateAllLEDs()
        
    def deactivateAllLights(self):
        self.domeController.resetSequenceClearLEDs()
        
    def activateSingleLight(self, lightIndex):
        logging.debug("activating light index " + str(lightIndex))
        self.domeController.activateLED(lightIndex)
    
    def getNewPreviewImage(self):
        #domeControl = domecontroller.DomeController()
        #domeControl = self.domeController
        #domeControl.activateAllLEDs()
        time.sleep(0.5) # allow camera to adjust to lighting
        if isinstance(self.cam, GCamCapture.GCamCapture):
            (camfolder, camfilename) = self.cam.capture()
            self.cam.save_from_cam(camfolder, camfilename, "temp.jpg")
            self.cam.delete_from_cam(camfolder, camfilename)
        elif isinstance(self.cam, CHDKPtp.CHDKPtpCapture):
            self.cam.activateShootingMode()
            self.cam.disableFlash()
            objectid = self.cam.capture()
            self.cam.downloadAndSaveObject(objectid, "temp.jpg")
            self.cam.deleteObject(objectid)
        else:
            raise Exception("self.cam is not an instance of a recognised class")
        pixmap = QtGui.QPixmap("temp.jpg")
        #domeControl.resetSequenceClearLEDs()
        return pixmap
        
    def doCaptureSequence(self, savePath, downloadAfter=True, baseLPFilePath=None, autofocus=True, captureUpdateCallback=None, downloadUpdateCallback=None):
        """captureUpdateCallback(capNo, totalCaps)
        downloadUpdateCallback(capNo, totalCaps, savePath)"""
        # find path that does not exist
        testno = 0
        pathprefix = os.path.join(savePath, "capture")
        cappath = pathprefix + str(testno)
        while os.path.exists(cappath):
            testno += 1
            cappath = pathprefix + str(testno)
        
        # we have found one that does not exist
        os.mkdir(cappath)
        
        #domeControl = domecontroller.DomeController()
        domeControl = self.domeController
        domeControl.resetSequenceClearLEDs()
        
        # for now autofocus now TODO: Add this to the ui so we can lock focus beforehand
        domeControl.activateAllLEDs()
        logging.debug("activateAllLEDs")
        if autofocus:
            self.cam.unlockAutofocus()
            logging.debug("unlockAutofocus")
            self.cam.autofocus()
            logging.debug("autofocus")
            self.cam.lockAutofocus()
            logging.debug("lockAutofocus")
        domeControl.resetSequenceClearLEDs()
        self.cam.disableFlash()
        caps = []
        total = self.totalCapCount
        for capno in range(1,total+1):
            domeControl.nextLED()
            imgpath = os.path.join(cappath, str(capno) + ".jpg")
            logging.debug("IMAGEPATH" + str(imgpath))           
            if isinstance(self.cam, GCamCapture.GCamCapture):
                (camfolder, camfilename) = self.cam.capture()
                captureUpdateCallback(capno, total)
                self.cam.save_from_cam(camfolder, camfilename, imgpath);
                self.cam.delete_from_cam(camfolder, camfilename)
                downloadUpdateCallback(capno, total, imgpath)
            elif isinstance(self.cam, CHDKPtp.CHDKPtpCapture):
                objectid = self.cam.capture()
                if captureUpdateCallback != None:
                    captureUpdateCallback(capno, total)
                if downloadAfter:
                    caps.append((objectid, imgpath))
                else:
                    self.cam.downloadAndSaveObject(objectid, imgpath)
                    self.cam.deleteObject(objectid)
                    downloadUpdateCallback(capno, total, imgpath)
            else:
                raise Exception("self.cam is not an instance of a recognised class")
            
                
            #yield (imgpath, total)
        
        domeControl.resetSequenceClearLEDs()
        #self.cam.unlockAutofocus()
        
        if downloadAfter:
            i = 1
            for capobjectid, capimgpath in caps:
                logging.debug("downloading object " + str(capobjectid) + " to " + capimgpath)
                self.cam.downloadAndSaveObject(capobjectid, capimgpath)
                self.cam.deleteObject(capobjectid)
                logging.debug("object " + str(capobjectid) + " download done")
                downloadUpdateCallback(i, total, capimgpath)
                i += 1
            logging.debug("all downloads done")
            
        logging.debug("capture sequence finished")
        
        if baseLPFilePath != None:
            logging.debug("generating lp file")
            lpOutputPath = os.path.join(cappath, "lights.lp")
            imagePaths = [imgp for objectid, imgp in caps] # list comprehension to generate a list of image paths from caps
            lpgen.generateLPFile(baseLPFilePath, imagePaths, lpOutputPath)
            logging.debug("lp file generated at " + lpOutputPath)
        
    def getTotalCapCount(self):
        return self.totalCapCount;
    
    def getAutofocusLocked(self):
        try:
            return self.cam.getAutofocusLocked()
        except AttributeError:
            return False
    
    def unlockAutofocus(self):
        logging.debug("unlockAutofocus()")
        self.cam.unlockAutofocus()
        
    def lockAutofocus(self):
        logging.debug("lockAutofocus()")
        self.cam.lockAutofocus()
        
    def autofocus(self):
        self.cam.unlockAutofocus()
        logging.debug("autofocus()")
        self.cam.autofocus()  
        self.cam.lockAutofocus()
        
if __name__ == "__main__":
    rticapapp = RTICapApp()
