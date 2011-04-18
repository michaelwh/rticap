# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'captureConfig.ui'
#
# Created: Mon Apr 18 20:13:49 2011
#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_CaptureConfig(object):
    def setupUi(self, CaptureConfig):
        CaptureConfig.setObjectName("CaptureConfig")
        CaptureConfig.resize(738, 161)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CaptureConfig.sizePolicy().hasHeightForWidth())
        CaptureConfig.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(CaptureConfig)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(CaptureConfig)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.saveDirectoryLineEdit = QtGui.QLineEdit(CaptureConfig)
        self.saveDirectoryLineEdit.setObjectName("saveDirectoryLineEdit")
        self.gridLayout.addWidget(self.saveDirectoryLineEdit, 0, 1, 1, 1)
        self.beginCaptureButton = QtGui.QPushButton(CaptureConfig)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.beginCaptureButton.sizePolicy().hasHeightForWidth())
        self.beginCaptureButton.setSizePolicy(sizePolicy)
        self.beginCaptureButton.setObjectName("beginCaptureButton")
        self.gridLayout.addWidget(self.beginCaptureButton, 2, 0, 1, 3)
        self.chooseDirectoryButton = QtGui.QPushButton(CaptureConfig)
        self.chooseDirectoryButton.setObjectName("chooseDirectoryButton")
        self.gridLayout.addWidget(self.chooseDirectoryButton, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.autofocusGroupBox = QtGui.QGroupBox(CaptureConfig)
        self.autofocusGroupBox.setFlat(False)
        self.autofocusGroupBox.setCheckable(True)
        self.autofocusGroupBox.setChecked(False)
        self.autofocusGroupBox.setObjectName("autofocusGroupBox")
        self.gridLayout.addWidget(self.autofocusGroupBox, 1, 0, 1, 1)

        self.retranslateUi(CaptureConfig)
        QtCore.QMetaObject.connectSlotsByName(CaptureConfig)

    def retranslateUi(self, CaptureConfig):
        CaptureConfig.setWindowTitle(QtGui.QApplication.translate("CaptureConfig", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CaptureConfig", "Save Directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.beginCaptureButton.setText(QtGui.QApplication.translate("CaptureConfig", "Begin Capture", None, QtGui.QApplication.UnicodeUTF8))
        self.chooseDirectoryButton.setText(QtGui.QApplication.translate("CaptureConfig", "Choose Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.autofocusGroupBox.setTitle(QtGui.QApplication.translate("CaptureConfig", "Attempt Autofocus", None, QtGui.QApplication.UnicodeUTF8))

