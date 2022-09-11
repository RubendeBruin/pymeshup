# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QFrame, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSplitter, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(937, 754)
        self.actionHelp_visible = QAction(MainWindow)
        self.actionHelp_visible.setObjectName(u"actionHelp_visible")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.top_widget = QWidget(self.centralwidget)
        self.top_widget.setObjectName(u"top_widget")
        self.top_widget.setMaximumSize(QSize(16777215, 20))
        self.horizontalLayout = QHBoxLayout(self.top_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 0, -1, 0)
        self.label_3 = QLabel(self.top_widget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.pushButton_2 = QPushButton(self.top_widget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.verticalLayout_3.addWidget(self.top_widget)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.splitter_3 = QSplitter(self.widget)
        self.splitter_3.setObjectName(u"splitter_3")
        sizePolicy.setHeightForWidth(self.splitter_3.sizePolicy().hasHeightForWidth())
        self.splitter_3.setSizePolicy(sizePolicy)
        self.splitter_3.setFrameShape(QFrame.NoFrame)
        self.splitter_3.setOrientation(Qt.Vertical)
        self.widget_3 = QWidget(self.splitter_3)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.widget_3)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet(u"background:darkblue;\n"
"color:white")

        self.verticalLayout.addWidget(self.label_2)

        self.teCode = QTextEdit(self.widget_3)
        self.teCode.setObjectName(u"teCode")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.teCode.sizePolicy().hasHeightForWidth())
        self.teCode.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.teCode)

        self.pushButton = QPushButton(self.widget_3)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.splitter_3.addWidget(self.widget_3)
        self.teFeedback = QTextEdit(self.splitter_3)
        self.teFeedback.setObjectName(u"teFeedback")
        sizePolicy1.setHeightForWidth(self.teFeedback.sizePolicy().hasHeightForWidth())
        self.teFeedback.setSizePolicy(sizePolicy1)
        self.splitter_3.addWidget(self.teFeedback)

        self.horizontalLayout_2.addWidget(self.splitter_3)

        self.splitter.addWidget(self.widget)
        self.widget_2 = QWidget(self.splitter)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.splitter_2 = QSplitter(self.widget_2)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setFrameShape(QFrame.NoFrame)
        self.splitter_2.setOrientation(Qt.Vertical)
        self.widget_4 = QWidget(self.splitter_2)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.listFrames = QListWidget(self.widget_4)
        self.listFrames.setObjectName(u"listFrames")
        sizePolicy1.setHeightForWidth(self.listFrames.sizePolicy().hasHeightForWidth())
        self.listFrames.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.listFrames)

        self.widgetPlot = QWidget(self.widget_4)
        self.widgetPlot.setObjectName(u"widgetPlot")

        self.horizontalLayout_4.addWidget(self.widgetPlot)

        self.splitter_2.addWidget(self.widget_4)
        self.wiget99 = QWidget(self.splitter_2)
        self.wiget99.setObjectName(u"wiget99")
        self.horizontalLayout_5 = QHBoxLayout(self.wiget99)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.listVolumes = QListWidget(self.wiget99)
        self.listVolumes.setObjectName(u"listVolumes")
        sizePolicy1.setHeightForWidth(self.listVolumes.sizePolicy().hasHeightForWidth())
        self.listVolumes.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.listVolumes)

        self.widgetGraphics = QWidget(self.wiget99)
        self.widgetGraphics.setObjectName(u"widgetGraphics")

        self.horizontalLayout_5.addWidget(self.widgetGraphics)

        self.splitter_2.addWidget(self.wiget99)

        self.horizontalLayout_3.addWidget(self.splitter_2)

        self.splitter.addWidget(self.widget_2)

        self.verticalLayout_3.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 937, 21))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(self.dockWidgetContents)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setEnabled(True)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 209, 671))
        self.horizontalLayout_6 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.horizontalLayout_6.addWidget(self.label)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.actionHelp_visible)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionHelp_visible.setText(QCoreApplication.translate("MainWindow", u"Help visible", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"clean output folder", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"SCRIPT", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Run [F5]", None))
#if QT_CONFIG(shortcut)
        self.pushButton.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">HELP</span></p><p><br/></p><p>PyMeshUp is a simple script-based application to generate meshes.</p><p><br/></p><p>Primitive volumes can be created using:</p><p>- Box</p><p>- Cylinder</p><p>- Hull</p><p><br/></p><p>Meshes can be combined and modified using:</p><p>- add</p><p>- remove</p><p>- rotate</p><p>- move</p><p>- scale</p><p>- crop</p></body></html>", None))
    # retranslateUi

