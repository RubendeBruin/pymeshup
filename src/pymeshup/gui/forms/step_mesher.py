# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'step_mesher.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFrame,
    QGridLayout, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(906, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.dsAngTol = QDoubleSpinBox(self.widget_2)
        self.dsAngTol.setObjectName(u"dsAngTol")
        self.dsAngTol.setDecimals(3)
        self.dsAngTol.setSingleStep(0.010000000000000)
        self.dsAngTol.setValue(0.100000000000000)

        self.gridLayout.addWidget(self.dsAngTol, 3, 1, 1, 1)

        self.label_4 = QLabel(self.widget_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.chAutoApply = QCheckBox(self.widget_2)
        self.chAutoApply.setObjectName(u"chAutoApply")
        self.chAutoApply.setChecked(True)

        self.gridLayout.addWidget(self.chAutoApply, 4, 0, 1, 1)

        self.dsLinTol = QDoubleSpinBox(self.widget_2)
        self.dsLinTol.setObjectName(u"dsLinTol")
        self.dsLinTol.setDecimals(3)
        self.dsLinTol.setMinimum(0.000000000000000)
        self.dsLinTol.setMaximum(10000.000000000000000)
        self.dsLinTol.setSingleStep(0.010000000000000)
        self.dsLinTol.setValue(1.000000000000000)

        self.gridLayout.addWidget(self.dsLinTol, 2, 1, 1, 1)

        self.pbApply = QPushButton(self.widget_2)
        self.pbApply.setObjectName(u"pbApply")

        self.gridLayout.addWidget(self.pbApply, 4, 1, 1, 1)

        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.widget_2, 0, 1, 1, 1)

        self.view3d = QWidget(self.centralwidget)
        self.view3d.setObjectName(u"view3d")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view3d.sizePolicy().hasHeightForWidth())
        self.view3d.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.view3d, 1, 0, 1, 2)

        self.lbFeedback = QLabel(self.centralwidget)
        self.lbFeedback.setObjectName(u"lbFeedback")
        self.lbFeedback.setFrameShape(QFrame.Shape.Box)

        self.gridLayout_2.addWidget(self.lbFeedback, 2, 0, 1, 2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.gridLayout_3 = QGridLayout(self.widget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.leFilename = QLineEdit(self.widget)
        self.leFilename.setObjectName(u"leFilename")

        self.gridLayout_3.addWidget(self.leFilename, 0, 1, 1, 1)

        self.pbBrowse = QPushButton(self.widget)
        self.pbBrowse.setObjectName(u"pbBrowse")

        self.gridLayout_3.addWidget(self.pbBrowse, 0, 2, 1, 1)

        self.leScale = QLineEdit(self.widget)
        self.leScale.setObjectName(u"leScale")

        self.gridLayout_3.addWidget(self.leScale, 1, 1, 1, 1)

        self.lbMessage_2 = QLabel(self.widget)
        self.lbMessage_2.setObjectName(u"lbMessage_2")

        self.gridLayout_3.addWidget(self.lbMessage_2, 1, 0, 1, 1)

        self.pbBatch = QPushButton(self.widget)
        self.pbBatch.setObjectName(u"pbBatch")

        self.gridLayout_3.addWidget(self.pbBatch, 3, 1, 1, 1)

        self.pbSave = QPushButton(self.widget)
        self.pbSave.setObjectName(u"pbSave")

        self.gridLayout_3.addWidget(self.pbSave, 3, 2, 1, 1)

        self.pbLoad = QPushButton(self.widget)
        self.pbLoad.setObjectName(u"pbLoad")

        self.gridLayout_3.addWidget(self.pbLoad, 1, 2, 1, 1)


        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 906, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Angular tolerance", None))
        self.chAutoApply.setText(QCoreApplication.translate("MainWindow", u"auto apply", None))
        self.pbApply.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Linear tolerance", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"settings", None))
        self.lbFeedback.setText(QCoreApplication.translate("MainWindow", u"Ready...", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"step file", None))
        self.pbBrowse.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.leScale.setText(QCoreApplication.translate("MainWindow", u".001", None))
        self.lbMessage_2.setText(QCoreApplication.translate("MainWindow", u"scale", None))
        self.pbBatch.setText(QCoreApplication.translate("MainWindow", u"Batch process all STEP files in this folder using these settings", None))
        self.pbSave.setText(QCoreApplication.translate("MainWindow", u"Save conversion as STL", None))
        self.pbLoad.setText(QCoreApplication.translate("MainWindow", u"(re)load", None))
    # retranslateUi

