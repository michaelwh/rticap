# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'captureConfig.ui'
#
# Created: Wed Mar 23 19:37:31 2011
#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_CaptureConfig(object):
    def setupUi(self, CaptureConfig):
        CaptureConfig.setObjectName("CaptureConfig")
        CaptureConfig.resize(738, 193)
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
        self.gridLayout.addWidget(self.beginCaptureButton, 4, 0, 1, 3)
        self.chooseDirectoryButton = QtGui.QPushButton(CaptureConfig)
        self.chooseDirectoryButton.setObjectName("chooseDirectoryButton")
        self.gridLayout.addWidget(self.chooseDirectoryButton, 0, 2, 1, 1)
        self.generateLPFileGroupBox = QtGui.QGroupBox(CaptureConfig)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generateLPFileGroupBox.sizePolicy().hasHeightForWidth())
        self.generateLPFileGroupBox.setSizePolicy(sizePolicy)
        self.generateLPFileGroupBox.setFlat(False)
        self.generateLPFileGroupBox.setCheckable(True)
        self.generateLPFileGroupBox.setChecked(False)
        self.generateLPFileGroupBox.setObjectName("generateLPFileGroupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.generateLPFileGroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.baseLPFileLineEdit = QtGui.QLineEdit(self.generateLPFileGroupBox)
        self.baseLPFileLineEdit.setObjectName("baseLPFileLineEdit")
        self.gridLayout_2.addWidget(self.baseLPFileLineEdit, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.generateLPFileGroupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.baseLPFileBrowseButton = QtGui.QPushButton(self.generateLPFileGroupBox)
        self.baseLPFileBrowseButton.setObjectName("baseLPFileBrowseButton")
        self.gridLayout_2.addWidget(self.baseLPFileBrowseButton, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.generateLPFileGroupBox, 2, 0, 2, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
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
        self.generateLPFileGroupBox.setTitle(QtGui.QApplication.translate("CaptureConfig", "Generate LP File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CaptureConfig", "Base LP File:", None, QtGui.QApplication.UnicodeUTF8))
        self.baseLPFileBrowseButton.setText(QtGui.QApplication.translate("CaptureConfig", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.autofocusGroupBox.setTitle(QtGui.QApplication.translate("CaptureConfig", "Attempt Autofocus", None, QtGui.QApplication.UnicodeUTF8))

