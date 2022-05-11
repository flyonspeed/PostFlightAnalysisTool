
# https://www.pyqtgraph.org/
# https://www.pythonguis.com/tutorials/pyside6-embed-pyqtgraph-custom-widgets/

# This Python file uses the following encoding: utf-8
import os
import sys
import io
import datetime

from pathlib import Path

from PySide6.QtCore    import QFile, QFileInfo, QSettings, QDir
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QVBoxLayout, \
                              QHBoxLayout, QSpacerItem, QSizePolicy, QLineEdit, QLabel, QDialog
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtUiTools import QUiLoader

import pyqtgraph as pg

import csv
import pandas as pd

import Utils

# -----------------------------------------------------------------------------
# Qt chart interface class
# -----------------------------------------------------------------------------

#class MergePlot(QWidget):
class MergePlot(QDialog):

    # Initialization
    # --------------

    def __init__(self, dataframe):
        super().__init__()

        self.qSettings = QSettings("FlyONSPEED", "PostFlightAnalysisTool")

        # Save the data
        self.dataframe = dataframe

        self.layout_chart_dialog()

        # Connect UI signals to slots
        self.pushPlot.clicked.connect(self.push_plot)
        self.pushExit.clicked.connect(self.push_exit)


    def layout_chart_dialog(self):

        # Top controls layout
        self.pushPlot   = QPushButton("Pfwd / docsPfwd")
        self.pushLatLon = QPushButton("Lat / Lon")
        self.pushExit   = QPushButton("Exit")
        self.layoutTop  = QHBoxLayout()
        self.layoutTop.addWidget(self.pushPlot)
        self.layoutTop.addWidget(self.pushExit)
        self.layoutTop.addSpacerItem(QSpacerItem(10000,1, QSizePolicy.Expanding))

        # Create chart object
        self._plot_widget = pg.PlotWidget()
        self._plot_widget.setBackground((255, 255, 255))
        self._plot_widget.addLegend()
        self._plot_widget.showButtons()
        self._plot_widget.enableAutoRange()
        self._plot_widget.showGrid(x=True, y=True, alpha=0.2)

        ## Bottom controls layout
        #self.lineStartIdx = QLineEdit(self)
        #self.lineEndIdx   = QLineEdit(self)
        #self.labelIdxMin  = QLabel(self)
        #self.labelIdxMax  = QLabel(self)

        #self.layoutBottom = QHBoxLayout()
        #self.layoutBottom.addWidget(self.labelIdxMin)
        #self.layoutBottom.addWidget(self.lineStartIdx)
        #self.layoutBottom.addSpacerItem(QSpacerItem(10000,1, QSizePolicy.Expanding))
        #self.layoutBottom.addWidget(self.lineEndIdx)
        #self.layoutBottom.addWidget(self.labelIdxMax)

        #self.labelIdxMin.setText("{}".format(0))
        #self.labelIdxMax.setText("{}".format(len(self.dataframe.index-1)))
        #self.lineStartIdx.setText("{}".format(0))
        #self.lineEndIdx.setText("{}".format(len(self.dataframe.index-1)))

        # Build overall chart widget layout
        self.setLayout(QVBoxLayout())
        self.layout().addLayout(self.layoutTop)
        self.layout().addWidget(self._plot_widget)
        #self.layout().addLayout(self.layoutBottom)


    # User interface event handlers
    # -----------------------------

    def push_plot(self):

        self._plot_widget.clear()

        StartIdx = 0
        StopIdx  = len(self.dataframe.index-1)
        xd = (self.dataframe.index / 1000).values

#        axis = pg.DateAxisItem(orientation='bottom')
#        self._plot_widget.plot(axisItems={'bottom': axis})
#        self._plot_widget.plot(axisItems = {'bottom': pg.DateAxisItem()})

        yd1 = self.dataframe['Pfwd'].values
        self._plot_widget.plot(x=xd, y=yd1, name="Pfwd",     pen=pg.mkPen((0,0,255)))

        yd2 = self.dataframe['docsPfwd'].values
        self._plot_widget.plot(x=xd, y=yd2, name="docsPfwd", pen=pg.mkPen((0,255,0)))

#        yd3 = (self.dataframe['DataMark'] * 100).values
#        self._plot_widget.plot(x=xd, y=yd3, name="Data Mark", pen=pg.mkPen((0,0,0)))

        self._plot_widget.showGrid(x=True, y=True)
#        self._plot_widget.setAxisItem({'bottom': axis})


    def push_exit(self):
        print("Bye!")
        self.close()




# =============================================================================

if __name__=='__main__':

    app = QApplication([])

    # Add some data to the chart
    #print("Read Merged Data...")
    merge_filename = "Data/2021-08-11 Data - Merged 20211027T132508.csv"
    merge_dataframe = pd.read_csv(merge_filename)

    window = MergePlot(merge_dataframe)
    window.setModal(True)
    window.show()
    window.resize(800, 600)

    sys.exit(app.exec())

    print("Done!")
