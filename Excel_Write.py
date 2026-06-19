# Excel_Write.py - Write and format Excel output files

# This Python file uses the following encoding: utf-8
import os
import sys
import io
import datetime

from pathlib import Path

import csv
import datetime
from tkinter.tix import COLUMN
import pandas as pd
import xlsxwriter as xw

import Excel_Columns as ExCol

# -----------------------------------------------------------------------------
# Write to Excel
# -----------------------------------------------------------------------------

def to_excel(dataframe_groups, output_filename):
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.ExcelWriter.html
    # https://xlsxwriter.readthedocs.io/

    num_groups     = len(dataframe_groups.keys())
    curr_group_idx = 1

    # Make list of columns to output and headers to use
    col_output_list = []
    col_header_list = []
    # col_data_defs   = ExCol.column_def[1:]
    col_data_defs   = ExCol.column_def
    col_data_defs.popitem(last=False)
    for col_fmt_key in col_data_defs:
        col_output_list.append(col_data_defs[col_fmt_key]["df_name"])
        col_header_list.append(col_data_defs[col_fmt_key]["col_text"])

    # Get reference to XlsxWriter object
    writer = pd.ExcelWriter(output_filename)

    # Make the output dataframes and write them
    # -----------------------------------------
#    with pd.ExcelWriter(output_filename) as writer:
    for group_key in dataframe_groups.keys():
        datamark_sheet_name = "DM{}".format(group_key)
        print("  Sheet '{}' ({} of {}) ...".format(datamark_sheet_name, curr_group_idx, num_groups))

        # Make a blank column just in case it is needed
        b_series = pd.Series(index= dataframe_groups[group_key].index, dtype='float64')
        out_df = dataframe_groups[group_key]

        # Step through the list of columns to output. Either find and copy
        # an existing data column or copy the blank column at each column 
        # position.
        df_columns = dataframe_groups[group_key].columns.values.tolist()
        for output_column_name in col_output_list:
            if output_column_name not in df_columns:
#                print("Missing column - ", output_column_name)
              # out_df = out_df.assign(output_column_name=b_series)
              # out_df[output_column_name]=b_series.values
                out_df = out_df.assign(**{output_column_name:b_series})

        # Write the dataframe to the spreadsheet
        # out_df.to_excel(writer, sheet_name=datamark_sheet_name, 
        #                 header=col_header_list, columns=col_output_list,
        #                 index_label="msecSinceMidnite")
        out_df.to_excel(writer, sheet_name=datamark_sheet_name, 
                        header=False, columns=col_output_list,
                        index_label="msecSinceMidnite", startrow=5)

        curr_group_idx += 1
        # if curr_group_idx == 2:
        #     break;

    # Do some worksheet formatting
    # ----------------------------

    # Note: once a cell format has been set it cannot be added to. You get to
    # set cell format once.
    
    # writer.sheets -> dict of sheet name strings
    # worksheet     -> one sheet name string
    # dm_sheet      -> xlsxwriter.worksheet.Worksheet
    # writer.book   -> xlsxwriter.workbook.Workbook
    
    for worksheet in writer.sheets:
        dm_sheet = writer.sheets[worksheet]

        # Add default top row formats
        sec_title_format = writer.book.add_format()
        sec_title_format.set_bold()

        hdr_row_format = writer.book.add_format()
        hdr_row_format.set_bold()
        hdr_row_format.set_text_wrap()
        hdr_row_format.set_align('top')
        hdr_row_format.set_align('center')
        dm_sheet.set_row(4, None, hdr_row_format)

        # Format each column header
        col_idx = 1
        for col_fmt_key in ExCol.column_def:

            ### Header row stuff

            # Setup header cell format 
            hdr_cell_format = writer.book.add_format()
            hdr_cell_format.set_bold()
            hdr_cell_format.set_text_wrap()
            hdr_cell_format.set_align('top')
            hdr_cell_format.set_align('center')

            # Add color
            if ExCol.column_def[col_fmt_key]["col_color"] != "":
                hdr_cell_format.set_bg_color(ExCol.column_def[col_fmt_key]["col_color"])

            # Add border
            if ExCol.column_def[col_fmt_key]["border"] == True:
                hdr_cell_format.set_right(2)

            # Write cell text and format
            if ExCol.column_def[col_fmt_key]["sec_title"] != "":
                dm_sheet.write_string(0, col_idx, ExCol.column_def[col_fmt_key]["sec_title"], sec_title_format)
            dm_sheet.write_string(3, col_idx, ExCol.column_def[col_fmt_key]["df_name"])
            dm_sheet.write_string(4, col_idx, ExCol.column_def[col_fmt_key]["col_text"], hdr_cell_format)

            # Write cell comment
            if ExCol.column_def[col_fmt_key]["equation"] != "":
                dm_sheet.write_comment(3, col_idx, "= "+ExCol.column_def[col_fmt_key]["equation"], {'font_size': 12, 'width' : 500})
            if ExCol.column_def[col_fmt_key]["comment"] != "":
                dm_sheet.write_comment(4, col_idx, ExCol.column_def[col_fmt_key]["comment"], {'font_size': 12, 'width' : 300})

            ### Column stuff
            col_format = writer.book.add_format()

            # Hide columns
            if ExCol.column_def[col_fmt_key]["col_hide"] == True:
                col_options = {'hidden':True}
            else:
                col_options = {}

            # Add column border
            if ExCol.column_def[col_fmt_key]["border"] == True:
                col_format.set_right(2)

            if ExCol.column_def[col_fmt_key]["num_format"] != "":
                col_format.set_num_format(ExCol.column_def[col_fmt_key]["num_format"])

            dm_sheet.set_column(col_idx, col_idx, 12, col_format, col_options)

            col_idx += 1


        # Freeze the top row
        dm_sheet.freeze_panes(5,0)


    writer.close()


# =============================================================================

# Test the Excel writer

if __name__=='__main__':
    test_filename = "Excel_Test.xlsx"

    # Make a test dataframe group
    data_array =  [
        { "priTimeStamp"     : 10000,
          "priPFwd"          : 1000,
          "priP45"           : 1000,
          "priPalt"          : 4000,
          "priIAS"           : 150,
          "priAngleOfAttack" : 3,
          "priDataMark"      : 0,
          "priTAS"           : "=I2*(1+(H2/1000*0.017))"}, 
        { "priTimeStamp"     : 10020,
          "priPFwd"          : 1005,
          "priP45"           : 1000,
          "priPalt"          : 4010,
          "priIAS"           : 160,
          "priAngleOfAttack" : 3.1,
          "priDataMark"      : 0,
          "priTAS"           : "=I2*(1+(H2/1000*0.017))" }, 
        { "priTimeStamp"     : 10040,
          "priPFwd"          : 1010,
          "priP45"           : 1000,
          "priPalt"          : 4100,
          "priIAS"           : 155,
          "priAngleOfAttack" : 3,
          "priDataMark"      : 1,
          "priTAS"           : "=I2*(1+(H2/1000*0.017))" }, 
        { "priTimeStamp"     : 10060,
          "priPFwd"          : 1015,
          "priP45"           : 1000,
          "priPalt"          : 4110,
          "priIAS"           : 165,
          "priAngleOfAttack" : 3,
          "priDataMark"      : 1,
          "priTAS"           : "=I2*(1+(H2/1000*0.017))" }, 
        ]            
    # print(data_array)

    index_time = [ 0, 20, 40, 80]
    dataframe  = pd.DataFrame(data_array, index_time)
    # print(dataframe)

    # Group the data by data mark
    datamark_groups = dataframe.groupby("priDataMark")

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

    print(dataframe_group)
    
    to_excel(dataframe_group, test_filename)

#    workbook = xw.Workbook(test_filename)
    #for sheet in workbook.worksheets():
    #    format_sheet(sheet)
 #   workbook.close()
    print("Excel_Write done!")
