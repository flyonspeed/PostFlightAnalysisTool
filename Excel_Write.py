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

column_def = []

# -----------------------------------------------------------------------------
# Column formats

def make_column_def_dict(df_name, output=True, hidden=False, tooltip="", col_color="", col_text=""):
    if col_text != "" and tooltip == "" :
        tooltip = df_name
    if col_text == "" :
        col_text = df_name

    return dict( df_name     = df_name, 
                 col_output  = output,
                 col_hide    = hidden,
                 col_text    = col_text,
                 col_color   = col_color,   # #RRGGBB
                 tooltip     = tooltip )

#column_def.append(make_column_def_dict("blank"))
#column_def.append(make_column_def_dict("msecSinceMidnite"))
column_def.append(make_column_def_dict("timeStamp"))
column_def.append(make_column_def_dict("Pfwd", hidden=True))
column_def.append(make_column_def_dict("PfwdSmoothed"))
column_def.append(make_column_def_dict("P45", hidden=True))
column_def.append(make_column_def_dict("P45Smoothed"))
column_def.append(make_column_def_dict("PStatic"))
column_def.append(make_column_def_dict("Palt"))
column_def.append(make_column_def_dict("IAS"))
column_def.append(make_column_def_dict("AngleofAttack",col_text="Primary AOA",col_color="#C0F0C0"))
column_def.append(make_column_def_dict("flapsPos",col_text="Flap Position"))
column_def.append(make_column_def_dict("DataMark", hidden=True))
column_def.append(make_column_def_dict("OAT"))
column_def.append(make_column_def_dict("TAS"))
column_def.append(make_column_def_dict("imuTemp", hidden=True))
column_def.append(make_column_def_dict("VerticalG"))
column_def.append(make_column_def_dict("LateralG"))
column_def.append(make_column_def_dict("ForwardG"))
column_def.append(make_column_def_dict("RollRate"))
column_def.append(make_column_def_dict("PitchRate"))
column_def.append(make_column_def_dict("YawRate"))
column_def.append(make_column_def_dict("Pitch"))
column_def.append(make_column_def_dict("Roll"))
column_def.append(make_column_def_dict("boomStaticRaw", hidden=True))
column_def.append(make_column_def_dict("boomDynamicRaw", hidden=True))
column_def.append(make_column_def_dict("boomAlphaRaw", hidden=True))
column_def.append(make_column_def_dict("boomBetaRaw", hidden=True))
column_def.append(make_column_def_dict("boomIAS", hidden=True))
column_def.append(make_column_def_dict("boomAge", hidden=True))
column_def.append(make_column_def_dict("vnAngularRateRoll", hidden=True))
column_def.append(make_column_def_dict("vnAngularRatePitch", hidden=True))
column_def.append(make_column_def_dict("vnAngularRateYaw", hidden=True))
column_def.append(make_column_def_dict("vnVelNedNorth", hidden=True))
column_def.append(make_column_def_dict("vnVelNedEast", hidden=True))
column_def.append(make_column_def_dict("vnVelNedDown", hidden=True))
column_def.append(make_column_def_dict("vnAccelFwd", hidden=True))
column_def.append(make_column_def_dict("vnAccelLat", hidden=True))
column_def.append(make_column_def_dict("vnAccelVert", hidden=True))
column_def.append(make_column_def_dict("vnYaw"))
column_def.append(make_column_def_dict("vnPitch"))
column_def.append(make_column_def_dict("vnRoll"))
column_def.append(make_column_def_dict("vnLinAccFwd", hidden=True))
column_def.append(make_column_def_dict("vnLinAccLat", hidden=True))
column_def.append(make_column_def_dict("vnLinAccVert", hidden=True))
column_def.append(make_column_def_dict("vnYawSigma", hidden=True))
column_def.append(make_column_def_dict("vnRollSigma", hidden=True))
column_def.append(make_column_def_dict("vnPitchSigma", hidden=True))
column_def.append(make_column_def_dict("vnGnssVelNedNorth", hidden=True))
column_def.append(make_column_def_dict("vnGnssVelNedEast", hidden=True))
column_def.append(make_column_def_dict("vnGnssVelNedDown", hidden=True))
column_def.append(make_column_def_dict("vnGnssLat"))
column_def.append(make_column_def_dict("vnGnssLon"))
column_def.append(make_column_def_dict("vnGPSFix"))
column_def.append(make_column_def_dict("vnDataAge", hidden=True))
column_def.append(make_column_def_dict("vnTimeUTC"))
column_def.append(make_column_def_dict("EarthVerticalG"))
column_def.append(make_column_def_dict("FlightPath"))
#column_def.append(make_column_def_dict("KalmanAlt"))
#column_def.append(make_column_def_dict("KalmanVSI"))
column_def.append(make_column_def_dict("VSI"))
column_def.append(make_column_def_dict("Altitude"))

column_def.append(make_column_def_dict("docsTimeStamp", hidden=True))
column_def.append(make_column_def_dict("docsPfwd", hidden=True))
column_def.append(make_column_def_dict("docsPfwdSmoothed"))
column_def.append(make_column_def_dict("docsP45", hidden=True))
column_def.append(make_column_def_dict("docsP45Smoothed"))
column_def.append(make_column_def_dict("docsPStatic"))
column_def.append(make_column_def_dict("docsPalt"))
column_def.append(make_column_def_dict("docsIAS"))
column_def.append(make_column_def_dict("docsAngleofAttack",col_text="Secondary AOA",col_color="#C0F0C0"))
column_def.append(make_column_def_dict("docsFlapsPos"))
column_def.append(make_column_def_dict("docsDataMark", hidden=True))
column_def.append(make_column_def_dict("docsImuTemp", hidden=True))
column_def.append(make_column_def_dict("docsVerticalG"))
column_def.append(make_column_def_dict("docsLateralG"))
column_def.append(make_column_def_dict("docsForwardG"))
column_def.append(make_column_def_dict("docsRollRate"))
column_def.append(make_column_def_dict("docsPitchRate"))
column_def.append(make_column_def_dict("docsYawRate"))
column_def.append(make_column_def_dict("docsPitch"))
column_def.append(make_column_def_dict("docsRoll"))
column_def.append(make_column_def_dict("efisIAS"))
column_def.append(make_column_def_dict("efisPitch"))
column_def.append(make_column_def_dict("efisRoll"))
column_def.append(make_column_def_dict("efisLateralG"))
column_def.append(make_column_def_dict("efisVerticalG"))
column_def.append(make_column_def_dict("efisPercentLift"))
column_def.append(make_column_def_dict("efisPalt"))
column_def.append(make_column_def_dict("efisVSI"))
column_def.append(make_column_def_dict("efisTime", hidden=True))
column_def.append(make_column_def_dict("docsEarthVerticalG"))
column_def.append(make_column_def_dict("docsFlightPath"))
#column_def.append(make_column_def_dict("docsKalmanAlt"))
#column_def.append(make_column_def_dict("docsKalmanVSI"))

column_def.append(make_column_def_dict("TASMS", hidden=True))
column_def.append(make_column_def_dict("TASFPS"))
column_def.append(make_column_def_dict("vnGndSpeed"))
column_def.append(make_column_def_dict("vnGndTrack"))
column_def.append(make_column_def_dict("PRatio"))
column_def.append(make_column_def_dict("boomAlphaDer",col_text="Boom AOA Derived",col_color="#C0F0C0"))
column_def.append(make_column_def_dict("v2CP3Inst"))
column_def.append(make_column_def_dict("v2CP3Smth"))
column_def.append(make_column_def_dict("v2AlphPitchCur"))
column_def.append(make_column_def_dict("v2AlphDyna"))
column_def.append(make_column_def_dict("v2AlphInstPitchCur"))
column_def.append(make_column_def_dict("v2AlphSmthIMUCur"))
column_def.append(make_column_def_dict("v3CP3Inst"))
column_def.append(make_column_def_dict("v3CP3Smth"))
column_def.append(make_column_def_dict("boomAlphDynaPitCur"))
column_def.append(make_column_def_dict("boomAlphDynaIMUCur"))
column_def.append(make_column_def_dict("boomAlphUpwaPitCur"))
column_def.append(make_column_def_dict("boomAlphUpwaIMUCur"))
column_def.append(make_column_def_dict("vnFltPth"))
column_def.append(make_column_def_dict("vnIVVI"))
column_def.append(make_column_def_dict("vnDerAlph",col_text="Ext IMU AOA Derived",col_color="#C0F0C0"))
column_def.append(make_column_def_dict("vnRollRateDeg"))
column_def.append(make_column_def_dict("vnRollRateSmthDeg"))
column_def.append(make_column_def_dict("vnPitchRateDeg"))
column_def.append(make_column_def_dict("vnPitchRateSmthDeg"))
column_def.append(make_column_def_dict("vnTHdg"))
column_def.append(make_column_def_dict("vnG"))
column_def.append(make_column_def_dict("vnGSmth"))
column_def.append(make_column_def_dict("vnBankAng"))
column_def.append(make_column_def_dict("TrnRateDeg"))
column_def.append(make_column_def_dict("TrnRadFt"))
column_def.append(make_column_def_dict("efisRollDisag"))
column_def.append(make_column_def_dict("efisPitchDisag"))
column_def.append(make_column_def_dict("efisPaltDisag"))
column_def.append(make_column_def_dict("v2IAS"))
column_def.append(make_column_def_dict("v2IASVs"))
column_def.append(make_column_def_dict("StallMarv2IAS"))
column_def.append(make_column_def_dict("v2CAS"))
column_def.append(make_column_def_dict("v2CASVs"))
column_def.append(make_column_def_dict("v2StallMarCAS"))
column_def.append(make_column_def_dict("EFISIAS"))
column_def.append(make_column_def_dict("EFISIASVs"))
column_def.append(make_column_def_dict("efisStallMarIAS"))
column_def.append(make_column_def_dict("efisCAS"))
column_def.append(make_column_def_dict("efisCASVs"))
column_def.append(make_column_def_dict("efisStallMarCAS"))
column_def.append(make_column_def_dict("AlphMar"))
column_def.append(make_column_def_dict("AbsAlph"))
column_def.append(make_column_def_dict("AbsAlphMar"))
column_def.append(make_column_def_dict("efisCASVsG"))
column_def.append(make_column_def_dict("efisStallMarCASG"))

# -----------------------------------------------------------------------------

def to_excel(dataframe_groups, output_filename):
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.ExcelWriter.html
    # https://xlsxwriter.readthedocs.io/

    num_groups     = len(dataframe_groups.keys())
    curr_group_idx = 1

    writer = pd.ExcelWriter(output_filename)

#    with pd.ExcelWriter(output_filename) as writer:
    for group_key in dataframe_groups.keys():
        datamark_sheet_name = "DM{}".format(group_key)
        print("  Sheet '{}' ({} of {}) ...".format(datamark_sheet_name, curr_group_idx, num_groups))

        # Make list of columns to output and headers to use
        col_output_list = []
        col_header_list = []
        for col_fmt in column_def:
            col_output_list.append(col_fmt["df_name"])
            col_header_list.append(col_fmt["col_text"])

        # Make a blank column just in case
        b_series = pd.Series(index= dataframe_groups[group_key].index, dtype='float64')
        out_df = dataframe_groups[group_key]

        # Fix up missing and extra columns
        df_columns = dataframe_groups[group_key].columns.values.tolist()
        for output_column_name in col_output_list:
            if output_column_name not in df_columns:
                print("Missing column - ", output_column_name)
              # out_df = out_df.assign(output_column_name=b_series)
              # out_df[output_column_name]=b_series.values
                out_df = out_df.assign(**{output_column_name:b_series})

        # Write the dataframe to the spreadsheet
        out_df.to_excel(writer, sheet_name=datamark_sheet_name, 
                        header=col_header_list, columns=col_output_list,
                        index_label="msecSinceMidnite")

        curr_group_idx += 1
        #if curr_group_idx == 3:
        #    break;

    # Do some worksheet formatting

    for worksheet in writer.sheets:
        # format_sheet(writer.sheets[worksheet])
        dm_sheet = writer.sheets[worksheet]

        # Format each column
        for col_idx in range(len(column_def)):

            # Add tooltip
#            if column_def[col_idx]["tooltip"] != "":
#                dm_sheet.write_url(0, col_idx+1, "", None, column_def[col_idx]["col_text"], column_def[col_idx]["tooltip"])
 
            # Add column color
            if column_def[col_idx]["col_color"] != "":
                col_format = writer.book.add_format()
                col_format.set_bg_color(column_def[col_idx]["col_color"])
                col_format.set_bold()
                dm_sheet.write_string(0, col_idx+1, column_def[col_idx]["col_text"], col_format)

            # Hide columns
            if column_def[col_idx]["col_hide"] == True:
                dm_sheet.set_column(col_idx+1, col_idx+1, None, None, {'hidden':1})

        # Freeze the top row
        dm_sheet.freeze_panes(1,0)

    writer.close()


# =============================================================================

if __name__=='__main__':
    test_filename = "C:/Users/bob/OneDrive/Documents/sandbox/FlyONSPEED/Flight Test Data/RV-4/2022-05-10 Data/2022-05-10 - Base.xlsx"
    workbook = xw.Workbook(test_filename)
    #for sheet in workbook.worksheets():
    #    format_sheet(sheet)
    workbook.close()
