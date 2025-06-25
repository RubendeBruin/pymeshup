# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDockWidget,
    QDoubleSpinBox, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSplitter, QStatusBar, QTabWidget,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1179, 1017)
        self.actionHelp_visible = QAction(MainWindow)
        self.actionHelp_visible.setObjectName(u"actionHelp_visible")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionReopen = QAction(MainWindow)
        self.actionReopen.setObjectName(u"actionReopen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_as = QAction(MainWindow)
        self.actionSave_as.setObjectName(u"actionSave_as")
        self.actionOpen_2 = QAction(MainWindow)
        self.actionOpen_2.setObjectName(u"actionOpen_2")
        self.actionSet_work_folder = QAction(MainWindow)
        self.actionSet_work_folder.setObjectName(u"actionSet_work_folder")
        self.actionOpen_GSH_to_DAVE_conversion_tool = QAction(MainWindow)
        self.actionOpen_GSH_to_DAVE_conversion_tool.setObjectName(u"actionOpen_GSH_to_DAVE_conversion_tool")
        self.actionOpen_work_folder_in_explorer = QAction(MainWindow)
        self.actionOpen_work_folder_in_explorer.setObjectName(u"actionOpen_work_folder_in_explorer")
        self.actionLoad_Capytaine_settings = QAction(MainWindow)
        self.actionLoad_Capytaine_settings.setObjectName(u"actionLoad_Capytaine_settings")
        self.actionSave_Capytaine_settings = QAction(MainWindow)
        self.actionSave_Capytaine_settings.setObjectName(u"actionSave_Capytaine_settings")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.label_3, 0, 2, 1, 1)

        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout = QVBoxLayout(self.widget_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter_4 = QSplitter(self.widget_3)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Orientation.Vertical)
        self.tabWidget = QTabWidget(self.splitter_4)
        self.tabWidget.setObjectName(u"tabWidget")
        self.Mesh = QWidget()
        self.Mesh.setObjectName(u"Mesh")
        self.verticalLayout_5 = QVBoxLayout(self.Mesh)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.splitter = QSplitter(self.Mesh)
        self.splitter.setObjectName(u"splitter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy1)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy2)
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        self.label_2.setStyleSheet(u"background: rgb(255, 204, 0);")

        self.verticalLayout_3.addWidget(self.label_2)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_3.addWidget(self.pushButton)

        self.splitter.addWidget(self.widget)
        self.widget_2 = QWidget(self.splitter)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.splitter_2 = QSplitter(self.widget_2)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setFrameShape(QFrame.Shape.NoFrame)
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)
        self.widget_4 = QWidget(self.splitter_2)
        self.widget_4.setObjectName(u"widget_4")
        self.gridLayout_2 = QGridLayout(self.widget_4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_7 = QLabel(self.widget_4)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)

        self.listFrames = QListWidget(self.widget_4)
        self.listFrames.setObjectName(u"listFrames")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.listFrames.sizePolicy().hasHeightForWidth())
        self.listFrames.setSizePolicy(sizePolicy3)
        self.listFrames.setFrameShape(QFrame.Shape.Box)

        self.gridLayout_2.addWidget(self.listFrames, 1, 0, 1, 1)

        self.widgetPlot = QWidget(self.widget_4)
        self.widgetPlot.setObjectName(u"widgetPlot")

        self.gridLayout_2.addWidget(self.widgetPlot, 1, 1, 1, 1)

        self.splitter_2.addWidget(self.widget_4)
        self.wiget99 = QWidget(self.splitter_2)
        self.wiget99.setObjectName(u"wiget99")
        self.gridLayout = QGridLayout(self.wiget99)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_5 = QLabel(self.wiget99)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)

        self.label_6 = QLabel(self.wiget99)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.widget_6 = QWidget(self.wiget99)
        self.widget_6.setObjectName(u"widget_6")
        self.verticalLayout_4 = QVBoxLayout(self.widget_6)
        self.verticalLayout_4.setSpacing(1)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(1, 1, 1, 1)
        self.listVolumes = QListWidget(self.widget_6)
        self.listVolumes.setObjectName(u"listVolumes")
        sizePolicy3.setHeightForWidth(self.listVolumes.sizePolicy().hasHeightForWidth())
        self.listVolumes.setSizePolicy(sizePolicy3)
        self.listVolumes.setFrameShape(QFrame.Shape.Box)

        self.verticalLayout_4.addWidget(self.listVolumes)

        self.widget_7 = QWidget(self.widget_6)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_3 = QPushButton(self.widget_7)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_7.addWidget(self.pushButton_3)

        self.label_4 = QLabel(self.widget_7)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_7.addWidget(self.label_4)

        self.comboBox = QComboBox(self.widget_7)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_7.addWidget(self.comboBox)


        self.verticalLayout_4.addWidget(self.widget_7)


        self.gridLayout.addWidget(self.widget_6, 1, 0, 1, 1)

        self.widgetGraphics = QWidget(self.wiget99)
        self.widgetGraphics.setObjectName(u"widgetGraphics")
        self.widgetGraphics.setToolTipDuration(-1)

        self.gridLayout.addWidget(self.widgetGraphics, 1, 1, 1, 1)

        self.splitter_2.addWidget(self.wiget99)

        self.horizontalLayout_3.addWidget(self.splitter_2)

        self.splitter.addWidget(self.widget_2)

        self.verticalLayout_5.addWidget(self.splitter)

        self.tabWidget.addTab(self.Mesh, "")
        self.Capytaine = QWidget()
        self.Capytaine.setObjectName(u"Capytaine")
        self.gridLayout_4 = QGridLayout(self.Capytaine)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_11 = QLabel(self.Capytaine)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 2, 0, 1, 1)

        self.teWaterdepth = QDoubleSpinBox(self.Capytaine)
        self.teWaterdepth.setObjectName(u"teWaterdepth")
        self.teWaterdepth.setMinimum(0.010000000000000)
        self.teWaterdepth.setMaximum(9999999.000000000000000)
        self.teWaterdepth.setValue(100.000000000000000)

        self.gridLayout_4.addWidget(self.teWaterdepth, 8, 2, 1, 1)

        self.label_16 = QLabel(self.Capytaine)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_4.addWidget(self.label_16, 9, 0, 1, 1)

        self.teHeading = QLineEdit(self.Capytaine)
        self.teHeading.setObjectName(u"teHeading")

        self.gridLayout_4.addWidget(self.teHeading, 5, 2, 1, 1)

        self.label_9 = QLabel(self.Capytaine)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)

        self.teOutputFile = QLineEdit(self.Capytaine)
        self.teOutputFile.setObjectName(u"teOutputFile")

        self.gridLayout_4.addWidget(self.teOutputFile, 1, 2, 1, 1)

        self.teMeshFile = QLineEdit(self.Capytaine)
        self.teMeshFile.setObjectName(u"teMeshFile")

        self.gridLayout_4.addWidget(self.teMeshFile, 0, 2, 1, 1)

        self.lblPeriods = QLabel(self.Capytaine)
        self.lblPeriods.setObjectName(u"lblPeriods")
        self.lblPeriods.setWordWrap(True)

        self.gridLayout_4.addWidget(self.lblPeriods, 4, 2, 1, 1)

        self.cbSymmetryMesh = QCheckBox(self.Capytaine)
        self.cbSymmetryMesh.setObjectName(u"cbSymmetryMesh")

        self.gridLayout_4.addWidget(self.cbSymmetryMesh, 15, 0, 1, 3)

        self.cbLid = QCheckBox(self.Capytaine)
        self.cbLid.setObjectName(u"cbLid")

        self.gridLayout_4.addWidget(self.cbLid, 11, 0, 1, 3)

        self.cbInf = QCheckBox(self.Capytaine)
        self.cbInf.setObjectName(u"cbInf")

        self.gridLayout_4.addWidget(self.cbInf, 8, 1, 1, 1)

        self.pbShowMesh = QPushButton(self.Capytaine)
        self.pbShowMesh.setObjectName(u"pbShowMesh")

        self.gridLayout_4.addWidget(self.pbShowMesh, 18, 0, 1, 1)

        self.label_20 = QLabel(self.Capytaine)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_4.addWidget(self.label_20, 1, 0, 1, 1)

        self.label_13 = QLabel(self.Capytaine)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_4.addWidget(self.label_13, 5, 0, 1, 1)

        self.tePeriods = QLineEdit(self.Capytaine)
        self.tePeriods.setObjectName(u"tePeriods")

        self.gridLayout_4.addWidget(self.tePeriods, 2, 2, 1, 1)

        self.lblHeading = QLabel(self.Capytaine)
        self.lblHeading.setObjectName(u"lblHeading")
        self.lblHeading.setWordWrap(True)

        self.gridLayout_4.addWidget(self.lblHeading, 7, 2, 1, 1)

        self.pbRunCapytaine = QPushButton(self.Capytaine)
        self.pbRunCapytaine.setObjectName(u"pbRunCapytaine")

        self.gridLayout_4.addWidget(self.pbRunCapytaine, 23, 0, 1, 1)

        self.label_15 = QLabel(self.Capytaine)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_4.addWidget(self.label_15, 8, 0, 1, 1)

        self.cbSymmetryHeadings = QCheckBox(self.Capytaine)
        self.cbSymmetryHeadings.setObjectName(u"cbSymmetryHeadings")

        self.gridLayout_4.addWidget(self.cbSymmetryHeadings, 17, 0, 1, 3)

        self.te_water_level_elevation = QDoubleSpinBox(self.Capytaine)
        self.te_water_level_elevation.setObjectName(u"te_water_level_elevation")
        self.te_water_level_elevation.setMinimum(-999.000000000000000)
        self.te_water_level_elevation.setMaximum(999.000000000000000)
        self.te_water_level_elevation.setValue(0.000000000000000)

        self.gridLayout_4.addWidget(self.te_water_level_elevation, 9, 2, 1, 1)

        self.tabWidget.addTab(self.Capytaine, "")
        self.splitter_4.addWidget(self.tabWidget)
        self.teFeedback = QTextEdit(self.splitter_4)
        self.teFeedback.setObjectName(u"teFeedback")
        self.splitter_4.addWidget(self.teFeedback)

        self.verticalLayout.addWidget(self.splitter_4)


        self.gridLayout_3.addWidget(self.widget_3, 1, 0, 1, 4)

        self.pbWorkFolder = QPushButton(self.centralwidget)
        self.pbWorkFolder.setObjectName(u"pbWorkFolder")

        self.gridLayout_3.addWidget(self.pbWorkFolder, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1179, 33))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuExamples = QMenu(self.menubar)
        self.menuExamples.setObjectName(u"menuExamples")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidget.setStyleSheet(u"")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.teHelp = QTextEdit(self.dockWidgetContents)
        self.teHelp.setObjectName(u"teHelp")
        self.teHelp.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.teHelp)

        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockWidget)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuExamples.menuAction())
        self.menuHelp.addAction(self.actionHelp_visible)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionReopen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSet_work_folder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen_GSH_to_DAVE_conversion_tool)
        self.menuFile.addAction(self.actionOpen_work_folder_in_explorer)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoad_Capytaine_settings)
        self.menuFile.addAction(self.actionSave_Capytaine_settings)
        self.menuExamples.addAction(self.actionOpen_2)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionHelp_visible.setText(QCoreApplication.translate("MainWindow", u"Help visible", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionReopen.setText(QCoreApplication.translate("MainWindow", u"Reopen Last File", None))
#if QT_CONFIG(shortcut)
        self.actionReopen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_as.setText(QCoreApplication.translate("MainWindow", u"Save as", None))
        self.actionOpen_2.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSet_work_folder.setText(QCoreApplication.translate("MainWindow", u"Set work folder", None))
        self.actionOpen_GSH_to_DAVE_conversion_tool.setText(QCoreApplication.translate("MainWindow", u"Open GHS to DAVE conversion tool", None))
        self.actionOpen_work_folder_in_explorer.setText(QCoreApplication.translate("MainWindow", u"Open work folder in explorer", None))
        self.actionLoad_Capytaine_settings.setText(QCoreApplication.translate("MainWindow", u"Load Capytaine settings", None))
        self.actionSave_Capytaine_settings.setText(QCoreApplication.translate("MainWindow", u"Save Capytaine settings", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"SCRIPT", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u">> Run [F5]", None))
#if QT_CONFIG(shortcut)
        self.pushButton.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Frames", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"middle-mouse or space to navigate, w: wireframe, s for solid", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Volumes:", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Save selected ", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"as", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u".stl", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u".obj", None))

#if QT_CONFIG(tooltip)
        self.widgetGraphics.setToolTip(QCoreApplication.translate("MainWindow", u"On touchpath: use \"m\" or space to navigate instead of middle-mouse button\n"
"\n"
"Hold middle mouse to rotate\n"
"Shift + middle to pan\n"
"Ctrl + middle to zoom\n"
"B for box\n"
"2/3 for 2d/3d", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Mesh), QCoreApplication.translate("MainWindow", u"Mesh", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Periods [s]", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Water level elevation [m]", None))
        self.teHeading.setText(QCoreApplication.translate("MainWindow", u"np.linspace(0, 180, 9)", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Mesh [file, in workfolder]", None))
        self.teOutputFile.setText(QCoreApplication.translate("MainWindow", u"my_model", None))
        self.lblPeriods.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.cbSymmetryMesh.setText(QCoreApplication.translate("MainWindow", u"Use symmetry in XZ for mesh (only half of mesh defined)", None))
        self.cbLid.setText(QCoreApplication.translate("MainWindow", u"Add lid at z=-0.01m (can not be used together with symmetry)", None))
        self.cbInf.setText(QCoreApplication.translate("MainWindow", u"Infinite", None))
        self.pbShowMesh.setText(QCoreApplication.translate("MainWindow", u"Show mesh", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Output file names", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Headings [degrees]", None))
        self.tePeriods.setText(QCoreApplication.translate("MainWindow", u"[*np.linspace(0.5,10,num=20), 11,12,14,16,20]", None))
        self.lblHeading.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pbRunCapytaine.setText(QCoreApplication.translate("MainWindow", u"Go!", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Waterdepth [m]", None))
        self.cbSymmetryHeadings.setText(QCoreApplication.translate("MainWindow", u"Use symmetry in XY for output (only headings 0...180 defined)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Capytaine), QCoreApplication.translate("MainWindow", u"Capytaine", None))
        self.pbWorkFolder.setText(QCoreApplication.translate("MainWindow", u"Workfolder:", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuExamples.setTitle(QCoreApplication.translate("MainWindow", u"Examples", None))
    # retranslateUi

