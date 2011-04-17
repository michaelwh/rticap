'''
Created on 12 Mar 2011

@author: Michael Hodgson
'''
import ptp
from ptp.PtpUsbTransport import PtpUsbTransport
from ptp.PtpAbstractTransport import PtpRequest
from ptp.PtpSession import PtpSession, PtpException
from ptp import PtpValues
import time
import logging

class CHDKPtpValues(object):
    """Values related to the CHDK PTP interface, taken from the core/ptp.h file"""
    CHDKOpcode = 0x9999
    
    class Commands(object):
        ExecuteScript = 7
        ScriptStatus = 8
    
    class ScriptingLanguage(object):
        LUA = 0
        UBASIC = 1
    
    class ResponseCodes(object):
        OK = 0x2001
        GeneralError = 0x2002
        ParameterNotSupported = 0x2006
        InvalidParameter = 0x201D
        
    class ScriptStatus(object): # flags
        RUN = 0x1
        MSG = 0x2
    
def executeScript(ptpSession, script, language=CHDKPtpValues.ScriptingLanguage.LUA, wait=False):
    """Attempts to execute the given script on the camera
        params:
            ptpSession - ptp session created using pyptp
            script - string containing the script to be executed on the camera
            language - the scripting language of the script, can be either LUA or UBASIC, values for this param are found in
                        CHDKPtpValues.ScriptingLanguage
            wait - if wait is true the function will not return until the script has stopped running"""
    scriptraw = unicode(script)
    scriptraw += u'\u0000'
    script_ptp_request = PtpRequest(CHDKPtpValues.CHDKOpcode, ptpSession.sessionid, ptpSession.NewTransaction(), params=(CHDKPtpValues.Commands.ExecuteScript,language))
    ptpSession.transport.send_ptp_request(script_ptp_request)
    ptpSession.transport.send_ptp_data(script_ptp_request, scriptraw)
    retryFlag = True
    # retry until we get the response, otherwise get_ptp_response times out due to long script 
    # and causes incorrect response to be sent next time & the program gets confused
    while retryFlag:
        try:
            script_ptp_response = ptpSession.transport.get_ptp_response(script_ptp_request)
            retryFlag = False
        except:
            pass
    if script_ptp_response.respcode != CHDKPtpValues.ResponseCodes.OK:
        raise Exception("CHDK PTP Response Code indicates something is wrong, Response Code: " + str(script_ptp_response.respcode))
    if wait:
        waitForScriptFinish(ptpSession)
        
def getScriptStatus(ptpSession):
    """Returns tuple of two booleans (scriptrunning, msgwaiting)"""
    sstatus_ptp_request = PtpRequest(CHDKPtpValues.CHDKOpcode, ptpSession.sessionid, ptpSession.NewTransaction(), params=(CHDKPtpValues.Commands.ScriptStatus,))
    ptpSession.transport.send_ptp_request(sstatus_ptp_request)
    retryFlag = True
    # retry until we get the response, otherwise get_ptp_response times out due to long script 
    # and causes incorrect response to be sent next time & the program gets confused
    while retryFlag:
        try:
            sstatus_ptp_response = ptpSession.transport.get_ptp_response(sstatus_ptp_request)
            retryFlag = False
        except:
            pass
    if sstatus_ptp_response.respcode != CHDKPtpValues.ResponseCodes.OK:
        raise Exception("CHDK PTP Response Code indicates something is wrong, Response Code: " + str(sstatus_ptp_response.respcode))
    
    scriptrunning = False
    msgwaiting = False
    if sstatus_ptp_response.params[0] & CHDKPtpValues.ScriptStatus.RUN:
        scriptrunning = True
    if sstatus_ptp_response.params[0] & CHDKPtpValues.ScriptStatus.MSG:
        msgwaiting = True
    return (scriptrunning, msgwaiting)

def waitForScriptFinish(ptpSession):
    # wait until the script finishes
    scriptrunning = True
    while scriptrunning == True:
        #logging.debug("requesting scriptstatus")
        (scriptrunning, msgwaiting) = getScriptStatus(ptpSession)
        time.sleep(0.25)


class CHDKPtpCapture:
    def __init__(self):
        self.autofocuslocked = False
    
    def connect(self):
        """Connects to the first available ptp device, ptpSession is used to access most ptp commands"""
        ptps = PtpUsbTransport.findptps()
        print ptps
        self.ptpTransport = PtpUsbTransport(ptps[0])
        self.ptpSession = PtpSession(self.ptpTransport)

        self.vendorId = PtpValues.Vendors.STANDARD
        self.ptpSession.OpenSession()
        
        self.deviceInfo = self.ptpSession.GetDeviceInfo()
        print "ser: " + self.deviceInfo.SerialNumber
        self.vendorId = self.deviceInfo.VendorExtensionID
        print "model: " + self.deviceInfo.Model
        
        return True
        
    def capture(self):
        """Captures an image and returns it's objectid"""
        self.activateShootingMode()
        lua_script = "shoot()"
        logging.debug("sending script")
        executeScript(self.ptpSession, lua_script, CHDKPtpValues.ScriptingLanguage.LUA, wait=True)
        logging.debug("script finished")
        # below couple of lines in while loop taken from Capture.py of pyptp
        objectid = None
        while True:
            evt = self.ptpSession.CheckForEvent(None)
            if evt == None:
                raise Exception("Capture did not complete")
            if evt.eventcode == PtpValues.StandardEvents.OBJECT_ADDED:
                objectid = evt.params[0]
                break
        return objectid
        
    def activateShootingMode(self):
        """Activates shooting mode on the camera, allowing the camera to shoot while under usb control"""
        lua_script = """
        switch_mode_usb(1)
        rec,vid,mode=get_mode()
        while rec == false do
            rec,vid,mode=get_mode()
        end
        """
        executeScript(self.ptpSession, lua_script, CHDKPtpValues.ScriptingLanguage.LUA, wait=True)
         
    
    def disableFlash(self):
        self.activateShootingMode()
        lua_script = "set_prop(143,2) -- turns flash off on SX200IS"
        executeScript(self.ptpSession, lua_script, CHDKPtpValues.ScriptingLanguage.LUA, wait=True)
    
    def enableAutoFlash(self):
        self.activateShootingMode()
        lua_script = "set_prop(143,1) -- turns flash to auto on SX200IS"
        executeScript(self.ptpSession, lua_script, CHDKPtpValues.ScriptingLanguage.LUA, wait=True)
        
    def lockAutofocus(self):
        """Prevents the camera from autofocusing"""
        self.activateShootingMode()
        lua_script = "set_aflock(1)"
        executeScript(self.ptpSession, lua_script, CHDKPtpValues.ScriptingLanguage.LUA, wait=True)
        self.autofocuslocked = True
    
    def unlockAutofocus(self):
        """Allows the camera to autofocus"""
        self.activateShootingMode()
        lua_script = "set_aflock(0)"
        executeScript(self.ptpSession, lua_script, CHDKPtpValues.ScriptingLanguage.LUA, wait=True)
        self.autofocuslocked = False
        
    def autofocus(self):
        """Attempts to autofocus the camera"""
        self.activateShootingMode()
        lua_script = "press('shoot_half')"
        executeScript(self.ptpSession, lua_script, CHDKPtpValues.ScriptingLanguage.LUA, wait=True)
        time.sleep(2) # we must wait for a short time for the autofocus to complete, otherwise if we lockAutofocus right afterwards we can cause the program to lock up
    
    def downloadAndSaveObject(self, objectid, savepath):
        file = open(savepath, "w")
        self.ptpSession.GetObject(objectid, file)
        file.close()
    
    def deleteObject(self, objectid):
        self.ptpSession.DeleteObject(objectid)
        
    def getAutofocusLocked(self):
        return self.autofocuslocked
        
    #def close(self):
    #    del ptpSession
    #    del ptpTransport
