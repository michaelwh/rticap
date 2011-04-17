# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'topMenu.ui'
#
# Created: Wed Mar 23 19:37:31 2011
#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_topMenu(object):
    def setupUi(self, topMenu):
        topMenu.setObjectName("topMenu")
        topMenu.resize(881, 78)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(topMenu.sizePolicy().hasHeightForWidth())
        topMenu.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(topMenu)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.retranslateUi(topMenu)
        QtCore.QMetaObject.connectSlotsByName(topMenu)

    def retranslateUi(self, topMenu):
        topMenu.setWindowTitle(QtGui.QApplication.translate("topMenu", "Form", None, QtGui.QApplication.UnicodeUTF8))

