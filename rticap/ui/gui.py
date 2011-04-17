import sys
from PySide import QtGui, QtCore

import pysideutil

from mainwindow import Ui_MainWindow
from capturePreview import Ui_capturePreview
from captureConfig import Ui_CaptureConfig
from captureSequence import Ui_CaptureSequence
from topMenu import Ui_topMenu
from connect import Ui_connect
import appconfig

class RTICapGUI:

    def __init__(self, rticapmodel):
      
        self.rticapmodel = rticapmodel
        self.qtapp = QtGui.QApplication(sys.argv)
        
        self.capPrev = CapturePreviewGUIMode(self.rticapmodel)
        #self.capPrev.setCaptureCallback(self._newPreviewImageCallback) # TODO: pass model into the CapturePreviewGUI so we don't need this
        self.capConfig = CaptureConfigGUIMode(self.rticapmodel, self.qtapp)
        #self.capConfig.setDoCaptureCallback(self._doCaptureCallback) 
        self.connect = ConnectGUIMode(self.rticapmodel, self)
               
        self.guiModes = [self.connect, self.capPrev, self.capConfig]
        
        self.mainwin = MainWindow(self.guiModes)
        self.mainwin.show()
        

        self.topMenu = TopMenuWidget(self.guiModes, self.setCurrentGUIMode)
        self.mainwin.setTopMenuWidget(self.topMenu)
        
        self.checkReady()
        self.setCurrentGUIMode(self.connect)
    
    def startGUI(self):
        return self.qtapp.exec_()
    
    def setCurrentGUIMode(self, guiMode):
        self.mainwin.setCurrentGUIMode(guiMode)
        self.topMenu.setCurrentGUIMode(guiMode)
        
    def checkReady(self):
        if self.rticapmodel.connectedAndReady():
            self.topMenu.setGUIModeEnabled(self.capPrev, True)
            self.topMenu.setGUIModeEnabled(self.capConfig, True)
        else:
            self.topMenu.setGUIModeEnabled(self.capPrev, False)
            self.topMenu.setGUIModeEnabled(self.capConfig, False)

class CapturePreviewGUIMode:
    
    def __init__(self, rticapmodel):
        self.rticapmodel = rticapmodel
        lights = [str(i) for i in range(self.rticapmodel.getTotalCapCount())]
        lights.insert(0, "None")
        self.capturePreviewWidget = CapturePreviewWidget(lights=lights)
        self.capturePreviewWidget.setCaptureCallback(self.doNewPreviewCapture)
        self.capturePreviewWidget.setActivateAllLightsCallback(self.rticapmodel.activateAllLights)
        self.capturePreviewWidget.setDeactivateAllLightsCallback(self.rticapmodel.deactivateAllLights)
        self.capturePreviewWidget.setActivateSingleLightIndexChangedCallback(self._activateSingleLightIndexChangedCallback)
        self.capturePreviewWidget.setUnlockAutofocusCallback(self._unlockAutofocusCallback)
        self.capturePreviewWidget.setAutofocusCallback(self._autofocusCallback)
        self.updateAutofocusStatus()
            
    def getWidget(self):
        return self.capturePreviewWidget

    def getModeName(self):
        return "Capture Preview"
    
    def doNewPreviewCapture(self):
        pixmap = self.rticapmodel.getNewPreviewImage()
        self.capturePreviewWidget.setPreviewImage(pixmap)
        
    def _activateSingleLightIndexChangedCallback(self):
        """Callback for when the index of the single light combo box is changed so we must activate the light it corresponds to"""
        lightIndex = self.capturePreviewWidget.getSingleLightCurrentIndex()
        if lightIndex == 0:
            self.rticapmodel.deactivateAllLights()
        else:
            self.rticapmodel.activateSingleLight(lightIndex - 1)
    
    def updateAutofocusStatus(self):
        self.capturePreviewWidget.setAutofocusLockStatus(self.rticapmodel.getAutofocusLocked())
        
    
    def _unlockAutofocusCallback(self):
        self.rticapmodel.unlockAutofocus()
        self.updateAutofocusStatus()
    
    def _autofocusCallback(self):
        self.rticapmodel.autofocus()
        self.updateAutofocusStatus()          
    
class CaptureConfigGUIMode:
    # TODO: Use event system to notify when eg appConfig changes so all classes can reload it and so update it
    configPath = 'config/CaptureConfig.pkl'
    def __init__(self, rticapmodel, qtapp):
        self.qtapp = qtapp
        self.rticapmodel = rticapmodel
        self.stackedLayout = QtGui.QStackedLayout()
        self.stackedWidget = QtGui.QWidget() # this widget will hold stackedLayout
        self.stackedWidget.setLayout(self.stackedLayout)
        self.captureConfigWidget = CaptureConfigWidget()
        self.captureConfigWidget.setDoCaptureCallback(self.doCaptureSequence)
        self.captureSequenceWidget = CaptureSequenceWidget()
        self.stackedLayout.addWidget(self.captureConfigWidget)
        self.stackedLayout.addWidget(self.captureSequenceWidget)
        self.stackedLayout.setCurrentWidget(self.captureConfigWidget)
        
        self.config = appconfig.AppConfig(self.configPath)
        
        if self.config.getValue('ImageSavePath') != None:
            self.captureConfigWidget.setSaveDir(self.config.getValue('ImageSavePath'))
            print self.config.getValue('ImageSavePath')
    
    def getWidget(self):
        return self.stackedWidget
    
    def getModeName(self):
        return "Capture Configuration"
    
    def doCaptureSequence(self):
        saveDir = self.captureConfigWidget.getSaveDir()
        autofocus = self.captureConfigWidget.getAttemptAutofocus()
        if self.captureConfigWidget.getLPGenSelected():
            baseLPFilePath = self.captureConfigWidget.getBaseLPFilePath()#
        else:
            baseLPFilePath = None
        self.config.setValue('ImageSavePath', saveDir)
        self.stackedLayout.setCurrentWidget(self.captureSequenceWidget) # switch to capture sequence
        currcapno = 1
        self.rticapmodel.doCaptureSequence(saveDir, baseLPFilePath=baseLPFilePath, autofocus=autofocus, captureUpdateCallback=self._captureUpdateCallback, downloadUpdateCallback=self._downloadUpdateCallback)
        
        self.stackedLayout.setCurrentWidget(self.captureConfigWidget) # switch back to capture config

    def _captureUpdateCallback(self, capNo, totalCaps):
        self.captureSequenceWidget.setCaptureSize(totalCaps)
        self.captureSequenceWidget.setCurrentCaptureNumber(capNo)
        self.qtapp.processEvents()
    
    def _downloadUpdateCallback(self, capNo, totalCaps, savePath):
        self.captureSequenceWidget.setCaptureSize(totalCaps)
        self.captureSequenceWidget.setCurrentDownloadNumber(capNo, savePath)
        self.qtapp.processEvents()

class ConnectGUIMode:
    
    def __init__(self, rticapmodel, rticapgui):
        self.rticapmodel = rticapmodel
        self.rticapgui = rticapgui
        self.connectWidget = ConnectWidget()
        self.connectWidget.setAutoconnectToCameraCallback(self.autoconnectToCameraCallback)
        self.connectWidget.setConnectToLightingCallback(self.connectToLightingCallback)
            
    def getWidget(self):
        return self.connectWidget

    def getModeName(self):
        return "Connections"
    
    def autoconnectToCameraCallback(self):
        connected = self.rticapmodel.connectCamera()
        self.connectWidget.setCameraStatus(connected)
        self.rticapgui.checkReady()
            
    def connectToLightingCallback(self):
        connected = self.rticapmodel.connectLighting()
        self.connectWidget.setLightingStatus(connected)
        self.rticapgui.checkReady()
    
class MainWindow(QtGui.QMainWindow):
    def __init__(self, guiModes, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.guiModes = guiModes
        self.stackedLayout = QtGui.QStackedLayout()
        for guiMode in self.guiModes:
            self.stackedLayout.addWidget(guiMode.getWidget())
        self.ui.centralscroll.setLayout(self.stackedLayout)
        
    def setCurrentGUIMode(self, guiMode):
        self.stackedLayout.setCurrentIndex(self.guiModes.index(guiMode))
        
    def setTopMenuWidget(self, topMenu):
        self.topFrameLayout = QtGui.QVBoxLayout()
        self.topFrameLayout.addWidget(topMenu)
        self.ui.topFrame.setLayout(self.topFrameLayout)
        
class CapturePreviewWidget(QtGui.QWidget):
    def __init__(self, parent=None, lights=[]):
        super(CapturePreviewWidget, self).__init__(parent)
        self.ui = Ui_capturePreview()
        self.ui.setupUi(self)
        # make and add the graphics scene to siplay the preview image
        self.previewGraphicsScene = QtGui.QGraphicsScene()
        self.ui.previewGraphicsView.setScene(self.previewGraphicsScene)
        self.ui.previewGraphicsView.scale(0.35, 0.35)
        if len(lights) > 0:
            self.ui.activateSingleLightComboBox.addItems(lights)
        else:
            self.ui.activateSingleLightComboBox.setEnabled(False)
            
    def setAutofocusLockStatus(self, locked):
        if locked:
            self.ui.autofocusLockStatusLabel.setText("Autofocus Locked")
        else:
            self.ui.autofocusLockStatusLabel.setText("Autofocus Not Locked")
    
    def setPreviewImage(self, pixmap):
        gitems = self.previewGraphicsScene.items()
        for gitem in gitems:
            self.previewGraphicsScene.removeItem(gitem)
        self.previewGraphicsScene.addPixmap(pixmap)
        self.previewGraphicsScene.setSceneRect(0,0,pixmap.width(),pixmap.height())
    
    def setCaptureCallback(self, capturecallback):
        ''' sets the callback which will inform the app that a new image is wanted 
        capturecallback should be of form func() '''
        self.ui.newCaptureButton.clicked.connect(capturecallback)
                
    def setUnlockAutofocusCallback(self, callback):
        self.ui.unlockAutofocusButton.clicked.connect(callback)
        
    def setAutofocusCallback(self, callback):
        self.ui.lockAutofocusButton.clicked.connect(callback)
        
    def setActivateAllLightsCallback(self, activateAllLightsCallback):
        self.ui.activateAllLightsButton.clicked.connect(activateAllLightsCallback)
    
    def setDeactivateAllLightsCallback(self, deactivateAllLightsCallback):
        self.ui.deactivateAllLightsButton.clicked.connect(deactivateAllLightsCallback)
        
    def setActivateSingleLightIndexChangedCallback(self, activateSingleLightIndexChangedCallback):
        self.ui.activateSingleLightComboBox.currentIndexChanged.connect(activateSingleLightIndexChangedCallback)
    
    def getSingleLightCurrentIndex(self):
        return self.ui.activateSingleLightComboBox.currentIndex()
        
class CaptureConfigWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CaptureConfigWidget, self).__init__(parent)
        self.ui = Ui_CaptureConfig()
        self.ui.setupUi(self)
        self.ui.chooseDirectoryButton.clicked.connect(self._chooseDirCallback)
        self.ui.baseLPFileBrowseButton.clicked.connect(self._baseLPFileBrowseCallback)
    
    def setDoCaptureCallback(self, callback):
        self.ui.beginCaptureButton.clicked.connect(callback)
        
    def setSaveDir(self, chooseDir):
        self.ui.saveDirectoryLineEdit.setText(chooseDir)
    
    def _chooseDirCallback(self):
        self.ui.saveDirectoryLineEdit.setText(QtGui.QFileDialog.getExistingDirectory(self, "Open Save Directory"))
        
    def getSaveDir(self):
        return self.ui.saveDirectoryLineEdit.text()
    
    def _baseLPFileBrowseCallback(self):
        self.ui.baseLPFileLineEdit.setText(QtGui.QFileDialog.getOpenFileName(self, "Select Base LP File"))
    
    def getLPGenSelected(self):
        return self.ui.generateLPFileGroupBox.isChecked()
    
    def getBaseLPFilePath(self):
        return self.ui.baseLPFileLineEdit.text()
    
    def getAttemptAutofocus(self):
        return self.ui.autofocusGroupBox.isChecked()
        
class CaptureSequenceWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CaptureSequenceWidget, self).__init__(parent)
        self.ui = Ui_CaptureSequence()
        self.ui.setupUi(self)
        self.viewImageScene = QtGui.QGraphicsScene()
        self.ui.viewImageGraphicsView.setScene(self.viewImageScene)
        self.ui.viewImageGraphicsView.scale(0.35, 0.35)
        
    def setCaptureSize(self, max):
        self.capSize = max
    
    def setCurrentCaptureNumber(self, currentNo):
        dspTxt = "Done capture: " + str(currentNo) + " of " + str(self.capSize)
        self.ui.captureProgressLabel.setText(dspTxt)
        
    def setCurrentDownloadNumber(self, currentNo, saveFilePath):
        dspTxt = "\nDownloaded capture " + str(currentNo) + " to: " + saveFilePath
        self.ui.captureProgressLabel.setText(dspTxt)
        self.setViewImage(QtGui.QPixmap(saveFilePath))
    
    def setDisplayTest(self, text):
        self.ui.captureProgressLabel.setText(text)    
    
    def setViewImage(self, pixmap):
        gitems = self.viewImageScene.items()
        for gitem in gitems:
            self.viewImageScene.removeItem(gitem)
        self.viewImageScene.addPixmap(pixmap)
        self.viewImageScene.setSceneRect(0,0,pixmap.width(),pixmap.height())
        
class TopMenuWidget(QtGui.QWidget):
    def __init__(self, guiModes, currentModeChangedCallback, parent=None):
        super(TopMenuWidget, self).__init__(parent)
        self.ui = Ui_topMenu()
        self.ui.setupUi(self)
        #self.ui.configureCaptureButton.clicked.connect(self._configureCaptureButtonClicked)
        #self.ui.capturePreviewButton.clicked.connect(self._capturePreviewButtonClicked)
        self.currentModeChangedCallback = currentModeChangedCallback
        self.guiModes = guiModes
        self.guiModeButtons = []
        for guiMode in self.guiModes:
            modeButton = QtGui.QPushButton()
            modeButton.setText(guiMode.getModeName())
            modeButton.setCheckable(True)
            pysideutil.qtLink(modeButton, "clicked()", self.currentModeChangedCallback, guiMode)
            self.layout().addWidget(modeButton)
            self.guiModeButtons.append(modeButton)

    def setCurrentGUIMode(self, guiMode):
        guiModeIndex = self.guiModes.index(guiMode)
        i = 0
        for guiModeButton in self.guiModeButtons:
            if i == guiModeIndex:
                guiModeButton.setChecked(True)
            else:
                guiModeButton.setChecked(False)
            i += 1
            
    def setGUIModeEnabled(self, guiMode, enabled):
        guiModeIndex = self.guiModes.index(guiMode)
        i = 0
        for guiModeButton in self.guiModeButtons:
            if i == guiModeIndex:
                guiModeButton.setEnabled(enabled)
            i += 1
            
class ConnectWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ConnectWidget, self).__init__(parent)
        self.ui = Ui_connect()
        self.ui.setupUi(self)      
    
    def setLightingStatus(self, connected, message=None):
        lightingText = ""
        if connected:
            lightingText += "Connected successfully!"
        else:
            lightingText += "Connection falied!"
        
        if message != None:
            lightingText += "\n" + message
            
        self.ui.lightingMessageLabel.setText(lightingText)
    
    def setCameraStatus(self, connected, message=None):
        cameraText = ""
        if connected:
            cameraText += "Connected successfully!"
        else:
            cameraText += "Connection falied!"
        
        if message != None:
            cameraText += "\n" + message
            
        self.ui.cameraMessageLabel.setText(cameraText)
    
    def setConnectToLightingCallback(self, callback):
        self.ui.connectToLightingButton.clicked.connect(callback)
              
    def setAutoconnectToCameraCallback(self, callback):
        self.ui.autoconnectToCameraButton.clicked.connect(callback)