# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect.ui'
#
# Created: Mon Apr 18 20:13:49 2011
#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_connect(object):
    def setupUi(self, connect):
        connect.setObjectName("connect")
        connect.resize(879, 426)
        self.gridLayout = QtGui.QGridLayout(connect)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtGui.QGroupBox(connect)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.autoconnectToCameraButton = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autoconnectToCameraButton.sizePolicy().hasHeightForWidth())
        self.autoconnectToCameraButton.setSizePolicy(sizePolicy)
        self.autoconnectToCameraButton.setObjectName("autoconnectToCameraButton")
        self.gridLayout_3.addWidget(self.autoconnectToCameraButton, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 4, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 1, 1, 1)
        self.cameraMessageLabel = QtGui.QLabel(self.groupBox_2)
        self.cameraMessageLabel.setObjectName("cameraMessageLabel")
        self.gridLayout_3.addWidget(self.cameraMessageLabel, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(connect)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 4, 0, 1, 1)
        self.connectToLightingButton = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectToLightingButton.sizePolicy().hasHeightForWidth())
        self.connectToLightingButton.setSizePolicy(sizePolicy)
        self.connectToLightingButton.setObjectName("connectToLightingButton")
        self.gridLayout_2.addWidget(self.connectToLightingButton, 1, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 1, 1, 1)
        self.lightingMessageLabel = QtGui.QLabel(self.groupBox)
        self.lightingMessageLabel.setObjectName("lightingMessageLabel")
        self.gridLayout_2.addWidget(self.lightingMessageLabel, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(connect)
        QtCore.QMetaObject.connectSlotsByName(connect)

    def retranslateUi(self, connect):
        connect.setWindowTitle(QtGui.QApplication.translate("connect", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("connect", "Camera", None, QtGui.QApplication.UnicodeUTF8))
        self.autoconnectToCameraButton.setText(QtGui.QApplication.translate("connect", "Autoconnect to Camera", None, QtGui.QApplication.UnicodeUTF8))
        self.cameraMessageLabel.setText(QtGui.QApplication.translate("connect", "Not Connected", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("connect", "Lighting", None, QtGui.QApplication.UnicodeUTF8))
        self.connectToLightingButton.setText(QtGui.QApplication.translate("connect", "Connect to Lighting", None, QtGui.QApplication.UnicodeUTF8))
        self.lightingMessageLabel.setText(QtGui.QApplication.translate("connect", "Not Connected", None, QtGui.QApplication.UnicodeUTF8))

