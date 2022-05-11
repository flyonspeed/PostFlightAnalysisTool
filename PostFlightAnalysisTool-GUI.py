# This Python file uses the following encoding: utf-8
import os
import sys
import io
import datetime

from pathlib import Path

from PySide6.QtCore    import QFile, QFileInfo, QSettings, QDir
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QDialog, QMainWindow
from PySide6.QtUiTools import QUiLoader

import PostFlightAnalysisTool as pfat
import Merge_Plot as mp
import Utils

# -----------------------------------------------------------------------------
# Qt user interface class
# -----------------------------------------------------------------------------

class MainUI(QMainWindow):

    # --------------
    # Initialization
    # --------------

    def __init__(self):
        pfat.set_logger(self.print_log)

        super(MainUI, self).__init__()
        self.load_ui()

        self.qSettings = QSettings("FlyONSPEED", "PostFlightAnalysisTool")

        # Declare some object variables
#        self.working_dir   = "G:/.shortcut-targets-by-id/1JEHdf2zPb_F1R0v-s94Ia2RZNGjPCk2n/Flight Test Data/Bob's Stuff/2021-08-11 Data"
        self.working_dir       = self.qSettings.value("working_dir", "")
        self.v2_filename       = ""
        self.docs_filename     = ""
        self.efis_filename     = ""
        self.kml_filename      = ""
        self.data_marks        = []
        self.working_dataframe = None
#        self.flt_dataframe = None

        # Setup some UI elements
#        self.qUI.pushOpenDocsDataFile.setEnabled(False)
#        self.qUI.pushOpenEFISDataFile.setEnabled(False)
#        self.qUI.pushOpenOutputDataFile.setEnabled(False)
        self.qUI.pushMerge.setEnabled(True)
        self.qUI.pushWrite.setEnabled(True)
        self.qUI.sliderStart.setValue(0)
        self.qUI.sliderStop.setValue(self.qUI.sliderStop.maximum())

        # Connect UI signals to slots
        self.qUI.pushOpenV2DataFile.clicked.connect(self.push_v2_file)
        self.qUI.pushOpenDocsDataFile.clicked.connect(self.push_docs_file)
        self.qUI.pushOpenEFISDataFile.clicked.connect(self.push_efis_file)
        self.qUI.pushOpenKmlDataFile.clicked.connect(self.push_kml_file)
        self.qUI.pushMerge.clicked.connect(self.push_merge)
        self.qUI.pushWrite.clicked.connect(self.push_write)
        self.qUI.pushExit.clicked.connect(self.push_exit)
        self.qUI.comboDataMarks.currentIndexChanged.connect(self.change_datamark)
        self.qUI.sliderStart.valueChanged.connect(self.slider_changed_start)
        self.qUI.sliderStop.valueChanged.connect(self.slider_changed_stop)
        self.qUI.sliderStart.sliderReleased.connect(self.slider_released)
        self.qUI.sliderStop.sliderReleased.connect(self.slider_released)


    def load_ui(self):
        qLoader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "PostFlightAnalysisTool.ui")
        qUiFile = QFile(path)
        qUiFile.open(QFile.ReadOnly)
        self.qUI = qLoader.load(qUiFile, self)
        qUiFile.close()


    # -----------------------------
    # User interface event handlers
    # -----------------------------

    # File select handlers
    # --------------------

    def push_v2_file(self):
        (filename, filter) = QFileDialog.getOpenFileName(self, "Open V2", dir=self.working_dir, filter="CSV Files (*.csv);;All Files (*.*)")
        if filename != "":
            self.qUI.lineV2DataFile.setText(filename)
            self.working_dir = QFileInfo(filename).absolutePath()
            self.qSettings.setValue("working_dir", self.working_dir)

            # Enable other UI elements
            self.qUI.pushOpenDocsDataFile.setEnabled(True)
            self.qUI.pushOpenEFISDataFile.setEnabled(True)

            # Make a reasonable output file name
            base_name = QFileInfo(filename).completeBaseName()
#            self.qUI.lineOutputDataFile.setText(self.working_dir + "/" + base_name)

            #print("Reading V2...")
            #pfat.read_v2(self.qUI.lineV2DataFile.text())
            #print("Done")


    def push_docs_file(self): 
        (filename, filter) = QFileDialog.getOpenFileName(self, "Open Docs", dir=self.working_dir, filter="CSV Files (*.csv);;All Files (*.*)")
        if filename != "":
            self.qUI.lineDocsDataFile.setText(filename)
            self.working_dir = QFileInfo(filename).absolutePath()
            self.qSettings.setValue("working_dir", self.working_dir)

            self.qUI.pushMerge.setEnabled(True)

            #print("Reading Docs...")
            #pfat.read_docs(self.qUI.lineDocsDataFile.text(), self.qUI.spinDocsDelay.value())
            #print("Done")


    def push_efis_file(self):
        (filename, filter) = QFileDialog.getOpenFileName(self, "Open EFIS", dir=self.working_dir, filter="CSV Files (*.csv);;All Files (*.*)")
        if filename != "":
            self.qUI.lineEFISDataFile.setText(filename)
            self.working_dir = QFileInfo(filename).absolutePath()
            self.qSettings.setValue("working_dir", self.working_dir)

            self.qUI.pushMerge.setEnabled(True)

            #print("Reading EFIS...")
            #pfat.read_docs(self.qUI.lineEFISDataFile.text(), self.qUI.spinEfisDelay.value())
            #print("Done")


    def push_kml_file(self):
        (filename, filter) = QFileDialog.getOpenFileName(self, "Open KML", dir=self.working_dir, filter="KML Files (*.kml);;All Files (*.*)")
        if filename != "":
            self.qUI.lineKmlDataFile.setText(filename)
            self.working_dir = QFileInfo(filename).absolutePath()
            self.qSettings.setValue("working_dir", self.working_dir)

#            self.qUI.pushMerge.setEnabled(True)

            #print("Reading KML...")
            #pfat.read_docs(self.qUI.lineKmlDataFile.text())
            #print("Done")

    # Output event handlers
    # ---------------------

    def push_output_file(self):
        (filename, filter) = QFileDialog.getOpenFileName(self, "Select Output", dir=self.working_dir, filter="CSV Files (*.csv);;All Files (*.*)")
        if filename != "":
            self.qUI.lineOutputDataFile.setText(filename)


    def push_merge(self):
        self.print_log("Merge...")
        if True:
            v2_data_filename     = self.qUI.lineV2DataFile.text()

            docs_data_filename   = self.qUI.lineDocsDataFile.text()
            docs_time_correction = self.qUI.spinDocsDelay.value()

            efis_data_filename   = self.qUI.lineEFISDataFile.text()
            efis_time_correction = self.qUI.spinEfisDelay.value()

            kml_data_filename    = self.qUI.lineKmlDataFile.text()

            self.flt_dataframe   = pfat.merge_data_files(v2_data_filename, docs_data_filename, docs_time_correction, efis_data_filename, efis_time_correction, kml_data_filename)
            self.data_marks      = pfat.data_marks(self.flt_dataframe)

        else:
            self.data_marks.append(0)
            self.data_marks.append(2)
            self.data_marks.append(3)
            self.data_marks.append(6)
            self.data_marks.append(7)

        # Fill in the data marks combo
        self.qUI.comboDataMarks.clear()
        self.qUI.comboDataMarks.addItem("All", -1)
        for data_mark in self.data_marks:
            #print(data_mark)
            self.qUI.comboDataMarks.addItem("Data Mark {}".format(data_mark))

        self.print_log("Merge Done")


    def change_datamark(self, dm_index):
        if dm_index == 0:
            #print("DM index {}  ALL".format(dm_index))
            self.working_dataframe = self.flt_dataframe
        else:
            #print("DM index {}  DM {}".format(dm_index, self.data_marks[dm_index-1]))
            self.working_dataframe = pfat.datamark_dataframe(self.flt_dataframe, self.data_marks[dm_index-1])
        self.update_start_stop()

    def slider_changed_start(self, slider_value):
        # Make sure stop is greater than start
        if slider_value > self.qUI.sliderStop.value():
            self.qUI.sliderStop.setValue(slider_value)
        self.update_start_stop()

    def slider_changed_stop(self, slider_value):
        # Make sure start is less than stop
        if slider_value < self.qUI.sliderStart.value():
            self.qUI.sliderStart.setValue(slider_value)
        self.update_start_stop()

    def slider_released(self):
        start_index = int( len(self.working_dataframe.index) * self.qUI.sliderStart.value() / self.qUI.sliderStart.maximum())
        stop_index  = int((len(self.working_dataframe.index) * self.qUI.sliderStop.value()  / self.qUI.sliderStop.maximum()) - 1)


    def push_write(self):
        # Generate a starting file name
        # Get the containing folder name to use as a file name

#        qV2Dir = QDir(self.qUI.lineV2DataFile.text())
#        file_path = qV2Dir.absolutePath()
        file_path = self.working_dir
        file_dir_parts = file_path.split("/")

        # Get the current date and time string
        file_timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")

        # Make a proposed output filename
        output_filename = file_path + "/" + file_dir_parts[-2] + " - Merged " + file_timestamp

        # Get the output limits
        start_index = int( len(self.working_dataframe.index) * self.qUI.sliderStart.value() / self.qUI.sliderStart.maximum())
        stop_index  = int((len(self.working_dataframe.index) * self.qUI.sliderStop.value()  / self.qUI.sliderStop.maximum()) - 1)

        # Plot
        if self.qUI.radioPlot.isChecked() == True:
            self.print_log("Output Plot...")
            plt_window = mp.MergePlot(self.working_dataframe[start_index:stop_index])
            plt_window.setModal(True)
            plt_window.exec()
            plt_window.resize(600, 400)

        # CSV
        if self.qUI.radioMergedCsv.isChecked() == True:
            user_output_filename = None
            (user_output_filename, extension) = QFileDialog.getSaveFileName(dir=output_filename, filter="CSV Files (*.csv);;All Files (*.*)")
            #print(user_output_filename)
            if user_output_filename != None:
                self.print_log("Output Merged CSV...")
                pfat.write_csv(self.working_dataframe[start_index:stop_index], user_output_filename)

        # Excel
        if self.qUI.radioMergedExcel.isChecked() == True:
            (user_output_filename, extension) = QFileDialog.getSaveFileName(dir=output_filename, filter="Excel Files (*.xlsx);;All Files (*.*)")
            #print(user_output_filename)
            self.print_log("Output Merged Excel...")
            pfat.write_excel(self.working_dataframe[start_index:stop_index], user_output_filename)

        # X-Plane
        if self.qUI.radioXPlane.isChecked() == True:
            (user_output_filename, extension) = QFileDialog.getSaveFileName(dir=output_filename, filter="FDR Files (*.fdr);;All Files (*.*)")
            #print(user_output_filename)
            self.print_log("Output X-Plane FDR...")
            pfat.write_xplane(self.working_dataframe[start_index:stop_index], user_output_filename)

    # Other event handlers
    # --------------------

    def push_exit(self):
        print("Bye!")
        exit()


    # -----------------------------
    # Other utility routines
    # -----------------------------

    def update_start_stop(self):

        start_index = int( len(self.working_dataframe.index) * self.qUI.sliderStart.value() / self.qUI.sliderStart.maximum())
        stop_index  = int((len(self.working_dataframe.index) * self.qUI.sliderStop.value()  / self.qUI.sliderStop.maximum()) - 1)

        #self.qUI.labelStart.setText(pfat.time_msec_to_str(self.working_dataframe.index[start_index]))
        #self.qUI.labelStop.setText(pfat.time_msec_to_str(self.working_dataframe.index[stop_index]))
        self.qUI.labelStart.setText(Utils.milliseconds_to_timestr(self.working_dataframe.index[start_index]))
        self.qUI.labelStop.setText(Utils.milliseconds_to_timestr(self.working_dataframe.index[stop_index]))


    def print_log(self, *args):
        print(*args)
        output = io.StringIO()
        print(*args, file=output)
        self.qUI.labelMsg.setText(output.getvalue())
        output.close()


# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication([])
    widgetMain = MainUI()
    widgetMain.show()
    sys.exit(app.exec())
