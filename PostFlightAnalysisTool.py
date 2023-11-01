# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 2020

@author: Bob Baggerman
"""

# pip install numpy
# pip install pandas
# pip install matplotlib
# pip install openpyxl or pip install xlsxwriter


# Someday look at seaborn
# http://seaborn.pydata.org/index.html

from msvcrt import kbhit
import os
import math
import datetime
import msvcrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import V2_Reader
import Doc_Reader
import EFIS_Reader
import Garmin_Reader
import KML_Reader
import XPlane_Write
import Derived_Data
import Utils as u

v2_dataframe     = None
docs_dataframe   = None
efis_dataframe   = None
garmin_dataframe = None
kml_dataframe    = None

# ---------------------------------------------------------------------------
# Plot routines
# -----------------------------------------------------------------------------

# Both "plot_center_sec" and "plot_span_sec" are in seconds

def plot_Pfwd(plot_center_sec, plot_span_sec):
    
    # print("  Get plot data ...")

    plot_center_msec = plot_center_sec * 1000
    # plot_center = merge_dataframe.index.get_loc(plot_center_msec,method='nearest')
    plot_center = merge_dataframe.index.get_indexer([plot_center_msec], method='nearest')
    plot_span   = plot_span_sec * 50
    plot_start  = int(plot_center - (plot_span / 2))
    if plot_start < 0:
        plot_start = 0
    plot_end    = int(plot_center + (plot_span / 2))
    if plot_end >= len(merge_dataframe):
        plot_end = len(merge_dataframe) - 1

    ts          = pd.Series(merge_dataframe.iloc[plot_start:plot_end].index).div(1000)
    #DynonPfwdSm = merge_dataframe.iloc[plot_start:plot_end]["Pfwd"]
    #AlSysPfwdSm = merge_dataframe.iloc[plot_start:plot_end]["docsPfwd"]
    DynonPfwdSm = merge_dataframe.iloc[plot_start:plot_end]["PfwdSmoothed"]
    AlSysPfwdSm = merge_dataframe.iloc[plot_start:plot_end]["docsPfwdSmoothed"]
    
    AlSysPfwdSmDer = AlSysPfwdSm.mul(1.15).add(50)
    
    #fig = plt.figure(figsize=(15.0, 15.0), dpi=300)
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(ts, DynonPfwdSm,    color='tab:blue',   label="DynonPfwdSm",        linewidth=1.0)
    ax.plot(ts, AlSysPfwdSmDer, color='tab:orange', label="docsPfwdSm Shifted", linewidth=1.0)
    plt.xlabel("Seconds since Midnight")
    plt.grid(True)
    plt.legend(framealpha=1.0)
    
    plt.show()
    
    return

# -----------------------------------------------------------------------------
# Output routines
# -----------------------------------------------------------------------------

def write_csv(flt_dataframe, output_filename):
    flt_dataframe.to_csv(output_filename, index_label="msecSinceMidnite")
    print("Write CSV done")


# -----------------------------------------------------------------------------

# Return a list of data marks in a dataframe
def data_marks(dataframe):

    # Group the data by data mark
    datamark_groups = dataframe.groupby("DataMark")

    # Make a numerically sorted list of data mark keys    
    dg_ikeys = []
    for group_key in datamark_groups.indices.keys():
        dg_ikeys.append(int(group_key))
    dg_ikeys.sort()

    return dg_ikeys


# -----------------------------------------------------------------------------

def datamark_dataframe(dataframe, datamark_num):

    # Group the data by data mark
    datamark_groups = dataframe.groupby("DataMark")

    first_line = datamark_groups.groups[datamark_num][0]
    last_line  = datamark_groups.groups[datamark_num][-1]
    
    return dataframe.loc[first_line:last_line]


# -----------------------------------------------------------------------------

# Slice a dataframe into a set of dataframes based on datamark groups
def slice_data(dataframe):
    
    # Group the data by data mark
    datamark_groups = dataframe.groupby("DataMark")

    # Make a numerically sorted list of data mark keys    
    dg_ikeys = []
    for group_key in datamark_groups.indices.keys():
        dg_ikeys.append(int(group_key))
    dg_ikeys.sort()

    # Make dataframes based on group start and stop times
    dataframe_group = {}
    for group_key in datamark_groups.groups.keys():
        first_line = datamark_groups.groups[group_key][0] #  - 2000
        last_line  = datamark_groups.groups[group_key][-1] # - 2000
        dataframe_group[group_key] = dataframe.loc[first_line:last_line]

    return dataframe_group

# ---------------------------------------------------------------------------

def write_excel(flt_dataframe, output_filename):

    # Write the individual datamark Excel tabs
    merge_dataframe_groups = slice_data(flt_dataframe)
   
    print("Write " + output_filename + " ...")
    num_groups     = len(merge_dataframe_groups.keys())
    curr_group_idx = 1
    with pd.ExcelWriter(output_filename) as writer:
        for group_key in merge_dataframe_groups.keys():
            datamark_sheet_name = "DM{}".format(group_key)
            print("  Sheet '{}' ({} of {}) ...".format(datamark_sheet_name, curr_group_idx, num_groups))
            merge_dataframe_groups[group_key].to_excel(writer, sheet_name=datamark_sheet_name, index_label="msecSinceMidnite")
            curr_group_idx += 1
    print("Write Excel done")
                
# ---------------------------------------------------------------------------

def write_xplane(flt_dataframe, output_filename):
    print("Write X-Plane " + output_filename + " ...")
    XPlane_Write.to_replay(flt_dataframe, output_filename)
    print("Write X-Plane done")

# -----------------------------------------------------------------------------
# Main read and merge routines
# -----------------------------------------------------------------------------

def read_v2(data_filenames):
    v2_dataframe = V2_Reader.make_dataframe(data_filenames)
    return v2_dataframe

# -----------------------------------------------------------------------------

def read_docs(data_filenames):
    docs_dataframe = Doc_Reader.make_dataframe(data_filenames)
    return docs_dataframe

# -----------------------------------------------------------------------------

def read_efis(data_filename, time_correction):
    efis_dataframe = EFIS_Reader.make_dataframe(data_filename, time_correction)
    return efis_dataframe

# -----------------------------------------------------------------------------

def read_garmin(data_filename, time_correction):
    garmin_dataframe = Garmin_Reader.make_dataframe(data_filename, time_correction)
    return garmin_dataframe

# -----------------------------------------------------------------------------

def read_kml(data_filename):
    kml_dataframe = KML_Reader.make_dataframe(data_filename, 0)
    return kml_dataframe

# -----------------------------------------------------------------------------

def merge_data_files(v2_data_filenames, docs_data_filenames, efis_data_filename, efis_time_correction, garmin_data_filename, garmin_time_correction, kml_data_filename):

    v2_dataframe     = pd.DataFrame()
    docs_dataframe   = pd.DataFrame()
    efis_dataframe   = pd.DataFrame()
    garmin_dataframe = pd.DataFrame()
    kml_dataframe    = pd.DataFrame()
    flt_dataframe    = pd.DataFrame()

    # Read the various data files
    if (v2_data_filenames != None) and (v2_data_filenames != ""):
        u.print_log("Read V2...")
        v2_dataframe = read_v2(v2_data_filenames)

    if (docs_data_filenames != None) and (docs_data_filenames != ""):
        u.print_log("Read Docs...")
        docs_dataframe = read_docs(docs_data_filenames)

    if (efis_data_filename != None) and (efis_data_filename != ""):
        u.print_log("Read EFIS...")
        efis_dataframe = read_efis(efis_data_filename, efis_time_correction)

    if (garmin_data_filename != None) and (garmin_data_filename != ""):
        u.print_log("Read Garmin...")
        garmin_dataframe = read_garmin(garmin_data_filename, garmin_time_correction)

    if (kml_data_filename != None) and (kml_data_filename != ""):
        u.print_log("Read KML...")
        kml_dataframe = read_kml(kml_data_filename)

    u.print_log("Merge...")
    if v2_dataframe.empty == False:
        if flt_dataframe.empty:
            flt_dataframe = v2_dataframe
        else:
            flt_dataframe = flt_dataframe.merge(v2_dataframe, how='left', left_index=True, right_index=True)

    if docs_dataframe.empty == False:
        if flt_dataframe.empty:
            flt_dataframe = docs_dataframe
        else:
            flt_dataframe = flt_dataframe.merge(docs_dataframe, how='left', left_index=True, right_index=True)

    if efis_dataframe.empty == False:
        if flt_dataframe.empty:
            flt_dataframe = efis_dataframe
        else:
            flt_dataframe = flt_dataframe.merge(efis_dataframe, how='left', left_index=True, right_index=True)

    if garmin_dataframe.empty == False:
        if flt_dataframe.empty:
            flt_dataframe = garmin_dataframe
        else:
            flt_dataframe = flt_dataframe.merge(garmin_dataframe, how='left', left_index=True, right_index=True)

    if kml_dataframe.empty == False:
        if flt_dataframe.empty:
            flt_dataframe = kml_dataframe
        else:
            flt_dataframe = flt_dataframe.merge(kml_dataframe, how='left', left_index=True, right_index=True)

    # Add data columns derived from existing columns
    if v2_dataframe.empty == False:
        u.print_log("Add derived data columns...")
        flt_dataframe = Derived_Data.add_derived_cols(flt_dataframe)

    return flt_dataframe


# =============================================================================
# Main routine
# =============================================================================

if __name__=='__main__':

    # Choose what to do with the data
    make_csv        = False
    make_excel      = False
    make_xplane     = False
    make_plot       = (make_csv == False) and (make_excel == False) and (make_xplane == False)

    # Load aircraft data files
    output_dir           = ""
    file_timestamp       = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    
    if True :
        test_data_dir          = "G:/.shortcut-targets-by-id/1JEHdf2zPb_F1R0v-s94Ia2RZNGjPCk2n/Flight Test Data/RV-4 Data/2023-10-29/"
        output_filename_root   = test_data_dir + output_dir + "2023-10-29"
        v2_data_dir            = "29 Oct 23 Cockpit Data/"
        docs_data_dir          = "29 Oct 23 Docs Data/"
        v2_data_filenames      = (test_data_dir + v2_data_dir + "log_4.csv") 
        docs_data_filenames    = ( \
                                  (test_data_dir + docs_data_dir + "log_4.csv", 1.0), \
                                  )
        efis_data_filename     = ""
        garmin_data_filename   = ""
        kml_data_filename      = ""
        efis_time_correction   = 0.0
        garmin_time_correction = 0.0
    else :
        test_data_dir          = "C:/Users/bob/OneDrive/Documents/sandbox/FlyONSPEED/Flight Test Data/RV-4/2022-05-10 Data/"
        v2_data_filenames      = (test_data_dir + "10 May 22 V2 Data/log_2.csv")
        docs_data_filenames    = ( \
                                  (test_data_dir + "10 May 22 Docs Data/log_3.csv", 0.0), \
                                  (test_data_dir + "10 May 22 Docs Data/log_4.csv", 0.0), \
                                  (test_data_dir + "10 May 22 Docs Data/log_5.csv", 0.0), \
                                  )
        efis_data_filename     = ""
        garmin_data_filename   = "" # test_data_dir + "log_20220602_172202_KTEW.csv"
        kml_data_filename      = ""
        output_filename_root   = test_data_dir + output_dir + "2022-05-10"
        efis_time_correction   = 0.0
        garmin_time_correction = 0.0

    #test_plot_center       = 43000
    #test_plot_span         = 4000

    #merge_dataframe = merge_data_files(v2_data_filename,                             \
    #                                   doc_data_filenames,                           \
    #                                   efis_data_filename,   efis_time_correction,   \
    #                                   garmin_data_filename, garmin_time_correction, \
    #                                   kml_data_filename)

    # Read the various data files
    v2_dataframe     = pd.DataFrame()
    docs_dataframe   = pd.DataFrame()
    # merge_dataframe  = pd.DataFrame()

    if (v2_data_filenames != None) and (v2_data_filenames != ""):
        u.print_log("Read V2...")
        v2_dataframe = read_v2(v2_data_filenames)

    if (docs_data_filenames != None) and (docs_data_filenames != ""):
        u.print_log("Read Docs...")
        docs_dataframe = read_docs(docs_data_filenames)


    # Outputs
    # -------
    make_plot = False
    while True:
        print("p - Plot")
        print("e - Excel")
        print("q - Quit")

        input = str(msvcrt.getch().decode('utf-8'))

        if input == 'q':
            break

        # Merge the various data frames
        u.print_log("Merge...")
        merge_dataframe  = pd.DataFrame()

        if v2_dataframe.empty == False:
            if merge_dataframe.empty:
                merge_dataframe = v2_dataframe
            else:
                merge_dataframe = merge_dataframe.merge(v2_dataframe, how='left', left_index=True, right_index=True)

        if docs_dataframe.empty == False:
            if merge_dataframe.empty:
                merge_dataframe = docs_dataframe
            else:
                merge_dataframe = merge_dataframe.merge(docs_dataframe, how='left', left_index=True, right_index=True)

        if v2_dataframe.empty == False:
#            u.print_log("Add derived data columns...")
            merge_dataframe = Derived_Data.add_derived_cols(merge_dataframe)

        # Write the big master CSV
        if (make_csv == True) or (input == 'c'):
            # Make sure the output folder exists
            if not os.path.exists(test_data_dir + output_dir):
                os.makedirs(test_data_dir + output_dir)
            
            output_filename = output_filename_root + " - Merged " + file_timestamp + ".csv"
            print("Write " + os.path.basename(output_filename) + " ...")
            write_csv(merge_dataframe, output_filename)

        if (make_excel == True) or (input == 'e'):
            # Make sure the output folder exists
            if not os.path.exists(test_data_dir + output_dir):
                os.makedirs(test_data_dir + output_dir)
            
            # Write the individual datamark Excel tabs
            output_filename = output_filename_root + " - Merged " + file_timestamp + ".xlsx"
            print("Write " + os.path.basename(output_filename) + " ...")
            write_excel(merge_dataframe, output_filename)
        
        if (make_xplane == True) or (input == 'x'):
            # Make sure the output folder exists
            if not os.path.exists(test_data_dir + output_dir):
                os.makedirs(test_data_dir + output_dir)
            
            # Write the individual datamark Excel tabs
            output_filename = output_filename_root + "XPlane " + file_timestamp + ".fdr"
            print("Write " + os.path.basename(output_filename) + " ...")
    #        write_xplane(merge_dataframe, output_filename)
            write_xplane(merge_dataframe.loc[44070360:44174860], output_filename)
        
        if (make_plot == True) or (input == 'p'):
            u.print_log("Data Time Span {0} to {1}".format(merge_dataframe.index[0], merge_dataframe.index[-1]))
            print("Plot ...")
            test_plot_center = int((merge_dataframe.index[-1] + merge_dataframe.index[0]) / (2 * 1000))
            test_plot_span   = int((merge_dataframe.index[-1] - merge_dataframe.index[0]) / 1000)
            plot_Pfwd(test_plot_center, test_plot_span)

    print("Done!")