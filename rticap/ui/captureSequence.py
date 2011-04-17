# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'captureSequence.ui'
#
# Created: Wed Mar 23 19:37:31 2011
#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_CaptureSequence(object):
    def setupUi(self, CaptureSequence):
        CaptureSequence.setObjectName("CaptureSequence")
        CaptureSequence.resize(808, 509)
        self.gridLayout = QtGui.QGridLayout(CaptureSequence)
        self.gridLayout.setObjectName("gridLayout")
        self.captureProgressLabel = QtGui.QLabel(CaptureSequence)
        self.captureProgressLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.captureProgressLabel.setObjectName("captureProgressLabel")
        self.gridLayout.addWidget(self.captureProgressLabel, 1, 0, 1, 1)
        self.viewImageGraphicsView = QtGui.QGraphicsView(CaptureSequence)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewImageGraphicsView.sizePolicy().hasHeightForWidth())
        self.viewImageGraphicsView.setSizePolicy(sizePolicy)
        self.viewImageGraphicsView.setObjectName("viewImageGraphicsView")
        self.gridLayout.addWidget(self.viewImageGraphicsView, 2, 0, 1, 1)

        self.retranslateUi(CaptureSequence)
        QtCore.QMetaObject.connectSlotsByName(CaptureSequence)

    def retranslateUi(self, CaptureSequence):
        CaptureSequence.setWindowTitle(QtGui.QApplication.translate("CaptureSequence", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.captureProgressLabel.setText(QtGui.QApplication.translate("CaptureSequence", "---", None, QtGui.QApplication.UnicodeUTF8))

