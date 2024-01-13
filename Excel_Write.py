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

color_primary   = "#FFFF00"     # yellow
color_boom      = "#FFC000"     # brown
color_ins       = "#92D050"     # green
color_secondary = "#00B0F0"     # blue
color_efis      = "#D9D9D9"     # gray

bHide = False

#column_def.append(make_column_def_dict("msecSinceMidnite"))
#column_def.append(make_column_def_dict("blank"))

# Raw
column_def.append(make_column_def_dict("timeStamp",         col_color=color_primary,                 col_text="Primary Time Stamp (ms)"))
column_def.append(make_column_def_dict("Pfwd",              col_color=color_primary,   hidden=bHide, col_text="Primary PFWD (counts)"))
column_def.append(make_column_def_dict("PfwdSmoothed",      col_color=color_primary,                 col_text="Primary PFWD Smoothed (counts)"))
column_def.append(make_column_def_dict("P45",               col_color=color_primary,   hidden=bHide, col_text="Primary P45 (counts)"))
column_def.append(make_column_def_dict("P45Smoothed",       col_color=color_primary,                 col_text="Primary P45 Smoothed (counts)"))
column_def.append(make_column_def_dict("PStatic",           col_color=color_primary,                 col_text="Primary Static Pressure (mb)"))
column_def.append(make_column_def_dict("Palt",              col_color=color_primary,                 col_text="Primary Pressure Altitude (ft)"))
column_def.append(make_column_def_dict("IAS",               col_color=color_primary,                 col_text="Primary KIAS"))
column_def.append(make_column_def_dict("AngleofAttack",     col_color=color_primary,                 col_text="Primary AOA (deg FRL)"))
column_def.append(make_column_def_dict("flapsPos",          col_color=color_primary,                 col_text="Primary Flap Position (deg)"))
column_def.append(make_column_def_dict("DataMark",          col_color=color_primary,   hidden=bHide, col_text="Primary Data Mark"))
column_def.append(make_column_def_dict("OAT",               col_color=color_primary,                 col_text="Primary OAT (C)"))
column_def.append(make_column_def_dict("TAS",               col_color=color_primary,                 col_text="Primary KTAS"))
column_def.append(make_column_def_dict("imuTemp",           col_color=color_primary,   hidden=bHide, col_text="Primary IMU Temp (C)"))
column_def.append(make_column_def_dict("VerticalG",         col_color=color_primary,                 col_text="Primary IMU Vertical G"))
column_def.append(make_column_def_dict("LateralG",          col_color=color_primary,                 col_text="Primary IMU Lateral G"))
column_def.append(make_column_def_dict("ForwardG",          col_color=color_primary,                 col_text="Primary IMU Forward G"))
column_def.append(make_column_def_dict("RollRate",          col_color=color_primary,                 col_text="Primary IMU Roll Rate (deg/sec)"))
column_def.append(make_column_def_dict("PitchRate",         col_color=color_primary,                 col_text="Primary IMU Pitch Rate (deg/sec)"))
column_def.append(make_column_def_dict("YawRate",           col_color=color_primary,                 col_text="Primary IMU Yaw Rate (deg/sec)"))
column_def.append(make_column_def_dict("Pitch",             col_color=color_primary,                 col_text="Primary IMU Pitch (deg)"))
column_def.append(make_column_def_dict("Roll",              col_color=color_primary,                 col_text="Primary IMU Roll (deg)"))
column_def.append(make_column_def_dict("EarthVerticalG",    col_color=color_primary,                 col_text="Primary Earth Vertical G"))
column_def.append(make_column_def_dict("FlightPath",        col_color=color_primary,                 col_text="Primary Derived Flight Path Angle (deg)"))
column_def.append(make_column_def_dict("VSI",               col_color=color_primary,                 col_text="Primary Kalman Filtered IVVI (FPM)"))
column_def.append(make_column_def_dict("Altitude",          col_color=color_primary,                 col_text="Primary Kalman Filtered Altitude (ft)"))
                                                                                       
# Boom                                                                                 
column_def.append(make_column_def_dict("boomStaticRaw",     col_color=color_boom,                    col_text="Boom Static Pressure (counts)"))
column_def.append(make_column_def_dict("boomDynamicRaw",    col_color=color_boom,                    col_text="Boom Dynamic Pressure (counts)"))
column_def.append(make_column_def_dict("boomAlphaRaw",      col_color=color_boom,      hidden=bHide, col_text="Boom Alpha (counts)"))
column_def.append(make_column_def_dict("boomBetaRaw",       col_color=color_boom,      hidden=bHide, col_text="Boom Beta (counts)"))
column_def.append(make_column_def_dict("boomIAS",           col_color=color_boom,      hidden=bHide, col_text="Boom KIAS"))
column_def.append(make_column_def_dict("boomAge",           col_color=color_boom,                    col_text="Boom Age (ms)"))
                                                                                       
# GNSS/INS                                                                             
column_def.append(make_column_def_dict("vnAngularRateRoll", col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Roll Rate (rad/sec)"))
column_def.append(make_column_def_dict("vnAngularRatePitch",col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Pitch Rate (rad/sec)"))
column_def.append(make_column_def_dict("vnAngularRateYaw",  col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Yaw Rate (rad/sec)"))
column_def.append(make_column_def_dict("vnVelNedNorth",     col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Velocity North (m/sec)"))
column_def.append(make_column_def_dict("vnVelNedEast",      col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Velocity East (m/sec)"))
column_def.append(make_column_def_dict("vnVelNedDown",      col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Velocity Down (m/sec)"))
column_def.append(make_column_def_dict("vnAccelFwd",        col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Forward Accel (m/sec2)"))
column_def.append(make_column_def_dict("vnAccelLat",        col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Lateral Accel (m/sec2)"))
column_def.append(make_column_def_dict("vnAccelVert",       col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Vertical Accel (m/sec2)"))
column_def.append(make_column_def_dict("vnYaw",             col_color=color_ins,                     col_text="GNSS/INS Yaw (deg)"))
column_def.append(make_column_def_dict("vnPitch",           col_color=color_ins,                     col_text="GNSS/INS Pitch (deg)"))
column_def.append(make_column_def_dict("vnRoll",            col_color=color_ins,                     col_text="GNSS/INS Roll (deg)"))
column_def.append(make_column_def_dict("vnLinAccFwd",       col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Linear Accel Forward (m/sec2)"))
column_def.append(make_column_def_dict("vnLinAccLat",       col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Linear Accel Lateral (m/sec2)"))
column_def.append(make_column_def_dict("vnLinAccVert",      col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Linear Accel Vertical (m/sec2)"))
column_def.append(make_column_def_dict("vnYawSigma",        col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Yaw Sigma (deg)"))
column_def.append(make_column_def_dict("vnRollSigma",       col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Roll Sigma (deg)"))
column_def.append(make_column_def_dict("vnPitchSigma",      col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Pitch Sigma (deg)"))
column_def.append(make_column_def_dict("vnGnssVelNedNorth", col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Velocity North (m/sec)"))
column_def.append(make_column_def_dict("vnGnssVelNedEast",  col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Velocity East (m/sec)"))
column_def.append(make_column_def_dict("vnGnssVelNedDown",  col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Velocity Down (m/sec)"))
column_def.append(make_column_def_dict("vnGnssLat",         col_color=color_ins,                     col_text="GNSS/INS Latitude (+ North - South)"))
column_def.append(make_column_def_dict("vnGnssLon",         col_color=color_ins,                     col_text="GNSS/INS Longitude (+ East - West)"))
column_def.append(make_column_def_dict("vnGPSFix",          col_color=color_ins,                     col_text="GNSS/INS GPS Quality"))
column_def.append(make_column_def_dict("vnDataAge",         col_color=color_ins,       hidden=bHide, col_text="GNSS/INS Data Age (ms)"))
column_def.append(make_column_def_dict("vnTimeUTC",         col_color=color_ins,                     col_text="GNSS/INS Zulu Time"))

# Secondary ("Docs")
column_def.append(make_column_def_dict("docsTimeStamp",     col_color=color_secondary, hidden=bHide, col_text="Secondary Time Stamp (ms)"))
column_def.append(make_column_def_dict("docsPfwd",          col_color=color_secondary, hidden=bHide, col_text="Secondary PFWD (counts)"))
column_def.append(make_column_def_dict("docsPfwdSmoothed",  col_color=color_secondary, hidden=bHide, col_text="Secondary PFWD Smoothed (counts)"))
column_def.append(make_column_def_dict("docsP45",           col_color=color_secondary, hidden=bHide, col_text="Secondary P45 (counts)"))
column_def.append(make_column_def_dict("docsP45Smoothed",   col_color=color_secondary,               col_text="Secondary P45 Smoothed (counts)"))
column_def.append(make_column_def_dict("docsPStatic",       col_color=color_secondary,               col_text="Secondary Static Pressure (mb)"))
column_def.append(make_column_def_dict("docsPalt",          col_color=color_secondary,               col_text="Secondary Pressure Altitude (ft)"))
column_def.append(make_column_def_dict("docsIAS",           col_color=color_secondary,               col_text="Secondary KIAS"))
column_def.append(make_column_def_dict("docsAngleofAttack", col_color=color_secondary,               col_text="Secondary AOA (not accurate) See Derived Data"))
column_def.append(make_column_def_dict("docsFlapsPos",      col_color=color_secondary, hidden=bHide, col_text="Secondary Flap Position (disabled)"))
column_def.append(make_column_def_dict("docsDataMark",      col_color=color_secondary, hidden=bHide, col_text="Secondary Data Mark (disabled)"))
column_def.append(make_column_def_dict("docsOAT",           col_color=color_secondary, hidden=bHide, col_text="Secondary OAT (C)"))
column_def.append(make_column_def_dict("docsTAS",           col_color=color_secondary, hidden=bHide, col_text="Secondary KTAS"))
column_def.append(make_column_def_dict("docsImuTemp",       col_color=color_secondary, hidden=bHide, col_text="Secondary IMU Temp C"))
column_def.append(make_column_def_dict("docsVerticalG",     col_color=color_secondary,               col_text="Secondary Vertical G"))
column_def.append(make_column_def_dict("docsLateralG",      col_color=color_secondary,               col_text="Secondary Lateral G"))
column_def.append(make_column_def_dict("docsForwardG",      col_color=color_secondary,               col_text="Secondary Forward G"))
column_def.append(make_column_def_dict("docsRollRate",      col_color=color_secondary,               col_text="Secondary IMU Roll Rate (deg/sec)"))
column_def.append(make_column_def_dict("docsPitchRate",     col_color=color_secondary,               col_text="Secondary IMU Pitch Rate (deg/sec)"))
column_def.append(make_column_def_dict("docsYawRate",       col_color=color_secondary,               col_text="Secondary IMU Yaw Rate (deg/sec)"))
column_def.append(make_column_def_dict("docsPitch",         col_color=color_secondary,               col_text="Secondary IMU Pitch (deg)"))
column_def.append(make_column_def_dict("docsRoll",          col_color=color_secondary,               col_text="Secondary IMU Roll (deg)"))
column_def.append(make_column_def_dict("docsEarthVerticalG",col_color=color_secondary,               col_text="Secondary Earth Vertical G"))
column_def.append(make_column_def_dict("docsFlightPath",    col_color=color_secondary,               col_text="Secondary Derived Flight Path Angle (deg)"))
column_def.append(make_column_def_dict("docsVSI",           col_color=color_secondary,               col_text="Secondary Kalman Filtered IVVI (FPM)"))
column_def.append(make_column_def_dict("docsAltitude",      col_color=color_secondary,               col_text="Secondary Kalman Filtered Altitude (ft)"))

# EFIS
column_def.append(make_column_def_dict("efisIAS",           col_color=color_efis,                    col_text="EFIS KIAS"))
column_def.append(make_column_def_dict("efisPitch",         col_color=color_efis,                    col_text="EFIS Pitch (deg)"))
column_def.append(make_column_def_dict("efisRoll",          col_color=color_efis,                    col_text="EFIS Roll (deg)"))
column_def.append(make_column_def_dict("efisLateralG",      col_color=color_efis,                    col_text="EFIS Lateral G"))
column_def.append(make_column_def_dict("efisVerticalG",     col_color=color_efis,                    col_text="EFIS Vertical G"))
column_def.append(make_column_def_dict("efisPercentLift",   col_color=color_efis,                    col_text="EFIS % Lift (not accurate)"))
column_def.append(make_column_def_dict("efisPalt",          col_color=color_efis,                    col_text="EFIS Pressure Altitude (ft)"))
column_def.append(make_column_def_dict("efisVSI",           col_color=color_efis,                    col_text="EFIS VSI (FPM)"))
column_def.append(make_column_def_dict("efisTime",          col_color=color_efis,      hidden=bHide, col_text="EFIS Zulu Time"))

# Area 1 - Time, GPS Gnd Speed and Track
column_def.append(make_column_def_dict("vnTimeUTC",                                                  col_text="GNSS/INS Zulu Time"))
column_def.append(make_column_def_dict("vnGndSpeed",                                                 col_text="GNSS/INS Ground Speed (kts)"))
column_def.append(make_column_def_dict("vnGndTrack",                                                 col_text="GNSS/INS True Ground Track (deg)"))

# Area 2 - Convert GNSS/INS Data from Metric to English Measurements and G
column_def.append(make_column_def_dict("blank1 ", col_text="GNSS/INS (NED) Velocity North (ft/sec)"))
column_def.append(make_column_def_dict("blank2 ", col_text="GNSS/INS (NED) Velocity East (ft/sec)"))
column_def.append(make_column_def_dict("blank3 ", col_text="GNSS/INS (NED) Velocity Down (ft/sec)"))
column_def.append(make_column_def_dict("blank4 ", col_text="GNSS/INS Forward G"))
column_def.append(make_column_def_dict("blank5 ", col_text="GNSS/INS Lateral G"))
column_def.append(make_column_def_dict("blank6 ", col_text="GNSS/INS Linear Acceleration Forward (G)"))
column_def.append(make_column_def_dict("blank7 ", col_text="GNSS/INS Linear Acceleration Lateral (G)"))
column_def.append(make_column_def_dict("blank8 ", col_text="GNSS/INS Linear Acceleration Vertical (G)"))

# Area 3 -  Pressures (PSI and mb) and Coefficient of Pressures
# "Primary Pfwd Smoothed (PSI)"
# "Primary P45 Smoothed (PSI)"
# "Secondary Pfwd Smoothed (PSI)"
# "Secondary P45 Smoothed (PSI)"
# "Primary Pfwd Smoothed (mb)"
# "Primary P45 Smoothed (mb)"
# "Secondary Pfwd Smoothed (mb)"
# "Secondary P45 Smoothed (mb)"
# "Primary P45/Pfwd Instantaneos"
# "Primary P45/Pfwd Smoothed"
# "Secondary P45/Pfwd Instantaneous"
# "Secondary P45/Pfwd Smoothed"
# "Primary ATAN2 (Pfwd,P45) Instantaneous"
# "Primary ATAN2 (Pfwd,P45) Smoothed"
# "Secondary ATAN2 (Pfwd,P45) Instantaneous"
# "Secondary ATAN2 (Pfwd,P45) Smoothed"
# "Primary (Pfwd-P45)/q Smoothed (PSI)"
# "Secondary (Pfwd-P45)/q Smoothed (PSI)"

# Area 4 - Atmospherics
# "OAT Deg F"
# "Standard Temp (deg F)"
# "Standard Temp Delta (deg F)"
# "Standard Temp (deg C)"
# "Standard Temp Delta (deg C)"
# "Standard Temp (deg K)"
# "Pressure Ratio"
# "Density Ratio"
# "Density Altitude (ft)"
# "Winds at Test Altitude"

# Area 5 - Air Data Boom Uncorrected Angles, Pressures and Airspeeds
# "Air Data Boom Static Pressure (mb)"
# "Air Data Boom Dynamic Pressure (mb)"
# "Air Data Boom Uncorrected Alpha Angle (deg)"
# "Air Data Boom Uncorrected Beta Angle (deg)"
# "Air Data Boom KIAS"
# "Air Data Boom KTAS Method 1 (using Density Ratio)"
# "Air Data Boom KTAS Method 2 (Temp and Pressure)"
# "Air Data Boom Pressure Altitude (ft)"

# Area 6 - Primary System Airspeeds
# "Primary KIAS"
# "Primary KIAS Smoothed"
# "Primary KIAS Smoothed ROC (dKIAS/dt)"
# "Primary KCAS"
# "Primary KCAS Smoothed"
# "Primary KCAS Smoothed ROC (dKCAS/dt)"
# "Primary KTAS"
# "Primary KTAS Smoothed"
# "Primary KTAS Smoothed ROC (dTAS/dt)"
column_def.append(make_column_def_dict("TASMS",                                                      col_text="Primary TAS (M/Sec)"))
column_def.append(make_column_def_dict("TASFPS",                                                     col_text="Primary TAS (Ft/Sec)"))

# Area 7 - Attitude, Performance and G
# "GNSS/INS Pitch (deg, + Up, - Down)"
# "GNSS/INS Pitch Rate (deg/sec)"
# "GNSS/INS Pitch Rate Smoothed (deg/sec)"
# "GNSS/INS Roll (deg, - Left, + Right)"
# "GNSS/INS Roll Rate (deg/sec)"
# "GNSS/INS Roll Rate Smoothed (deg/sec)"
# "Air Data Boom Yaw Angle (deg, + Left Yaw, - Right Yaw)"
# "GNSS/INS Yaw Rate (deg/sec)"
# "GNSS/INS Yaw Rate Smoothed (deg/sec)"
# "GNSS/INS Flight Path Angle (deg)"
# "GNSS/INS Flight Path Angle Corrected (deg)"
# "GNSS/INS True Heading (deg)"
# "GNSS/INS IVVI (FPM)"
# "GNSS/INS Turn Rate (deg/sec)"
# "GNSS/INS Turn Rate Smoothed (deg/sec)"
# "GNSS/INS Turn Radius (ft)"
# "Primary G Smoothed"
# "Secondary G Smoothed"
# "GNSS/INS G"
# "GNSS/INS G Smoothed"

# Area 8 - Angle of Attack
# "GNSS/INS Derived AOA (deg)"
# "GNSS/INS Derived AOA Smoothed (deg)"
# "GNSS/INS Derived AOA Rate (deg/sec)"
# "GNSS/INS Derived AOA Rate Smoothed (deg/sec)"
# "Air Data Boom Corrected AOA (deg)"
# "Air Data Boom Corrected AOA Smoothed (deg)"
# "Air Data Boom Corrected AOA Rate (deg/sec)"
# "Air Data Boom Corrected AOA Rate Smoothed (deg/sec)"
# "Cockpit Recorded AOA (deg)"
# "Cockpit Recorded AOA Smoothed (deg)"
# "Cockpit Recorded AOA Rate (deg/sec)"
# "Cockpit Recorded AOA Rate Smoothed (deg/sec)"
# "Primary AOA (deg)"
# "Primary AOA Smoothed (deg)"
# "Primary AOA Rate (deg/sec)"
# "Primary AOA Rate Smoothed (deg/sec)"
# "Secondary AOA (deg)"
# "Secondary AOA Smoothed (deg)"
# "Secondary AOA Rate (deg/sec)"
# "Secondary AOA Rate Smoothed (deg/sec)"
# "Primary Absolute Alpha (deg)"
# "Primary Absolute Alpha Smoothed (deg)"

# Area 9 - Side Slip
# "Air Data Boom Uncorrected Beta Angle (deg)"
# "Air Data Boom Corrected Yaw (deg)"
# "Air Data Boom Corrected Yaw Smoothed (deg)"
# "Air Data Boom Corrected Yaw Rate (deg/sec)"
# "Air Data Boom Corrected Yaw Rate Smoothed (deg/sec)"

# Area 10 - AOA Accuracy
# "Air Data Boom vs Cockpit Recorded AOA (deg)"
# "GNSS/INS Derived vs Cockpit Recorded AOA (deg)"
# "Air Data Boom vs Primary AOA (deg)"
# "GNSS/INS Derived vs Primary AOA (deg)"
# "Air Data Boom vs Secondary AOA (deg)"
# "GNSS/INS Derived vs Secondary AOA (deg)"

# Area 11 - Disagreements
# "Primary vs GNSS/INS Roll Disag (deg)"
# "Primary vs GNSS/INS Pitch Disag (deg)"
# "Primary vs EFIS Pressure Altitude Disag (ft)"
# "Primary vs EFIS KIAS Disag"
# "Primary vs Air Data Boom Pressure Altitude Disag (ft)"
# "Primary vs Air Data Boom KIAS Disag"
# "Primary KTAS vs Air Data Boom KTAS Disag"

# Area 12 - Aerodynamic Margin
# "Primary KIAS Stall Speed"
# "Primary KIAS Stall Margin (kts)"
# "Primary AOA Smoothed Stall Margin (deg)"
# "Cockpit Recorded AOA Smoothed Stall Margin (deg)"
# "Primary Absolute Alpha Smoothed Stall Margin (deg)"
# "Secondary KIAS Stall Speed"
# "Secondary KIAS Stall Margin (kts)"
# "Secondary AOA Smoothed Stall Margin (deg)"

# Columns not used
  # column_def.append(make_column_def_dict("PRatio",                                                     col_text=""))
# column_def.append(make_column_def_dict("boomAlphaDer",                                               col_text="Boom AOA Derived"))
# column_def.append(make_column_def_dict("v2CP3Inst",                                                  col_text=""))
# column_def.append(make_column_def_dict("v2CP3Smth",                                                  col_text=""))
# column_def.append(make_column_def_dict("v2AlphPitchCur",                                             col_text=""))
# column_def.append(make_column_def_dict("v2AlphDyna",                                                 col_text=""))
# column_def.append(make_column_def_dict("v2AlphInstPitchCur",                                         col_text=""))
# column_def.append(make_column_def_dict("v2AlphSmthIMUCur",                                           col_text=""))
# column_def.append(make_column_def_dict("v3CP3Inst",                                                  col_text=""))
# column_def.append(make_column_def_dict("v3CP3Smth",                                                  col_text=""))
# column_def.append(make_column_def_dict("boomAlphDynaPitCur",                                         col_text=""))
# column_def.append(make_column_def_dict("boomAlphDynaIMUCur",                                         col_text=""))
# column_def.append(make_column_def_dict("boomAlphUpwaPitCur",                                         col_text=""))
# column_def.append(make_column_def_dict("boomAlphUpwaIMUCur",                                         col_text=""))
# column_def.append(make_column_def_dict("vnFltPth",                                                   col_text=""))
# column_def.append(make_column_def_dict("vnIVVI",                                                     col_text=""))
# column_def.append(make_column_def_dict("vnDerAlph",                                                  col_text="Ext IMU AOA Derived"))
# column_def.append(make_column_def_dict("vnRollRateDeg",                                              col_text=""))
# column_def.append(make_column_def_dict("vnRollRateSmthDeg",                                          col_text=""))
# column_def.append(make_column_def_dict("vnPitchRateDeg",                                             col_text=""))
# column_def.append(make_column_def_dict("vnPitchRateSmthDeg",                                         col_text=""))
# column_def.append(make_column_def_dict("vnTHdg",                                                     col_text=""))
# column_def.append(make_column_def_dict("vnG",                                                        col_text=""))
# column_def.append(make_column_def_dict("vnGSmth",                                                    col_text=""))
# column_def.append(make_column_def_dict("vnBankAng",                                                  col_text=""))
# column_def.append(make_column_def_dict("TrnRateDeg",                                                 col_text=""))
# column_def.append(make_column_def_dict("TrnRadFt",                                                   col_text=""))
# column_def.append(make_column_def_dict("efisRollDisag",                                              col_text=""))
# column_def.append(make_column_def_dict("efisPitchDisag",                                             col_text=""))
# column_def.append(make_column_def_dict("efisPaltDisag",                                              col_text=""))
# column_def.append(make_column_def_dict("v2IAS",                                                      col_text=""))
# column_def.append(make_column_def_dict("v2IASVs",                                                    col_text=""))
# column_def.append(make_column_def_dict("StallMarv2IAS",                                              col_text=""))
# column_def.append(make_column_def_dict("v2CAS",                                                      col_text=""))
# column_def.append(make_column_def_dict("v2CASVs",                                                    col_text=""))
# column_def.append(make_column_def_dict("v2StallMarCAS",                                              col_text=""))
# column_def.append(make_column_def_dict("EFISIAS",                                                    col_text=""))
# column_def.append(make_column_def_dict("EFISIASVs",                                                  col_text=""))
# column_def.append(make_column_def_dict("efisStallMarIAS",                                            col_text=""))
# column_def.append(make_column_def_dict("efisCAS",                                                    col_text=""))
# column_def.append(make_column_def_dict("efisCASVs",                                                  col_text=""))
# column_def.append(make_column_def_dict("efisStallMarCAS",                                            col_text=""))
# column_def.append(make_column_def_dict("AlphMar",                                                    col_text=""))
# column_def.append(make_column_def_dict("AbsAlph",                                                    col_text=""))
# column_def.append(make_column_def_dict("AbsAlphMar",                                                 col_text=""))
# column_def.append(make_column_def_dict("efisCASVsG",                                                 col_text=""))
# column_def.append(make_column_def_dict("efisStallMarCASG",                                           col_text=""))

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
        if curr_group_idx == 3:
            break;

    # Do some worksheet formatting

    for worksheet in writer.sheets:
        # format_sheet(writer.sheets[worksheet])
        dm_sheet = writer.sheets[worksheet]

        # Add default top row formats
        col_format = writer.book.add_format()
        col_format.set_bold()
        col_format.set_text_wrap()
        col_format.set_align('top')
        col_format.set_align('center')
        dm_sheet.set_row(0, None, col_format)

        # Format each column
        for col_idx in range(len(column_def)):

            # Add tooltip
#            if column_def[col_idx]["tooltip"] != "":
#                dm_sheet.write_url(0, col_idx+1, "", None, column_def[col_idx]["col_text"], column_def[col_idx]["tooltip"])
 
            # Set column width
            dm_sheet.set_column(col_idx, col_idx, 10)

            # Add column color
            if column_def[col_idx]["col_color"] != "":
                col_format = writer.book.add_format()
                col_format.set_bold()
                col_format.set_text_wrap()
                col_format.set_align('top')
                col_format.set_align('center')
                col_format.set_bg_color(column_def[col_idx]["col_color"])
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
