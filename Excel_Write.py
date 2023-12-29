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

col_format = []

# -----------------------------------------------------------------------------
# Column formats

def make_col_format_dict(column, df_name, output, hidden, col_name):
    return dict( column      = column,
                 df_name     = df_name, 
                 col_output  = output,
                 col_hide    = hidden,
                 col_name    = col_name )

#col_format.append(make_col_format_dict(" A","msecSinceMidnite",True,False,"msec Since Midnite"))
col_format.append(make_col_format_dict(" B","timeStamp",True,False,"timeStamp"))
col_format.append(make_col_format_dict(" C","Pfwd",True,False,"Pfwd"))
col_format.append(make_col_format_dict(" D","PfwdSmoothed",True,False,"PfwdSmoothed"))
col_format.append(make_col_format_dict(" E","P45",True,False,"P45"))
col_format.append(make_col_format_dict(" F","P45Smoothed",True,False,"P45Smoothed"))
col_format.append(make_col_format_dict(" G","PStatic",True,False,"PStatic"))
col_format.append(make_col_format_dict(" H","Palt",True,False,"Palt"))
col_format.append(make_col_format_dict(" I","IAS",True,False,"IAS"))
col_format.append(make_col_format_dict(" J","AngleofAttack",True,False,"Angle of Attack"))
col_format.append(make_col_format_dict(" K","flapsPos",True,False,"Flaps Pos"))
col_format.append(make_col_format_dict(" L","DataMark",True,False,"DataMark"))
col_format.append(make_col_format_dict(" M","imuTemp",True,False,"imuTemp"))
col_format.append(make_col_format_dict(" N","VerticalG",True,False,"VerticalG"))
col_format.append(make_col_format_dict(" O","LateralG",True,False,"LateralG"))
col_format.append(make_col_format_dict(" P","ForwardG",True,False,"ForwardG"))
col_format.append(make_col_format_dict(" Q","RollRate",True,False,"RollRate"))
col_format.append(make_col_format_dict(" R","PitchRate",True,False,"PitchRate"))
col_format.append(make_col_format_dict(" S","YawRate",True,False,"YawRate"))
col_format.append(make_col_format_dict(" T","Pitch",True,False,"Pitch"))
col_format.append(make_col_format_dict(" U","Roll",True,False,"Roll"))
col_format.append(make_col_format_dict(" V","boomStaticRaw",True,False,"boomStaticRaw"))
col_format.append(make_col_format_dict(" W","boomDynamicRaw",True,False,"boomDynamicRaw"))
col_format.append(make_col_format_dict(" X","boomAlphaRaw",True,False,"boomAlphaRaw"))
col_format.append(make_col_format_dict(" Y","boomBetaRaw",True,False,"boomBetaRaw"))
col_format.append(make_col_format_dict(" Z","boomIAS",True,False,"boomIAS"))
col_format.append(make_col_format_dict("AA","boomAge",True,False,"boomAge"))
col_format.append(make_col_format_dict("AB","vnAngularRateRoll",True,False,"vnAngularRateRoll"))
col_format.append(make_col_format_dict("AC","vnAngularRatePitch",True,False,"vnAngularRatePitch"))
col_format.append(make_col_format_dict("AD","vnAngularRateYaw",True,False,"vnAngularRateYaw"))
col_format.append(make_col_format_dict("AE","vnVelNedNorth",True,False,"vnVelNedNorth"))
col_format.append(make_col_format_dict("AF","vnVelNedEast",True,False,"vnVelNedEast"))
col_format.append(make_col_format_dict("AG","vnVelNedDown",True,False,"vnVelNedDown"))
col_format.append(make_col_format_dict("AH","vnAccelFwd",True,False,"vnAccelFwd"))
col_format.append(make_col_format_dict("AI","vnAccelLat",True,False,"vnAccelLat"))
col_format.append(make_col_format_dict("AJ","vnAccelVert",True,False,"vnAccelVert"))
col_format.append(make_col_format_dict("AK","vnYaw",True,False,"vnYaw"))
col_format.append(make_col_format_dict("AL","vnPitch",True,False,"vnPitch"))
col_format.append(make_col_format_dict("AM","vnRoll",True,False,"vnRoll"))
col_format.append(make_col_format_dict("AN","vnLinAccFwd",True,False,"vnLinAccFwd"))
col_format.append(make_col_format_dict("AO","vnLinAccLat",True,False,"vnLinAccLat"))
col_format.append(make_col_format_dict("AP","vnLinAccVert",True,False,"vnLinAccVert"))
col_format.append(make_col_format_dict("AQ","vnYawSigma",True,False,"vnYawSigma"))
col_format.append(make_col_format_dict("AR","vnRollSigma",True,False,"vnRollSigma"))
col_format.append(make_col_format_dict("AS","vnPitchSigma",True,False,"vnPitchSigma"))
col_format.append(make_col_format_dict("AT","vnGnssVelNedNorth",True,False,"vnGnssVelNedNorth"))
col_format.append(make_col_format_dict("AU","vnGnssVelNedEast",True,False,"vnGnssVelNedEast"))
col_format.append(make_col_format_dict("AV","vnGnssVelNedDown",True,False,"vnGnssVelNedDown"))
col_format.append(make_col_format_dict("AW","vnGnssLat",True,False,"vnGnssLat"))
col_format.append(make_col_format_dict("AX","vnGnssLon",True,False,"vnGnssLon"))
col_format.append(make_col_format_dict("AY","vnGPSFix",True,False,"vnGPSFix"))
col_format.append(make_col_format_dict("AZ","vnDataAge",True,False,"vnDataAge"))
col_format.append(make_col_format_dict("BA","vnTimeUTC",True,False,"vnTimeUTC"))
col_format.append(make_col_format_dict("BB","EarthVerticalG",True,False,"EarthVerticalG"))
col_format.append(make_col_format_dict("BC","FlightPath",True,False,"FlightPath"))
col_format.append(make_col_format_dict("BD","KalmanAlt",True,False,"KalmanAlt"))
col_format.append(make_col_format_dict("BE","KalmanVSI",True,False,"KalmanVSI"))
col_format.append(make_col_format_dict("BF","docsTimeStamp",True,False,"docsTimeStamp"))
col_format.append(make_col_format_dict("BG","docsPfwd",True,False,"docsPfwd"))
col_format.append(make_col_format_dict("BH","docsPfwdSmoothed",True,False,"docsPfwdSmoothed"))
col_format.append(make_col_format_dict("BI","docsP45",True,False,"docsP45"))
col_format.append(make_col_format_dict("BJ","docsP45Smoothed",True,False,"docsP45Smoothed"))
col_format.append(make_col_format_dict("BK","docsPStatic",True,False,"docsPStatic"))
col_format.append(make_col_format_dict("BL","docsPalt",True,False,"docsPalt"))
col_format.append(make_col_format_dict("BM","docsIAS",True,False,"docsIAS"))
col_format.append(make_col_format_dict("BN","docsAngleofAttack",True,False,"docsAngleofAttack"))
col_format.append(make_col_format_dict("BO","docsFlapsPos",True,False,"docsFlapsPos"))
col_format.append(make_col_format_dict("BP","docsDataMark",True,False,"docsDataMark"))
col_format.append(make_col_format_dict("BQ","docsImuTemp",True,False,"docsImuTemp"))
col_format.append(make_col_format_dict("BR","docsVerticalG",True,False,"docsVerticalG"))
col_format.append(make_col_format_dict("BS","docsLateralG",True,False,"docsLateralG"))
col_format.append(make_col_format_dict("BT","docsForwardG",True,False,"docsForwardG"))
col_format.append(make_col_format_dict("BU","docsRollRate",True,False,"docsRollRate"))
col_format.append(make_col_format_dict("BV","docsPitchRate",True,False,"docsPitchRate"))
col_format.append(make_col_format_dict("BW","docsYawRate",True,False,"docsYawRate"))
col_format.append(make_col_format_dict("BX","docsPitch",True,False,"docsPitch"))
col_format.append(make_col_format_dict("BY","docsRoll",True,False,"docsRoll"))
col_format.append(make_col_format_dict("BZ","efisIAS",True,False,"efisIAS"))
col_format.append(make_col_format_dict("CA","efisPitch",True,False,"efisPitch"))
col_format.append(make_col_format_dict("CB","efisRoll",True,False,"efisRoll"))
col_format.append(make_col_format_dict("CC","efisLateralG",True,False,"efisLateralG"))
col_format.append(make_col_format_dict("CD","efisVerticalG",True,False,"efisVerticalG"))
col_format.append(make_col_format_dict("CE","efisPercentLift",True,False,"efisPercentLift"))
col_format.append(make_col_format_dict("CF","efisPalt",True,False,"efisPalt"))
col_format.append(make_col_format_dict("CG","efisVSI",True,False,"efisVSI"))
col_format.append(make_col_format_dict("CH","efisTime",True,False,"efisTime"))
col_format.append(make_col_format_dict("CI","docsEarthVerticalG",True,False,"docsEarthVerticalG"))
col_format.append(make_col_format_dict("CJ","docsFlightPath",True,False,"docsFlightPath"))
col_format.append(make_col_format_dict("CK","docsKalmanAlt",True,False,"docsKalmanAlt"))
col_format.append(make_col_format_dict("CL","docsKalmanVSI",True,False,"docsKalmanVSI"))
col_format.append(make_col_format_dict("CM","TAS",True,False,"TAS"))
col_format.append(make_col_format_dict("CN","TASMS",True,False,"TASMS"))
col_format.append(make_col_format_dict("CO","TASFPS",True,False,"TASFPS"))
col_format.append(make_col_format_dict("CP","vnGndSpeed",True,False,"vnGndSpeed"))
col_format.append(make_col_format_dict("CQ","vnGndTrack",True,False,"vnGndTrack"))
col_format.append(make_col_format_dict("CR","PRatio",True,False,"PRatio"))
col_format.append(make_col_format_dict("CS","boomAlphaDer",True,False,"boomAlphaDer"))
col_format.append(make_col_format_dict("CT","v2CP3Inst",True,False,"v2CP3Inst"))
col_format.append(make_col_format_dict("CU","v2CP3Smth",True,False,"v2CP3Smth"))
col_format.append(make_col_format_dict("CV","v2AlphPitchCur",True,False,"v2AlphPitchCur"))
col_format.append(make_col_format_dict("CW","v2AlphDyna",True,False,"v2AlphDyna"))
col_format.append(make_col_format_dict("CX","v2AlphInstPitchCur",True,False,"v2AlphInstPitchCur"))
col_format.append(make_col_format_dict("CY","v2AlphSmthIMUCur",True,False,"v2AlphSmthIMUCur"))
col_format.append(make_col_format_dict("CZ","v3CP3Inst",True,False,"v3CP3Inst"))
col_format.append(make_col_format_dict("DA","v3CP3Smth",True,False,"v3CP3Smth"))
col_format.append(make_col_format_dict("DB","boomAlphDynaPitCur",True,False,"boomAlphDynaPitCur"))
col_format.append(make_col_format_dict("DC","boomAlphDynaIMUCur",True,False,"boomAlphDynaIMUCur"))
col_format.append(make_col_format_dict("DD","boomAlphUpwaPitCur",True,False,"boomAlphUpwaPitCur"))
col_format.append(make_col_format_dict("DE","boomAlphUpwaIMUCur",True,False,"boomAlphUpwaIMUCur"))
col_format.append(make_col_format_dict("DF","vnFltPth",True,False,"vnFltPth"))
col_format.append(make_col_format_dict("DG","vnIVVI",True,False,"vnIVVI"))
col_format.append(make_col_format_dict("DH","vnDerAlph",True,False,"vnDerAlph"))
col_format.append(make_col_format_dict("DI","vnRollRateDeg",True,False,"vnRollRateDeg"))
col_format.append(make_col_format_dict("DJ","vnRollRateSmthDeg",True,False,"vnRollRateSmthDeg"))
col_format.append(make_col_format_dict("DK","vnPitchRateDeg",True,False,"vnPitchRateDeg"))
col_format.append(make_col_format_dict("DL","vnPitchRateSmthDeg",True,False,"vnPitchRateSmthDeg"))
col_format.append(make_col_format_dict("DM","vnTHdg",True,False,"vnTHdg"))
col_format.append(make_col_format_dict("DN","vnG",True,False,"vnG"))
col_format.append(make_col_format_dict("DO","vnGSmth",True,False,"vnGSmth"))
col_format.append(make_col_format_dict("DP","vnBankAng",True,False,"vnBankAng"))
col_format.append(make_col_format_dict("DQ","TrnRateDeg",True,False,"TrnRateDeg"))
col_format.append(make_col_format_dict("DR","TrnRadFt",True,False,"TrnRadFt"))
col_format.append(make_col_format_dict("DS","efisRollDisag",True,False,"efisRollDisag"))
col_format.append(make_col_format_dict("DT","efisPitchDisag",True,False,"efisPitchDisag"))
col_format.append(make_col_format_dict("DU","efisPaltDisag",True,False,"efisPaltDisag"))
col_format.append(make_col_format_dict("DV","v2IAS",True,False,"v2IAS"))
col_format.append(make_col_format_dict("DW","v2IASVs",True,False,"v2IASVs"))
col_format.append(make_col_format_dict("DX","StallMarv2IAS",True,False,"StallMarv2IAS"))
col_format.append(make_col_format_dict("DY","v2CAS",True,False,"v2CAS"))
col_format.append(make_col_format_dict("DZ","v2CASVs",True,False,"v2CASVs"))
col_format.append(make_col_format_dict("EA","v2StallMarCAS",True,False,"v2StallMarCAS"))
col_format.append(make_col_format_dict("EB","EFISIAS",True,False,"EFISIAS"))
col_format.append(make_col_format_dict("EC","EFISIASVs",True,False,"EFISIASVs"))
col_format.append(make_col_format_dict("ED","efisStallMarIAS",True,False,"efisStallMarIAS"))
col_format.append(make_col_format_dict("EE","efisCAS",True,False,"efisCAS"))
col_format.append(make_col_format_dict("EF","efisCASVs",True,False,"efisCASVs"))
col_format.append(make_col_format_dict("EG","efisStallMarCAS",True,False,"efisStallMarCAS"))
col_format.append(make_col_format_dict("EH","AlphMar",True,False,"AlphMar"))
col_format.append(make_col_format_dict("EI","AbsAlph",True,False,"AbsAlph"))
col_format.append(make_col_format_dict("EJ","AbsAlphMar",True,False,"AbsAlphMar"))
col_format.append(make_col_format_dict("EK","efisCASVsG",True,False,"efisCASVsG"))
col_format.append(make_col_format_dict("EL","efisStallMarCASG",True,False,"efisStallMarCASG"))

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
        for col_fmt in col_format:
            col_output_list.append(col_fmt["df_name"])
            col_header_list.append(col_fmt["col_name"])
        
        # Write the dataframe to the spreadsheet
        dataframe_groups[group_key].to_excel(writer, sheet_name=datamark_sheet_name, 
                                             header=col_header_list, columns=col_output_list,
                                             index_label="msecSinceMidnite")

        curr_group_idx += 1
        if curr_group_idx == 3:
            break;

    # Do some worksheet formatting
    for worksheet in writer.sheets:
        format_sheet(writer.sheets[worksheet])

    writer.close()


# -----------------------------------------------------------------------------
def format_sheet(dm_sheet):
    dm_sheet.freeze_panes(1,0)


# =============================================================================

if __name__=='__main__':
    test_filename = "C:/Users/bob/OneDrive/Documents/sandbox/FlyONSPEED/Flight Test Data/RV-4/2022-05-10 Data/2022-05-10 - Base.xlsx"
    workbook = xw.Workbook(test_filename)
    for sheet in workbook.worksheets():
        format_sheet(sheet)
    workbook.close()
