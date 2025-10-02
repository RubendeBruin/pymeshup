# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QRect,
    Qt,
)
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDockWidget,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1179, 1017)
        self.actionHelp_visible = QAction(MainWindow)
        self.actionHelp_visible.setObjectName("actionHelp_visible")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionReopen = QAction(MainWindow)
        self.actionReopen.setObjectName("actionReopen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionOpen_2 = QAction(MainWindow)
        self.actionOpen_2.setObjectName("actionOpen_2")
        self.actionSet_work_folder = QAction(MainWindow)
        self.actionSet_work_folder.setObjectName("actionSet_work_folder")
        self.actionOpen_GSH_to_DAVE_conversion_tool = QAction(MainWindow)
        self.actionOpen_GSH_to_DAVE_conversion_tool.setObjectName(
            "actionOpen_GSH_to_DAVE_conversion_tool"
        )
        self.actionOpen_work_folder_in_explorer = QAction(MainWindow)
        self.actionOpen_work_folder_in_explorer.setObjectName(
            "actionOpen_work_folder_in_explorer"
        )
        self.actionLoad_Capytaine_settings = QAction(MainWindow)
        self.actionLoad_Capytaine_settings.setObjectName(
            "actionLoad_Capytaine_settings"
        )
        self.actionSave_Capytaine_settings = QAction(MainWindow)
        self.actionSave_Capytaine_settings.setObjectName(
            "actionSave_Capytaine_settings"
        )
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.label_3, 0, 2, 1, 1)

        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout = QVBoxLayout(self.widget_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_4 = QSplitter(self.widget_3)
        self.splitter_4.setObjectName("splitter_4")
        self.splitter_4.setOrientation(Qt.Orientation.Vertical)
        self.tabWidget = QTabWidget(self.splitter_4)
        self.tabWidget.setObjectName("tabWidget")
        self.Mesh = QWidget()
        self.Mesh.setObjectName("Mesh")
        self.verticalLayout_5 = QVBoxLayout(self.Mesh)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.splitter = QSplitter(self.Mesh)
        self.splitter.setObjectName("splitter")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy1)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName("widget")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy2)
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        self.label_2.setStyleSheet("background: rgb(255, 204, 0);")

        self.verticalLayout_3.addWidget(self.label_2)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")

        self.verticalLayout_3.addWidget(self.pushButton)

        self.splitter.addWidget(self.widget)
        self.widget_2 = QWidget(self.splitter)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.splitter_2 = QSplitter(self.widget_2)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter_2.setFrameShape(QFrame.Shape.NoFrame)
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)
        self.widget_4 = QWidget(self.splitter_2)
        self.widget_4.setObjectName("widget_4")
        self.gridLayout_2 = QGridLayout(self.widget_4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QLabel(self.widget_4)
        self.label_7.setObjectName("label_7")

        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)

        self.listFrames = QListWidget(self.widget_4)
        self.listFrames.setObjectName("listFrames")
        sizePolicy3 = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.listFrames.sizePolicy().hasHeightForWidth())
        self.listFrames.setSizePolicy(sizePolicy3)
        self.listFrames.setFrameShape(QFrame.Shape.Box)

        self.gridLayout_2.addWidget(self.listFrames, 1, 0, 1, 1)

        self.widgetPlot = QWidget(self.widget_4)
        self.widgetPlot.setObjectName("widgetPlot")

        self.gridLayout_2.addWidget(self.widgetPlot, 1, 1, 1, 1)

        self.splitter_2.addWidget(self.widget_4)
        self.wiget99 = QWidget(self.splitter_2)
        self.wiget99.setObjectName("wiget99")
        self.gridLayout = QGridLayout(self.wiget99)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QLabel(self.wiget99)
        self.label_5.setObjectName("label_5")

        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)

        self.label_6 = QLabel(self.wiget99)
        self.label_6.setObjectName("label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.widget_6 = QWidget(self.wiget99)
        self.widget_6.setObjectName("widget_6")
        self.verticalLayout_4 = QVBoxLayout(self.widget_6)
        self.verticalLayout_4.setSpacing(1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(1, 1, 1, 1)
        self.listVolumes = QListWidget(self.widget_6)
        self.listVolumes.setObjectName("listVolumes")
        sizePolicy3.setHeightForWidth(self.listVolumes.sizePolicy().hasHeightForWidth())
        self.listVolumes.setSizePolicy(sizePolicy3)
        self.listVolumes.setFrameShape(QFrame.Shape.Box)

        self.verticalLayout_4.addWidget(self.listVolumes)

        self.widget_7 = QWidget(self.widget_6)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.pushButton_3 = QPushButton(self.widget_7)
        self.pushButton_3.setObjectName("pushButton_3")

        self.horizontalLayout_7.addWidget(self.pushButton_3)

        self.label_4 = QLabel(self.widget_7)
        self.label_4.setObjectName("label_4")

        self.horizontalLayout_7.addWidget(self.label_4)

        self.comboBox = QComboBox(self.widget_7)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName("comboBox")

        self.horizontalLayout_7.addWidget(self.comboBox)

        self.verticalLayout_4.addWidget(self.widget_7)

        self.gridLayout.addWidget(self.widget_6, 1, 0, 1, 1)

        self.widgetGraphics = QWidget(self.wiget99)
        self.widgetGraphics.setObjectName("widgetGraphics")
        self.widgetGraphics.setToolTipDuration(-1)

        self.gridLayout.addWidget(self.widgetGraphics, 1, 1, 1, 1)

        self.splitter_2.addWidget(self.wiget99)

        self.horizontalLayout_3.addWidget(self.splitter_2)

        self.splitter.addWidget(self.widget_2)

        self.verticalLayout_5.addWidget(self.splitter)

        self.tabWidget.addTab(self.Mesh, "")
        self.Capytaine = QWidget()
        self.Capytaine.setObjectName("Capytaine")
        self.gridLayout_4 = QGridLayout(self.Capytaine)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_11 = QLabel(self.Capytaine)
        self.label_11.setObjectName("label_11")

        self.gridLayout_4.addWidget(self.label_11, 2, 0, 1, 1)

        self.teWaterdepth = QDoubleSpinBox(self.Capytaine)
        self.teWaterdepth.setObjectName("teWaterdepth")
        self.teWaterdepth.setMinimum(0.010000000000000)
        self.teWaterdepth.setMaximum(9999999.000000000000000)
        self.teWaterdepth.setValue(100.000000000000000)

        self.gridLayout_4.addWidget(self.teWaterdepth, 8, 2, 1, 1)

        self.label_16 = QLabel(self.Capytaine)
        self.label_16.setObjectName("label_16")

        self.gridLayout_4.addWidget(self.label_16, 9, 0, 1, 1)

        self.teHeading = QLineEdit(self.Capytaine)
        self.teHeading.setObjectName("teHeading")

        self.gridLayout_4.addWidget(self.teHeading, 5, 2, 1, 1)

        self.label_9 = QLabel(self.Capytaine)
        self.label_9.setObjectName("label_9")

        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)

        self.teOutputFile = QLineEdit(self.Capytaine)
        self.teOutputFile.setObjectName("teOutputFile")

        self.gridLayout_4.addWidget(self.teOutputFile, 1, 2, 1, 1)

        self.teMeshFile = QLineEdit(self.Capytaine)
        self.teMeshFile.setObjectName("teMeshFile")

        self.gridLayout_4.addWidget(self.teMeshFile, 0, 2, 1, 1)

        self.lblPeriods = QLabel(self.Capytaine)
        self.lblPeriods.setObjectName("lblPeriods")
        self.lblPeriods.setWordWrap(True)

        self.gridLayout_4.addWidget(self.lblPeriods, 4, 2, 1, 1)

        self.cbSymmetryMesh = QCheckBox(self.Capytaine)
        self.cbSymmetryMesh.setObjectName("cbSymmetryMesh")

        self.gridLayout_4.addWidget(self.cbSymmetryMesh, 15, 0, 1, 3)

        self.cbLid = QCheckBox(self.Capytaine)
        self.cbLid.setObjectName("cbLid")

        self.gridLayout_4.addWidget(self.cbLid, 11, 0, 1, 3)

        self.cbInf = QCheckBox(self.Capytaine)
        self.cbInf.setObjectName("cbInf")

        self.gridLayout_4.addWidget(self.cbInf, 8, 1, 1, 1)

        self.pbShowMesh = QPushButton(self.Capytaine)
        self.pbShowMesh.setObjectName("pbShowMesh")

        self.gridLayout_4.addWidget(self.pbShowMesh, 18, 0, 1, 1)

        self.label_20 = QLabel(self.Capytaine)
        self.label_20.setObjectName("label_20")

        self.gridLayout_4.addWidget(self.label_20, 1, 0, 1, 1)

        self.label_13 = QLabel(self.Capytaine)
        self.label_13.setObjectName("label_13")

        self.gridLayout_4.addWidget(self.label_13, 5, 0, 1, 1)

        self.tePeriods = QLineEdit(self.Capytaine)
        self.tePeriods.setObjectName("tePeriods")

        self.gridLayout_4.addWidget(self.tePeriods, 2, 2, 1, 1)

        self.lblHeading = QLabel(self.Capytaine)
        self.lblHeading.setObjectName("lblHeading")
        self.lblHeading.setWordWrap(True)

        self.gridLayout_4.addWidget(self.lblHeading, 7, 2, 1, 1)

        self.pbRunCapytaine = QPushButton(self.Capytaine)
        self.pbRunCapytaine.setObjectName("pbRunCapytaine")

        self.gridLayout_4.addWidget(self.pbRunCapytaine, 23, 0, 1, 1)

        self.label_15 = QLabel(self.Capytaine)
        self.label_15.setObjectName("label_15")

        self.gridLayout_4.addWidget(self.label_15, 8, 0, 1, 1)

        self.cbSymmetryHeadings = QCheckBox(self.Capytaine)
        self.cbSymmetryHeadings.setObjectName("cbSymmetryHeadings")

        self.gridLayout_4.addWidget(self.cbSymmetryHeadings, 17, 0, 1, 3)

        self.te_water_level_elevation = QDoubleSpinBox(self.Capytaine)
        self.te_water_level_elevation.setObjectName("te_water_level_elevation")
        self.te_water_level_elevation.setMinimum(-999.000000000000000)
        self.te_water_level_elevation.setMaximum(999.000000000000000)
        self.te_water_level_elevation.setValue(0.000000000000000)

        self.gridLayout_4.addWidget(self.te_water_level_elevation, 9, 2, 1, 1)

        self.tabWidget.addTab(self.Capytaine, "")
        self.splitter_4.addWidget(self.tabWidget)
        self.teFeedback = QTextEdit(self.splitter_4)
        self.teFeedback.setObjectName("teFeedback")
        self.splitter_4.addWidget(self.teFeedback)

        self.verticalLayout.addWidget(self.splitter_4)

        self.gridLayout_3.addWidget(self.widget_3, 1, 0, 1, 4)

        self.pbWorkFolder = QPushButton(self.centralwidget)
        self.pbWorkFolder.setObjectName("pbWorkFolder")

        self.gridLayout_3.addWidget(self.pbWorkFolder, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1179, 33))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuExamples = QMenu(self.menubar)
        self.menuExamples.setObjectName("menuExamples")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidget.setStyleSheet("")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.teHelp = QTextEdit(self.dockWidgetContents)
        self.teHelp.setObjectName("teHelp")
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
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.actionHelp_visible.setText(
            QCoreApplication.translate("MainWindow", "Help visible", None)
        )
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", "Open", None))
        # if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+O", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionReopen.setText(
            QCoreApplication.translate("MainWindow", "Reopen Last File", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionReopen.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+R", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", "Save", None))
        # if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+S", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionSave_as.setText(
            QCoreApplication.translate("MainWindow", "Save as", None)
        )
        self.actionOpen_2.setText(
            QCoreApplication.translate("MainWindow", "Open", None)
        )
        self.actionSet_work_folder.setText(
            QCoreApplication.translate("MainWindow", "Set work folder", None)
        )
        self.actionOpen_GSH_to_DAVE_conversion_tool.setText(
            QCoreApplication.translate(
                "MainWindow", "Open GHS to DAVE conversion tool", None
            )
        )
        self.actionOpen_work_folder_in_explorer.setText(
            QCoreApplication.translate(
                "MainWindow", "Open work folder in explorer", None
            )
        )
        self.actionLoad_Capytaine_settings.setText(
            QCoreApplication.translate("MainWindow", "Load Capytaine settings", None)
        )
        self.actionSave_Capytaine_settings.setText(
            QCoreApplication.translate("MainWindow", "Save Capytaine settings", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.label_2.setText(QCoreApplication.translate("MainWindow", "SCRIPT", None))
        self.pushButton.setText(
            QCoreApplication.translate("MainWindow", ">> Run [F5]", None)
        )
        # if QT_CONFIG(shortcut)
        self.pushButton.setShortcut(
            QCoreApplication.translate("MainWindow", "F5", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.label_7.setText(QCoreApplication.translate("MainWindow", "Frames", None))
        self.label_5.setText(
            QCoreApplication.translate(
                "MainWindow",
                "middle-mouse or space to navigate, w: wireframe, s for solid",
                None,
            )
        )
        self.label_6.setText(QCoreApplication.translate("MainWindow", "Volumes:", None))
        self.pushButton_3.setText(
            QCoreApplication.translate("MainWindow", "Save selected ", None)
        )
        self.label_4.setText(QCoreApplication.translate("MainWindow", "as", None))
        self.comboBox.setItemText(
            0, QCoreApplication.translate("MainWindow", ".stl", None)
        )
        self.comboBox.setItemText(
            1, QCoreApplication.translate("MainWindow", ".obj", None)
        )

        # if QT_CONFIG(tooltip)
        self.widgetGraphics.setToolTip(
            QCoreApplication.translate(
                "MainWindow",
                'On touchpath: use "m" or space to navigate instead of middle-mouse button\n'
                "\n"
                "Hold middle mouse to rotate\n"
                "Shift + middle to pan\n"
                "Ctrl + middle to zoom\n"
                "B for box\n"
                "2/3 for 2d/3d",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.Mesh),
            QCoreApplication.translate("MainWindow", "Mesh", None),
        )
        self.label_11.setText(
            QCoreApplication.translate("MainWindow", "Periods [s]", None)
        )
        self.label_16.setText(
            QCoreApplication.translate("MainWindow", "Water level elevation [m]", None)
        )
        self.teHeading.setText(
            QCoreApplication.translate("MainWindow", "np.linspace(0, 180, 9)", None)
        )
        self.label_9.setText(
            QCoreApplication.translate("MainWindow", "Mesh [file, in workfolder]", None)
        )
        self.teOutputFile.setText(
            QCoreApplication.translate("MainWindow", "my_model", None)
        )
        self.lblPeriods.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.cbSymmetryMesh.setText(
            QCoreApplication.translate(
                "MainWindow",
                "Use symmetry in XZ for mesh (only half of mesh defined)",
                None,
            )
        )
        self.cbLid.setText(
            QCoreApplication.translate(
                "MainWindow",
                "Add lid at z=-0.01m (can not be used together with symmetry)",
                None,
            )
        )
        self.cbInf.setText(QCoreApplication.translate("MainWindow", "Infinite", None))
        self.pbShowMesh.setText(
            QCoreApplication.translate("MainWindow", "Show mesh", None)
        )
        self.label_20.setText(
            QCoreApplication.translate("MainWindow", "Output file names", None)
        )
        self.label_13.setText(
            QCoreApplication.translate("MainWindow", "Headings [degrees]", None)
        )
        self.tePeriods.setText(
            QCoreApplication.translate(
                "MainWindow", "[*np.linspace(0.5,10,num=20), 11,12,14,16,20]", None
            )
        )
        self.lblHeading.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.pbRunCapytaine.setText(
            QCoreApplication.translate("MainWindow", "Go!", None)
        )
        self.label_15.setText(
            QCoreApplication.translate("MainWindow", "Waterdepth [m]", None)
        )
        self.cbSymmetryHeadings.setText(
            QCoreApplication.translate(
                "MainWindow",
                "Use symmetry in XY for output (only headings 0...180 defined)",
                None,
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.Capytaine),
            QCoreApplication.translate("MainWindow", "Capytaine", None),
        )
        self.pbWorkFolder.setText(
            QCoreApplication.translate("MainWindow", "Workfolder:", None)
        )
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Help", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menuExamples.setTitle(
            QCoreApplication.translate("MainWindow", "Examples", None)
        )

    # retranslateUi
