# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GHS_to_DAVE_form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpinBox, QWidget)

class Ui_ConversionDialog(object):
    def setupUi(self, ConversionDialog):
        if not ConversionDialog.objectName():
            ConversionDialog.setObjectName(u"ConversionDialog")
        ConversionDialog.resize(442, 305)
        self.gridLayout = QGridLayout(ConversionDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(ConversionDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_4 = QLabel(ConversionDialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 2)

        self.pbGo = QPushButton(ConversionDialog)
        self.pbGo.setObjectName(u"pbGo")

        self.gridLayout.addWidget(self.pbGo, 6, 0, 1, 1)

        self.label = QLabel(ConversionDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_5 = QLabel(ConversionDialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 2)

        self.tbFilename = QLineEdit(ConversionDialog)
        self.tbFilename.setObjectName(u"tbFilename")

        self.gridLayout.addWidget(self.tbFilename, 0, 1, 1, 2)

        self.pbBrowse = QPushButton(ConversionDialog)
        self.pbBrowse.setObjectName(u"pbBrowse")

        self.gridLayout.addWidget(self.pbBrowse, 0, 3, 1, 1)

        self.tbOutputDir = QLineEdit(ConversionDialog)
        self.tbOutputDir.setObjectName(u"tbOutputDir")

        self.gridLayout.addWidget(self.tbOutputDir, 1, 1, 1, 3)

        self.tbVesselName = QLineEdit(ConversionDialog)
        self.tbVesselName.setObjectName(u"tbVesselName")

        self.gridLayout.addWidget(self.tbVesselName, 2, 2, 1, 2)

        self.sbDeg = QSpinBox(ConversionDialog)
        self.sbDeg.setObjectName(u"sbDeg")
        self.sbDeg.setMinimum(1)
        self.sbDeg.setMaximum(360)
        self.sbDeg.setValue(10)

        self.gridLayout.addWidget(self.sbDeg, 3, 2, 1, 2)

        self.tbOutput = QPlainTextEdit(ConversionDialog)
        self.tbOutput.setObjectName(u"tbOutput")
        self.tbOutput.setStyleSheet(u"background:palette(midlight)")

        self.gridLayout.addWidget(self.tbOutput, 4, 0, 1, 4)

        QWidget.setTabOrder(self.tbFilename, self.pbBrowse)
        QWidget.setTabOrder(self.pbBrowse, self.tbOutputDir)
        QWidget.setTabOrder(self.tbOutputDir, self.tbVesselName)
        QWidget.setTabOrder(self.tbVesselName, self.sbDeg)
        QWidget.setTabOrder(self.sbDeg, self.pbGo)
        QWidget.setTabOrder(self.pbGo, self.tbOutput)

        self.retranslateUi(ConversionDialog)

        QMetaObject.connectSlotsByName(ConversionDialog)
    # setupUi

    def retranslateUi(self, ConversionDialog):
        ConversionDialog.setWindowTitle(QCoreApplication.translate("ConversionDialog", u"Convert GHS to DAVE kickstart", None))
        self.label_2.setText(QCoreApplication.translate("ConversionDialog", u"Output folder", None))
        self.label_4.setText(QCoreApplication.translate("ConversionDialog", u"vessel name", None))
        self.pbGo.setText(QCoreApplication.translate("ConversionDialog", u"Go", None))
        self.label.setText(QCoreApplication.translate("ConversionDialog", u"GHS file", None))
        self.label_5.setText(QCoreApplication.translate("ConversionDialog", u"circular segment resolution [deg]", None))
        self.tbFilename.setPlaceholderText(QCoreApplication.translate("ConversionDialog", u".gf of .fg1 file here", None))
        self.pbBrowse.setText(QCoreApplication.translate("ConversionDialog", u"...", None))
        self.tbOutputDir.setPlaceholderText(QCoreApplication.translate("ConversionDialog", u"output directory", None))
        self.tbVesselName.setText("")
        self.tbVesselName.setPlaceholderText(QCoreApplication.translate("ConversionDialog", u"Ducky1", None))
    # retranslateUi

