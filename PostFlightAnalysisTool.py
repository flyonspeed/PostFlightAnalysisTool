# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 2020

@author: Bob Baggerman
"""

# pip install numpy
# pip install pandas
# pip install matplotlib
# pip install xlsxwriter


# Someday look at seaborn
# http://seaborn.pydata.org/index.html

import os
import math
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import V2_Reader
import Doc_Reader
import EFIS_Reader
import KML_Reader
import XPlane_Write
import Derived_Data

v2_dataframe   = None
docs_dataframe = None
efis_dataframe = None
kml_dataframe  = None

print_log = print

def set_logger(new_print_log):
    print_log = new_print_log


# ---------------------------------------------------------------------------
# Plot routines
# -----------------------------------------------------------------------------

# Both "plot_center_sec" and "plot_span_sec" are in seconds

def plot_Pfwd(plot_center_sec, plot_span_sec):
    
    print("  Get plot data ...")

    plot_center = merge_dataframe.index.get_loc(plot_center_sec*1000,method='nearest')
    plot_span   = plot_span_sec * 50
    plot_start  = int(plot_center - (plot_span / 2))
    plot_end    = int(plot_center + (plot_span / 2))
    
    ts          = pd.Series(merge_dataframe.iloc[plot_start:plot_end].index).div(1000)
    DynonPfwdSm = merge_dataframe.iloc[plot_start:plot_end]["Pfwd"]
    AlSysPfwdSm = merge_dataframe.iloc[plot_start:plot_end]["docsPfwd"]
    #DynonPfwdSm = merge_dataframe.iloc[plot_start:plot_end]["PfwdSmoothed"]
    #AlSysPfwdSm = merge_dataframe.iloc[plot_start:plot_end]["docsPfwdSmoothed"]
    
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

def read_docs(data_filenames, time_corrections):
    docs_dataframe = Doc_Reader.make_dataframe(data_filenames, time_corrections)
    return docs_dataframe

# -----------------------------------------------------------------------------

def read_efis(data_filename, time_correction):
    efis_dataframe = EFIS_Reader.make_dataframe(data_filename, time_correction)
    return docs_dataframe

# -----------------------------------------------------------------------------

def read_kml(data_filename):
    kml_dataframe = KML_Reader.make_dataframe(data_filename, 0)
    return kml_dataframe

# -----------------------------------------------------------------------------

def merge_data_files(v2_data_filenames, docs_data_filenames, docs_time_corrections, efis_data_filename, efis_time_correction, kml_data_filename):

    v2_dataframe   = pd.DataFrame()
    docs_dataframe = pd.DataFrame()
    efis_dataframe = pd.DataFrame()
    kml_dataframe  = pd.DataFrame()
    flt_dataframe  = pd.DataFrame()

    # Read the various data files
    if (v2_data_filenames != None) and (v2_data_filenames != ""):
        print_log("Read V2...")
        v2_dataframe = read_v2(v2_data_filenames)

    if (docs_data_filenames != None) and (docs_data_filenames != ""):
        print_log("Read Docs...")
        docs_dataframe = read_docs(docs_data_filenames, docs_time_corrections)

    if (efis_data_filename != None) and (efis_data_filename != ""):
        print_log("Read EFIS...")
        efis_dataframe = read_efis(efis_data_filename, efis_time_correction)

    if (kml_data_filename != None) and (kml_data_filename != ""):
        print_log("Read KML...")
        kml_dataframe = read_kml(kml_data_filename)

    print_log("Merge...")
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

    if kml_dataframe.empty == False:
        if flt_dataframe.empty:
            flt_dataframe = kml_dataframe
        else:
            flt_dataframe = flt_dataframe.merge(kml_dataframe, how='left', left_index=True, right_index=True)

    # Add ground speed and ground track
    if v2_dataframe.empty == False:
        print_log("Add derived data columns...")
        flt_dataframe = Derived_Data.add_derived_cols(flt_dataframe)

    print_log("Done")
    return flt_dataframe


# =============================================================================
# Main routine
# =============================================================================

if __name__=='__main__':

    # Choose what to do with the data
    make_csv        = False
    make_excel      = True
    make_plot       = False

    # Load aircraft data files
    output_dir           = ""
    file_timestamp       = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    
    #test_data_dir        = "G:/.shortcut-targets-by-id/1JEHdf2zPb_F1R0v-s94Ia2RZNGjPCk2n/Flight Test Data/RV-4 Data/2022-05-13 Data/"
    test_data_dir        = "C:/Users/bob/OneDrive/Documents/sandbox/FlyONSPEED/Flight Test Data/RV-4/2022-05-13 Data/"
    v2_data_filename     = (test_data_dir + "13 May 22 V2 Data/log_2.csv", \
                            test_data_dir + "13 May 22 V2 Data/log_3.csv", \
                            test_data_dir + "13 May 22 V2 Data/log_4.csv")
    doc_data_filename    = (test_data_dir + "13 May 22 Docs Box Data/log_3.csv", \
                            test_data_dir + "13 May 22 Docs Box Data/log_4.csv", \
                            test_data_dir + "13 May 22 Docs Box Data/log_5.csv", \
                            test_data_dir + "13 May 22 Docs Box Data/log_6.csv")
    efis_data_filename   = ""
    kml_data_filename    = ""
    output_filename_root = test_data_dir + output_dir + "2022-05-13"
    doc_time_correction  = (2.0, 2.1, 2.1, 2.1)
    efis_time_correction = 0.0
    test_plot_center     = 43000
    test_plot_span       = 4000

    merge_dataframe = merge_data_files(v2_data_filename, doc_data_filename, doc_time_correction, efis_data_filename, efis_time_correction, kml_data_filename)

    # Outputs
    # -------

    # Write the big master CSV
    if make_csv == True:
        # Make sure the output folder exists
        if not os.path.exists(test_data_dir + output_dir):
            os.makedirs(test_data_dir + output_dir)
            
        output_filename = output_filename_root + " - Merged " + file_timestamp + ".csv"
        print("Write " + output_filename + " ...")
        write_csv(merge_dataframe, output_filename)

    if make_excel == True:
        # Make sure the output folder exists
        if not os.path.exists(test_data_dir + output_dir):
            os.makedirs(test_data_dir + output_dir)
            
        # Write the individual datamark Excel tabs
        output_filename = output_filename_root + " - Merged " + file_timestamp + ".xlsx"
        print("Write " + output_filename + " ...")
        write_excel(merge_dataframe, output_filename)
        
    if make_plot == True:
        print("Data Time Span {0} to {1}".format(merge_dataframe.index[0], merge_dataframe.index[-1]))
        print("Plot ...")
        plot_Pfwd(test_plot_center, test_plot_span)

    print("Done!")