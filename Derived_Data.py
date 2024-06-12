# -*- coding: utf-8 -*-
"""
Created on Wed Mar 1 2022

@author: Bob Baggerman
"""

import math
import numpy as np
import pandas as pd
import re

import Excel_Columns as ExCol
import Alpha_Beta_Filter as abf

# Precompile the equation strip regular expression
strip_re = re.compile(r'fdf\[\'(.*?)\'\]')

# Strip the data frame variable reference  from an equation string for better display
def eq_strip(equation):
    stripped_eq = strip_re.sub(r'\1', equation)
    return stripped_eq


def add_derived_cols(fdf):

    # Catch harmless warnings so they won't print
    # numpy.seterr(all='warn')

    available_cols = fdf.columns.values.tolist()
    data_sample_period = 1.0 / 50.0 # 50 Hz

    # Smoothed Data
    # -------------
    
    # Pressure smoothing done in real time in the box adds about 0.3 seconds
    # of time delay. This centered window filtering offered filtered values
    # without the time delay. These should be used instead of the logged
    # smoothed values
    
    if ("priPFwd" in available_cols):
        # fdf["priPFwdSmthW"] = fdf["priPFwd"].rolling(25, center=True).mean()
        eq = "fdf['priPFwd'].rolling(25, center=True).mean()"
        ExCol.column_def["priPFwdSmthW"]["equation"] = eq_strip(eq)
        fdf["priPFwdSmthW"] = eval(eq)
        available_cols.append("priPFwdSmthW")

    if ("priP45" in available_cols):
        eq = "fdf['priP45'].rolling(25, center=True).mean()"
        ExCol.column_def["priP45SmthW"]["equation"] = eq_strip(eq)
        fdf["priP45SmthW"] = eval(eq)
        available_cols.append("priP45SmthW")

    if ("secPFwd" in available_cols):
        eq = "fdf['secPFwd'].rolling(25, center=True).mean()"
        ExCol.column_def["secPFwdSmthW"]["equation"] = eq_strip(eq)
        fdf["secPFwdSmthW"] = eval(eq)
        available_cols.append("secPFwdSmthW")

    if ("secP45" in available_cols):
        eq = "fdf['secP45'].rolling(25, center=True).mean()"
        ExCol.column_def["secP45SmthW"]["equation"] = eq_strip(eq)
        fdf["secP45SmthW"] = eval(eq)
        available_cols.append("secP45SmthW")

    if ("priPStatic" in available_cols):
        eq = "fdf['priPStatic'].rolling(50, center=True).mean()"
        ExCol.column_def["priPStaticSmth"]["equation"] = eq_strip(eq)
        fdf["priPStaticSmth"] = eval(eq)
        available_cols.append("priPStaticSmth")

    if ("secPStatic" in available_cols):
        eq = "fdf['secPStatic'].rolling(50, center=True).mean()"
        ExCol.column_def["secPStaticSmth"]["equation"] = eq_strip(eq)
        fdf["secPStaticSmth"] = eval(eq)
        available_cols.append("secPStaticSmth")

    # In several places secondary system pressures are normalized to
    # the static pressure measured by the primary system. Trouble is that
    # these static pressures are quite noisy. Calculate and filter a
    # static pressure correction term for use later.
        
    if ("priPStaticSmth" in available_cols) and ("priPStaticSmth" in available_cols):
        fdf["StaticCorrSmthMB"] = fdf["secPStatic"] - fdf["priPStatic"]
        available_cols.append("StaticCorrSmthMB")
        
    # Area 1:  Time, GPS Gnd Speed, Track and Winds Aloft
    # ---------------------------------------------------
    
    # vnTimeUTC
    # '=vnTimeUTC

    # vnGndSpeed - Ground Speed
    # vnGndTrack - Ground Track
    if ("vnGnssVelNedNorth" in available_cols) and ("vnGnssVelNedEast" in available_cols):
        fdf["vnGndSpeed"] = ((fdf["vnGnssVelNedNorth"] ** 2) + \
                             (fdf["vnGnssVelNedEast"]  ** 2)).apply(math.sqrt) * 1.9438
        fdf["vnGndTrack"] = (np.arctan2(fdf["vnGnssVelNedEast"], fdf["vnGnssVelNedNorth"]) * 180.0 / 3.1416).mod(360)
        available_cols.append("vnGndSpeed")
        available_cols.append("vnGndTrack")

    # vnWindDir

    # vnWindSpd

    # Area 2:  Convert GNSS/INS Data from Metric to English Measurements and G
    # ------------------------------------------------------------------------
    
    # vnVelNedNorthFPS
    # '=vnVelNedNorth*3.2808399
    if ("vnVelNedNorth" in available_cols):
        eq = "fdf['vnVelNedNorth'] * 3.2808399"
        ExCol.column_def["vnVelNedNorthFPS"]["equation"] = eq_strip(eq)
        fdf["vnVelNedNorthFPS"] = eval(eq)
        available_cols.append("vnVelNedNorthFPS")

    # vnVelNedEastFPS
    # '=vnVelNedEast*3.2808399
    if ("vnVelNedEast" in available_cols):
        eq = "fdf['vnVelNedEast'] * 3.2808399"
        ExCol.column_def["vnVelNedEastFPS"]["equation"] = eq_strip(eq)
        fdf["vnVelNedEastFPS"] = eval(eq)
        available_cols.append("vnVelNedEastFPS")

    # vnVelNedDownFPS
    # '=vnVelNedDown*3.2808399
    if ("vnVelNedDown" in available_cols):
        eq = "fdf['vnVelNedDown'] * 3.2808399"
        ExCol.column_def["vnVelNedDownFPS"]["equation"] = eq_strip(eq)
        fdf["vnVelNedDownFPS"] = eval(eq)
        available_cols.append("vnVelNedDownFPS")

    # vnFwdG
    # '=vnAccelFwd/9.80655
    if ("vnAccelFwd" in available_cols):
        eq = "fdf['vnAccelFwd'] / 9.80655"
        ExCol.column_def["vnFwdG"]["equation"] = eq_strip(eq)
        fdf["vnFwdG"] = eval(eq)
        available_cols.append("vnFwdG")

    # vnLatG
    # '=vnAccelLat/9.80655
    if ("vnAccelLat" in available_cols):
        eq = "fdf['vnAccelLat'] / 9.80655"
        ExCol.column_def["vnLatG"]["equation"] = eq_strip(eq)
        fdf["vnLatG"] = eval(eq)
        available_cols.append("vnLatG")

    # vnLinAccFwdG
    # '=vnLinAccFwd/9.80655
    if ("vnLinAccFwd" in available_cols):
        eq = "fdf['vnLinAccFwd'] / 9.80655"
        ExCol.column_def["vnLinAccFwdG"]["equation"] = eq_strip(eq)
        fdf["vnLinAccFwdG"] = eval(eq)
        available_cols.append("vnLinAccFwdG")

    # vnLinAccLatG
    # '=vnLinAccLat/9.80655
    if ("vnLinAccLat" in available_cols):
        eq = "fdf['vnLinAccLat'] / 9.80655"
        ExCol.column_def["vnLinAccLatG"]["equation"] = eq_strip(eq)
        fdf["vnLinAccLatG"] = eval(eq)
        available_cols.append("vnLinAccLatG")

    # vnLinAccVertG
    # '=-vnLinAccVert/9.80655
    if ("vnLinAccVert" in available_cols):
        eq = "-fdf['vnLinAccVert'] / 9.80655"
        ExCol.column_def["vnLinAccVertG"]["equation"] = eq_strip(eq)
        fdf["vnLinAccVertG"] = eval(eq)
        available_cols.append("vnLinAccVertG")

    # Area 3.  Pressures (PSI and mb) and Coefficient of Pressures
    # ------------------------------------------------------------
    
    # Conversion from pressure counts to PSI is all jacked up. From the 4525DODS5AI001DP
    # pressure sensor data sheet it looks like the slope of the transfer function is 6553.0.
    # Note that the count values sent by the box already have the zero bias taken out
    # so that 0 counts is 0 pressure difference.

    # priPFwdSmthPSI
    # OLD '=0.0002*(priPFwdSmthW+8111)-1.25 WRONG!
    # NEW '=priPFwdSmthW/6553.0
    if ("priPFwdSmthW" in available_cols):
        eq = "fdf['priPFwdSmthW'] / 6553.0"
        ExCol.column_def["priPFwdSmthPSI"]["equation"] = eq_strip(eq)
        fdf["priPFwdSmthPSI"] = eval(eq)
        available_cols.append("priPFwdSmthPSI")

    # priP45SmthPSI
    # OLD '=0.0002*(priP45SmthW+8055)-1.25 WRONG!
    # NEW '=priP45SmthW/6553.0
    if ("priP45SmthW" in available_cols):
        eq = "fdf['priP45SmthW'] / 6553.0"
        ExCol.column_def["priP45SmthPSI"]["equation"] = eq_strip(eq)
        fdf["priP45SmthPSI"] = eval(eq)
        available_cols.append("priP45SmthPSI")

    # Looks like Vac made an attempt to reference pressures to the priPStatic, which
    # is not unreasonable. But where he came up with the original math is a mystery
    # to me. I'll attempt to unjack it.

    # secPFwdSmthPSI
    # OLD '=0.0002*(secPFwdSmthW+8192)-1.25+(secPStatic*0.0145038)-(priPStatic*0.0145038)
    # NEW '=(secPFwdSmthW/6553.0)+(secPStatic-priPStatic)*0.0145038
    if ("secPFwdSmthW" in available_cols) and ("StaticCorrSmthMB" in available_cols):
        eq = "fdf['secPFwdSmthW']/6553.0 + fdf['StaticCorrSmthMB']*0.0145038"
        ExCol.column_def["secPFwdSmthPSI"]["equation"] = eq_strip(eq)
        fdf["secPFwdSmthPSI"] = eval(eq)
        available_cols.append("secPFwdSmthPSI")

    # secP45SmthPSI
    # OLD '=0.0002*(secP45SmthW+8192)-1.25+(secPStatic*0.0145038)-(priPStatic*0.0145038)
    # NEW '=(secP45SmthW/6553.0)+(secPStatic-priPStatic)*0.0145038
    if ("secP45SmthW" in available_cols) and ("StaticCorrSmthMB" in available_cols):
        eq = "fdf['secP45SmthW']/6553.0 + fdf['StaticCorrSmthMB']*0.0145038"
        ExCol.column_def["secP45SmthPSI"]["equation"] = eq_strip(eq)
        fdf["secP45SmthPSI"] = eval(eq)
        available_cols.append("secP45SmthPSI")

    # Again, this conversion to millibars is all jacked up. Do a straight 
    # conversion from PSI to millibars.

    # priPFwdSmthMB
    # OLD '=0.0105*(priPFwdSmthW+8111)-86.183 WRONG
    # NEW '=priPFwdSmthPSI * 68.94757
    if ("priPFwdSmthPSI" in available_cols):
        eq = "fdf['priPFwdSmthPSI'] * 68.94757"
        ExCol.column_def["priPFwdSmthMB"]["equation"] = eq_strip(eq)
        fdf["priPFwdSmthMB"] = eval(eq)
        available_cols.append("priPFwdSmthMB")

    # priP45SmthMB
    # OLD '=0.0105*(priP45SmthW+8192)-86.183 WRONG!
    # NEW '=priP45SmthPSI * 68.94757
    if ("priP45SmthPSI" in available_cols):
        eq = "fdf['priP45SmthPSI']  * 68.94757"
        ExCol.column_def["priP45SmthMB"]["equation"] = eq_strip(eq)
        fdf["priP45SmthMB"] = eval(eq)
        available_cols.append("priP45SmthMB")

    # secPFwdSmthMB
    # OLD '=0.0105*(secPFwdSmthW+8192)-86.183+secPStatic-priPStatic
    # NEW '=secPFwdSmthPSI * 68.94757 + secPStatic - priPStatic
    if ("secPFwdSmthPSI" in available_cols) and ("StaticCorrSmthMB" in available_cols):
        eq = "fdf['secPFwdSmthPSI'] * 68.94757 + fdf['StaticCorrSmthMB']"
        ExCol.column_def["secPFwdSmthMB"]["equation"] = eq_strip(eq)
        fdf["secPFwdSmthMB"] = eval(eq)
        available_cols.append("secPFwdSmthMB")

    # secP45SmthMB
    # OLD '=0.0105*(secP45SmthW+8192)-86.183+secPStatic-priPStatic
    # NEW '=secP45SmthPSI * 68.94757 + secPStatic - priPStatic
    if ("secP45SmthPSI" in available_cols) and ("StaticCorrSmthMB" in available_cols):
        eq = "fdf['secP45SmthPSI'] * 68.94757 + fdf['StaticCorrSmthMB']"
        ExCol.column_def["secP45SmthMB"]["equation"] = eq_strip(eq)
        fdf["secP45SmthMB"] = eval(eq)
        available_cols.append("secP45SmthMB")

    # priCP3Inst - V2 CP3 Inst (priP45/priPFwd)
    # =E2/C2
    if ("priPFwd" in available_cols) and ("priP45" in available_cols):
        eq = "fdf['priP45'] / fdf['priPFwd']"
        ExCol.column_def["priCP3Inst"]["equation"] = eq_strip(eq)
        fdf["priCP3Inst"] = eval(eq)
        available_cols.append("priCP3Inst")

    # priCP3Smth - V2 CP3 Smooth (priP45/priPFwd)
    # =F2/D2
    if ("priPFwdSmthW" in available_cols) and ("priP45SmthW" in available_cols):
        eq = "fdf['priP45SmthW'] / fdf['priPFwdSmthW']"
        ExCol.column_def["priCP3Smth"]["equation"] = eq_strip(eq)
        fdf["priCP3Smth"] = eval(eq)
        available_cols.append("priCP3Smth")
    
    # secCP3Inst - V3 CP3 Instantaneous
    # =(Q2+8192)/(S2+8192)
    if ("secPFwd" in available_cols) and ("secP45" in available_cols):
        eq = "(fdf['secPFwd']+8192) / (fdf['secP45']+8192)"
        ExCol.column_def["secCP3Inst"]["equation"] = eq_strip(eq)
        fdf["secCP3Inst"] = eval(eq)
        available_cols.append("secCP3Inst")

    # secCP3Smth - V3 CP3 Smoothed
    # =(R2+8192)/(T2+8192)
    if ("secPFwdSmthW" in available_cols) and ("secP45SmthW" in available_cols):
        eq = "(fdf['secPFwdSmthW']+8192) / (fdf['secP45SmthW']+8192)"
        ExCol.column_def["secCP3Smth"]["equation"] = eq_strip(eq)
        fdf["secCP3Smth"] = eval(eq)
        available_cols.append("secCP3Smth")

    # Note, arguments for np.arctan2(y,x) are opposite of Excel =atan2(x,y)

    # priCP4Inst
    # '=ATAN2(priPFwd,priP45)
    if ("priPFwd" in available_cols) and ("priP45" in available_cols):
        eq = "np.arctan2(fdf['priP45'], fdf['priPFwd'])"
        ExCol.column_def["priCP4Inst"]["equation"] = eq_strip(eq)
        fdf["priCP4Inst"] = eval(eq)
        available_cols.append("priCP4Inst")

    # priCP4Smth
    # '=ATAN2(priPFwdSmthW,priP45SmthW)
    if ("priPFwdSmthW" in available_cols) and ("priP45SmthW" in available_cols):
        eq = "np.arctan2(fdf['priP45SmthW'], fdf['priPFwdSmthW'])"
        ExCol.column_def["priCP4Smth"]["equation"] = eq_strip(eq)
        fdf["priCP4Smth"] = eval(eq)
        available_cols.append("priCP4Smth")

    # secCP4Inst
    # '=ATAN2(secPFwd,secP45)
    if ("secPFwd" in available_cols) and ("secP45" in available_cols):
        eq = "np.arctan2(fdf['secP45'], fdf['secPFwd'])"
        ExCol.column_def["secCP4Inst"]["equation"] = eq_strip(eq)
        fdf["secCP4Inst"] = eval(eq)
        available_cols.append("secCP4Inst")

    # secCP4Smth
    # '=ATAN2(secPFwdSmthW,secP45SmthW)
    if ("secPFwdSmthW" in available_cols) and ("secP45SmthW" in available_cols):
        eq = "np.arctan2(fdf['secP45SmthW'], fdf['secPFwdSmthW'])"
        ExCol.column_def["secCP4Smth"]["equation"] = eq_strip(eq)
        fdf["secCP4Smth"] = eval(eq)
        available_cols.append("secCP4Smth")

    # priFwd-45/q
    # '=(priPFwdSmthPSI-priP45SmthPSI)/priPFwdSmthPSI
    if ("priPFwdSmthPSI" in available_cols) and ("priP45SmthPSI" in available_cols):
        eq = "(fdf['priPFwdSmthPSI']-fdf['priP45SmthPSI'])/fdf['priPFwdSmthPSI']"
        ExCol.column_def["priFwd-45/q"]["equation"] = eq_strip(eq)
        fdf["priFwd-45/q"] = eval(eq)
        available_cols.append("priFwd-45/q")

    # secFwd-45/q
    # '=(secPFwdSmthPSI-secP45SmthPSI)/secPFwdSmthPSI
    if ("secPFwdSmthPSI" in available_cols) and ("secP45SmthPSI" in available_cols):
        eq = "(fdf['secPFwdSmthPSI']-fdf['secP45SmthPSI'])/fdf['secPFwdSmthPSI']"
        ExCol.column_def["secFwd-45/q"]["equation"] = eq_strip(eq)
        fdf["secFwd-45/q"] = eval(eq)
        available_cols.append("secFwd-45/q")

    # Area 4.  Atmospherics
    # ---------------------
    
    # OATF
    # '=(priOAT*(9/5))+32
    if "priOAT" in available_cols:
        eq = "(fdf['priOAT'] * 9.0/5.0) + 32.0"
        ExCol.column_def["OATF"]["equation"] = eq_strip(eq)
        fdf["OATF"] = eval(eq)
        available_cols.append("OATF")

    # StdTempF
    # '=59-(priAltitude/1000*3.566)
    if "priAltitude" in available_cols:
        eq = "59 - (fdf['priAltitude']/1000*3.566)"
        ExCol.column_def["StdTempF"]["equation"] = eq_strip(eq)
        fdf["StdTempF"] = eval(eq)
        available_cols.append("StdTempF")

    # StdTempDeltaF
    # '=OATF-StdTempF
    if ("OATF" in available_cols) and ("StdTempF" in available_cols):
        eq = "fdf['OATF'] - fdf['StdTempF']"
        ExCol.column_def["StdTempDeltaF"]["equation"] = eq_strip(eq)
        fdf["StdTempDeltaF"] = eval(eq)
        available_cols.append("StdTempDeltaF")

    # StdTempC (OK)
    # '=15-(priAltitude/1000*1.9812)
    if "priAltitude" in available_cols:
        eq = "15 - (fdf['priAltitude']/1000*1.9812)"
        ExCol.column_def["StdTempC"]["equation"] = eq_strip(eq)
        fdf["StdTempC"] = eval(eq)
        available_cols.append("StdTempC")

    # StdTempDeltaC (OK)
    # '=priOAT-StdTempC
    if ("priOAT" in available_cols) and ("StdTempC" in available_cols):
        eq = "fdf['priOAT'] - fdf['StdTempC']"
        ExCol.column_def["StdTempDeltaC"]["equation"] = eq_strip(eq)
        fdf["StdTempDeltaC"] = eval(eq)
        available_cols.append("StdTempDeltaC")

    # StdTempK (OK)
    # '=288.15-(priAltitude/1000*1.9812)
    if "priAltitude" in available_cols:
        eq = "288.15 - (fdf['priAltitude']/1000*1.9812)"
        ExCol.column_def["StdTempK"]["equation"] = eq_strip(eq)
        fdf["StdTempK"] = eval(eq)
        available_cols.append("StdTempK")

    # Pressure Ratio (OK)
    # =(1-priAltitude/145442)^5.25586
    if "priAltitude" in available_cols:
        eq = "(1 - (fdf['priAltitude'] / 145442)) ** 5.25586"
        ExCol.column_def["PresRatio"]["equation"] = eq_strip(eq)
        fdf["PresRatio"] = eval(eq)
        available_cols.append("PresRatio")

    # DenRatio (OK, values checked)
    # OLD '=((PresRatio*2116.2)/(1718*(460+OATF))/(0.0023769))
    # https://eaglepubs.erau.edu/introductiontoaerospaceflightvehicles/chapter/international-standard-atmosphere-isa/
    # NEW =PresRatio * 518.67 / (OATF+459.7)
    if ("PresRatio" in available_cols) and ("OATF" in available_cols):
        eq = "fdf['PresRatio'] * 518.67 / (460+fdf['OATF'])"
        ExCol.column_def["DenRatio"]["equation"] = eq_strip(eq)
        fdf["DenRatio"] = eval(eq)
        available_cols.append("DenRatio")
        
    # DenAlt (OK, values checked)
    # '=priAltitude+120*(StdTempDeltaC)
    if ("priAltitude" in available_cols) and ("StdTempDeltaC" in available_cols):
        eq = "fdf['priAltitude'] + 118.8 * fdf['StdTempDeltaC']"
        ExCol.column_def["DenAlt"]["equation"] = eq_strip(eq)
        fdf["DenAlt"] = eval(eq)
        available_cols.append("DenAlt")

    # Area 5.  Air Data Boom Uncorrected Angles, Pressures and Airspeeds
    # ------------------------------------------------------------------
    
    # boomStatic
    # '=(0.00012207*(boomStaticRaw-1638))*1000
    if "boomStaticRaw" in available_cols:
        eq = "(0.00012207*(fdf['boomStaticRaw']-1638))*1000"
        ExCol.column_def["boomStatic"]["equation"] = eq_strip(eq)
        fdf["boomStatic"] = eval(eq)
        available_cols.append("boomStatic")

    # boomDynamic
    # '=0.01525902*(boomDynamicRaw-1638)-100
    if "boomDynamicRaw" in available_cols:
        eq = "0.01525902*(fdf['boomDynamicRaw']-1638)-100"
        ExCol.column_def["boomDynamic"]["equation"] = eq_strip(eq)
        fdf["boomDynamic"] = eval(eq)
        available_cols.append("boomDynamic")

    # boomAlpha - Boom alpha in degrees
    if ("boomAlphaRaw" in available_cols):
        # =0.00000000000070918*V5^4-0.000000011698*V5^3+0.000070109*V5^2-0.21624*V5+310.21
        eq = "0.000000011698      * np.power(fdf['boomAlphaRaw'], 3) + " \
             "0.000070109         * np.power(fdf['boomAlphaRaw'], 2) - " \
             "0.21624             *          fdf['boomAlphaRaw']     + " \
             "310.21"
        ExCol.column_def["boomAlpha"]["equation"] = eq_strip(eq)
        fdf["boomAlpha"] = eval(eq)
        # fdf["boomAlpha"] = 0.00000000000070918 * np.power(fdf["boomAlphaRaw"], 4) - \
        #                    0.000000011698      * np.power(fdf["boomAlphaRaw"], 3) + \
        #                    0.000070109         * np.power(fdf["boomAlphaRaw"], 2) - \
        #                    0.21624             *          fdf["boomAlphaRaw"]     + \
        #                    310.21
        available_cols.append("boomAlpha")

    # boomBeta
    # '=0.00000000000020096*boomBetaRaw^4-0.0000000037124*boomBetaRaw^3+0.000025497*boomBetaRaw^2-0.037141*boomBetaRaw-72.506

    # boomIASCalc
    # '=SQRT(2*boomDynamic*100/1.225)*1.94384

    # boomTAS1
    # '=boomBeta * SQRT(1 / DenRatio)

    # boomTAS2
    # '=boomBeta * SQRT((1.225 / ((boomStatic * 100) / (287.05 * (priOAT + 273.15)))))

    # boomPAlt
    # '= (1-(boomStatic/1013.25)^0.190284)*145366.45


    # Area 6.  Primary System Airspeeds
    # ---------------------------------
    
    # priIAS
    # '=priIAS

    # priIASSmth
    # '=abf(priIAS)

    # priIASSmthRate

    # priCAS
    # '=0.9935*priIAS+0.7972

    # priCASSmth
    # '=abf(priCAS)
    
    # priCASSmthRate

    # priTAS
    # '=priTAS

    # priTASSmth
    # '=abf(priTAS)

    # priTASSmthRate

    # TASMS - TAS M/S 
    if ("priTAS" in available_cols):
        # =I2*(1+(H2/1000*0.017))*0.5144
        fdf["priTASMS"] = fdf["priTAS"] * 0.5144 
        available_cols.append("priTASMS")

    # TASFPS - TAS FPS 
    if ("priTAS" in available_cols):
        # =DO2*2.28084
        fdf["priTASFPS"] = fdf["priTAS"] * 1.68781
        available_cols.append("TASFPS")

    # Area 7.  Secondary System Airspeeds
    # -----------------------------------
    
    # secIASCalc
    # '=SQRT(2*((secPFwdSmthMB+secPStatic)-priPStatic)*100/1.225)*1.94384

    # secIASSmth
    # '='abf(secIASCalc)

    # SecIASSmthRate
    # secCAS
    # secCASSmth
    # secCASSmthRate

    # Area 8.  Attitude, Performance and G
    # ------------------------------------
    
    # 
    # vnPitch
    # '=vnPitch

    # vnPitchRateDeg - VN Pitch Rate (deg/sec) 
    if ("vnAngularRatePitch" in available_cols):
        # =AC2*57.2958
        fdf["vnPitchRateDeg"] = fdf["vnAngularRatePitch"] * 57.2958
        available_cols.append("vnPitchRateDeg")

    # vnPitchRateSmthDeg - VN Pitch Rate Smoothed (deg/sec) 
    if ("vnPitchRateDeg" in available_cols):
        # DI4=0.1*DI3+0.9*DJ3
        start_val = 0
        abfilter = abf.AlphaBetaFilter(data_sample_period, 0.1, 1, start_val)
        fdf["vnPitchRateSmthDeg"] = fdf["vnPitchRateDeg"].apply(abfilter.update)
        available_cols.append("vnPitchRateSmthDeg")

    # vnRoll
    # '=vnRoll

    # vnRollRateDeg - VN Roll Rate (deg/sec) 
    if ("vnAngularRateRoll" in available_cols):
        # =AB2*57.2958
        fdf["vnRollRateDeg"] = fdf["vnAngularRateRoll"] * 57.2958
        available_cols.append("vnRollRateDeg")

    # vnRollRateSmthDeg - VN Roll Rate Smoothed (deg/sec) 
    if ("vnRollRateDeg" in available_cols):
        # DG4=0.1*DG3+0.9*DH3
        start_val = 0
        abfilter = abf.AlphaBetaFilter(data_sample_period, 0.1, 1, start_val)
        fdf["vnRollRateSmthDeg"] = fdf["vnRollRateDeg"].apply(abfilter.update)
        available_cols.append("vnRollRateSmthDeg")

    # boomBeta
    # '=boomBeta

    # boomBetaRateDeg
    # '=vnAngularRateYaw

    # boomBetaRateSmthDeg
    # abf(boomBetaRateDeg)

    # vnFltPth - VN Flight Path Angle (deg) 
    if ("vnVelNedDown" in available_cols) and ("priTASMS" in available_cols):
        # =ASIN(-AG2/DO2)*180/PI()
        # Ignore harmless warnings so they won't print
        np.seterr(all='ignore')
        fdf["vnFltPth"] =  np.arcsin(-fdf["vnVelNedDown"]/fdf["priTASMS"]) * 180 / 3.1416
        np.seterr(all='print')
        available_cols.append("vnFltPth")

    # vnFltPthCor
    # '=ASIN(-vnVelNedDown/priTASMS)*180/PI()-(X6/9.80955)

    # vnTHdg - VN True Heading (deg) 
    if ("vnYaw" in available_cols):
        # =IF(AK2>0,AK2,IF(AK2<0,360-ABS(AK2)))
        fdf.loc[fdf["vnYaw"] >= 0, "vnTHdg"] = fdf["vnYaw"]
        fdf.loc[fdf["vnYaw"] <  0, "vnTHdg"] = 360 - fdf["vnYaw"].abs()
        available_cols.append("vnTHdg")

    # vnIVVI - VN IVVI (FPM) 
    if ("vnVelNedDown" in available_cols):
        # =-(AG2/0.00508)
        fdf["vnIVVI"] = -fdf["vnVelNedDown"] / 0.00508
        available_cols.append("vnIVVI")

    # vnTrnRateDeg
    # '=ABS(vnAngularRateYaw*57.2958)

    # vnTrnRateDegSmth
    # abf(vnTrnRateDegSmth)

    # vnTrnRadFt
    # '=(priTAS^2/(11.26*TAN(ABS(vnRoll)*0.017453)))

    # priGSmth
    # abf(priVerticalG)

    # secGSmth
    # abf(secVerticalG)

    # vnG - VN G 
    # vnGSmth - VN G Smoothed 
    if "vnAccelVert" in available_cols:
        # =-(AJ2/9.80655)
        fdf["vnG"] = -fdf["vnAccelVert"] / 9.80655
        available_cols.append("vnG")

        # Init the alpha-beta filters
        # DL4=0.1*DL3+0.9*DM3
        start_val = fdf["vnG"][1:50].agg('mean')
        abfilter = abf.AlphaBetaFilter(data_sample_period, 0.1, 1, start_val)
        fdf["vnGSmth"] = fdf["vnG"].apply(abfilter.update)
        available_cols.append("vnGSmth")


    # Area 9.  Angle of Attack
    # ------------------------
    
    # vnDerAlph - VN Derived Alpha (deg) 
    # vnDrAlphSmth
    # abf(vnDerAlph)
    if ("vnPitch" in available_cols) and ("vnFltPth" in available_cols):
        # =AL2-DQ2
        fdf["vnDerAlph"] = fdf["vnPitch"] - fdf["vnFltPth"]
        available_cols.append("vnDerAlph")

    # vnDrAlphRate
    # vnDrAlphRateSmth

    # boomAlphaCor
    # boomAlphCorSmth
    # '=IF(priFlapsPos=0,0.7917*boomAlpha-1.2758,IF(priFlapsPos=20,0.7979*boomAlpha-1.6647,IF(priFlapsPos=40,0.7863*boomAlpha-1.7172)))-(0.1264*(-vnAccelVert/9.80655-1))+(3.08*(vnAngularRatePitch*57.2958)/(priTAS*1.68781)+(10.19*(vnAngularRateRoll*57.2958)/(priTAS*1.68781)))
    # abf(boomAlphaCor)


    # boomAlphaRate
    # boomAlphaRateSmth

    # CockpitAngleofAttack
    # CockpitAngleofAttackSmth
    # =priAngleofAttack
    # abf(CockpitAngleofAttack)

    # CockpitAngleofAttackRate
    # CockpitAngleofAttackRateSmth

    # priAlpha
    # priAlphaSmth
    # '=IF(priFlapsPos=0,6.5805*priCP3Smth^2+22.763*priCP3Smth+4.3907,IF(priFlapsPos=20,-4.0083*priCP3Smth^2+29.537*priCP3Smth+2.6034,IF(priFlapsPos=40,-5.6802*priCP3Smth^2+31.567*priCP3Smth+1.0169)))
    # abf(priAlpha)

    # priAlphaRate
    # priAlphaRateSmth

    # secAlphaCP3
    # secAlphaCP3Smth

    # secAlphaCP3Rate
    # secAlphaCP3RateSmth

    # secAlphaCP4
    # secAlphaCP4Smth

    # secAlphaCP4Rate
    # secAlphaCP4RateSmth

    # priAbsAlph
    # priAbsAlphaSmth
    # '=IF(priFlapsPos=0,10.58*priCP3Smth^2+25.139*priCP3Smth+6.1489,IF(priFlapsPos=20,25.039*priCP3Smth+5.7465,IF(priFlapsPos=40,8.5839*priCP3Smth^2+21.974*priCP3Smth+5.8102)))
    # abf(priAbsAlph)

    # Area 10.  Sideslip
    # ------------------
    
    # boomBeta
    # '=boomBeta

    # boomBetaCor
    # boomBetaCorSmth

    # boomBetaRate
    # boomBetaRateSmth

    # Area 11.  AOA Accuracy
    # ----------------------
    
    # boomvsCockpit
    # '=ABS(boomAlphCorSmth-CockpitAngleofAttackSmth)

    # vnvsCockpit
    # '=ABS(vnDrAlphSmth-CockpitAngleofAttackSmth)

    # boomvspri
    # '=ABS(boomAlphCorSmth-priAlphaSmth)

    # vnvspri
    # '=ABS(vnDrAlphSmth-priAlphaSmth)

    # boomvssecCP3
    # '=ABS(boomAlphCorSmth-secAlphaCP3Smth)

    # vnvssecCP3
    # '=ABS(vnDrAlphSmth-secAlphaCP3Smth)

    # boomvssecCP4
    # '=ABS(boomAlphCorSmth-secAlphaCP4Smth)

    # vnvssecCP4
    # '=ABS(vnDrAlphSmth-secAlphaCP4Smth)


    # Area 12. Disagreements
    # ----------------------
    
    # priDisagvnRoll
    # '=ABS(priRoll-vnRoll)

    # priDisagvnPitch
    # '=ABS(priPitch-vnPitch)

    # priDisagefisPAlt
    # '=ABS(priAltitude-efisPAlt)

    # priDisagefisKIAS
    # '=ABS(priIAS-efisIAS)

    # priDisagboomPAlt
    # '=ABS(boomPAlt-priAltitude)

    # priDisagboomKIAS
    # '=ABS(priIAS-boomBeta)

    # priDisagboomTAS
    # '=ABS(priTAS-boomTAS1)


    # Area 13.  Aerodynamic Margin
    # ----------------------------
    
    # priKIASStall
    # '=IF(priFlapsPos=0,46.47*SQRT(ABS(vnGSmth)),IF(priFlapsPos=20,44.92*SQRT(ABS(vnGSmth)),IF(priFlapsPos=40,42.88*SQRT(ABS(vnGSmth)))))

    # priKIASStallMar
    # =priIAS-priKIASStall

    # priAOAStallMarSmth
    # '=IF(priFlapsPos=0,18.72-priAlphaSmth,IF(priFlapsPos=20,18.18-priAlphaSmth,IF(priFlapsPos=40,17.86-priAlphaSmth)))

    # CockpitAOASmthMar
    # '=IF(priFlapsPos=0,20.09-CockpitAngleofAttackSmth,IF(priFlapsPos=20,20.04-CockpitAngleofAttackSmth,IF(priFlapsPos=40,20.1-CockpitAngleofAttackSmth)))

    # priAbsAlphaSmthMar
    # '=IF(priFlapsPos=0,22.96-priAbsAlphaSmth,IF(priFlapsPos=20,20.06-priAbsAlphaSmth,IF(priFlapsPos=40,22.02-priAbsAlphaSmth)))

    # secKIASStall

    # secKIASStallMar

    # secAOAMarSmth


    # Extras
    # ------
    #     
    # TAS - TAS Knots
    # if (("priIAS" in available_cols) and ("priPAlt" in available_cols)) and not ("priTAS" in available_cols):
    #     # =I2*(1+(H2/1000*0.017))
    #     fdf["priTAS"] = fdf["priIAS"] * (1 + (fdf["priPAlt"] / 1000 * 0.017)) # MAKE SURE THIS IS RIGHT ()
    #     available_cols.append("priTAS")

    # boomBetaDer - Boom beta in degrees
    # if ("BoomBetaDer" in available_cols) and ("priP45" in available_cols):
        # # BLANK
        # fdf["BoomBetaDer"] = 1
        # available_cols.append("BoomBetaDer")


    # v2AlphPitchCur - V2 Derived Alpha Pitch Curves [Same as Column J] (deg) 
    if ("flapsPos" in available_cols) and ("v2CP3Smth" in available_cols):
        # =IF(K2=0, 22.556*CQ2+4.1106,IF(K2=20,23.318*CQ2+2.5496,IF(K2=40,24.959*CQ2+0.7909)))
        fdf.loc[fdf["flapsPos"] ==  0, "v2AlphPitchCur"] = 22.556 * fdf["v2CP3Smth"] + 4.1106    # 22.556*CQ2+4.1106
        fdf.loc[fdf["flapsPos"] == 20, "v2AlphPitchCur"] = 23.318 * fdf["v2CP3Smth"] + 2.5496    # 23.318*CQ2+2.5496
        fdf.loc[fdf["flapsPos"] == 40, "v2AlphPitchCur"] = 24.959 * fdf["v2CP3Smth"] + 0.7909    # 24.959*CQ2+0.7909
        available_cols.append("v2AlphPitchCur")

    # v2AlphDyna - V2 Dynamic Alpha (deg) Accurate Flaps 0 Only 
    if ("v2CP3Smth" in available_cols):
        # =10.11*CQ2^2+23.893*CQ2+4.742
        fdf["v2AlphDyna"] = (10.11 * fdf["v2CP3Smth"] * fdf["v2CP3Smth"]) + (23.893 * fdf["v2CP3Smth"]) + 4.742  
        available_cols.append("v2AlphDyna")

    # v2AlphInstPitchCur - V2 Instant Alpha Pitch Curve (deg) 
    if ("flapsPos" in available_cols) and ("v2CP3Inst" in available_cols):
        # =IF(K2=0, 22.556*CP2+4.1106,  IF(K2=20,23.318*CP2+2.5496,  IF(K2=40,24.959*CP2+0.7909)))
        fdf.loc[fdf["flapsPos"] ==  0, "v2AlphInstPitchCur"] = 22.556 * fdf["v2CP3Inst"] + 4.1106    # 22.556*CP2+4.1106
        fdf.loc[fdf["flapsPos"] == 20, "v2AlphInstPitchCur"] = 23.318 * fdf["v2CP3Inst"] + 2.5496    # 23.318*CP2+2.5496
        fdf.loc[fdf["flapsPos"] == 40, "v2AlphInstPitchCur"] = 24.959 * fdf["v2CP3Inst"] + 0.7909    # 24.959*CP2+0.7909
        available_cols.append("v2AlphInstPitchCur")

    # v2AlphSmthIMUCur - V2 Smooth Alpha IMU Curve (deg) 
    if ("flapsPos" in available_cols) and ("v2CP3Inst" in available_cols):
        # =IF(K2=0, 23.672*CQ2+4.1089,IF(K2=20,23.348*CQ2+2.3504,IF(K2=40,25.18*CQ2+0.9235)))
        fdf.loc[fdf["flapsPos"] ==  0, "v2AlphSmthIMUCur"] = 23.672 * fdf["v2CP3Inst"] + 4.1089    # 23.672*CQ2+4.1089
        fdf.loc[fdf["flapsPos"] == 20, "v2AlphSmthIMUCur"] = 23.348 * fdf["v2CP3Inst"] + 2.3504    # 23.348*CQ2+2.3504
        fdf.loc[fdf["flapsPos"] == 40, "v2AlphSmthIMUCur"] = 25.180 * fdf["v2CP3Inst"] + 0.9235    # 25.18*CQ2+0.9235
        available_cols.append("v2AlphSmthIMUCur")

    # v3DerAlphSmthPitCur - V2 Derived Alpha Pitch Curves [Smoothed CP3] (deg). 
    # if "" in available_cols:
        # # BLANK
        # fdf["v3DerAlphSmthPitCur"] = 1
        # available_cols.append("v3DerAlphSmthPitCur")

    # v3DynaAlph - V3 Dynamic Alpha (deg) Accurate Flaps 0 Only 
    # if "" in available_cols:
        # # BLANK
        # fdf["v3DynaAlph"] = 1
        # available_cols.append("v3DynaAlph")

    # v3InstAlphPitCur - V2 Instant Alpha Pitch Curve (deg) 
    # if "" in available_cols:
        # # BLANK
        # fdf["v3InstAlphPitCur"] = 1
        # available_cols.append("v3InstAlphPitCur")

    # v3SmthAlphIMUCur - V2 Smooth Alpha IMU Curve (deg) 
    # if "" in available_cols:
        # # BLANK
        # fdf["v3SmthAlphIMUCur"] = 1
        # available_cols.append("v3SmthAlphIMUCur")

    # boomAlphDynaPitCur - Boom Alpha Dynamic Corrected (Pitch Derived Curves) (deg) 
    # NOTE: COULD USE boomAlphUpwaPitCur TO CALC
    if ("flapsPos" in available_cols) and ("vnAccelVert" in available_cols) and ("vnAngularRatePitch" in available_cols) and ("IAS" in available_cols) and ("Palt" in available_cols) and ("boomAlphaDer" in available_cols):
        # =IF(K2=0, 0.7751*X2-1.6016,IF(K2=20,0.7838*X2-1.83,IF(K2=40,0.8023*X2-2.3141)))-(0.1264*(-AJ2/9.80655-1))+(3.08*(AC2*57.2958)/(I2*(1+H2/1000*0.017))*1.68718)
        offset = (0.1264*(-fdf["vnAccelVert"]/9.80655-1))+(3.08*(fdf["vnAngularRatePitch"]*57.2958)/(fdf["IAS"]*(1+fdf["Palt"]/1000*0.017))*1.68718)
        fdf.loc[fdf["flapsPos"] ==  0, "boomAlphDynaPitCur"] = 0.7751 * fdf["boomAlphaDer"] - 1.6016 - offset
        fdf.loc[fdf["flapsPos"] == 20, "boomAlphDynaPitCur"] = 0.7838 * fdf["boomAlphaDer"] - 1.8300 - offset
        fdf.loc[fdf["flapsPos"] == 40, "boomAlphDynaPitCur"] = 0.8023 * fdf["boomAlphaDer"] - 2.3141 - offset
        available_cols.append("boomAlphDynaPitCur")

    # boomAlphDynaIMUCur - Boom Alpha Dynamic Corrected (IMU Derived Curves) (deg) 
    # NOTE: COULD USE boomAlphUpwaIMUCur TO CALC
    if ("flapsPos" in available_cols) and ("vnAccelVert" in available_cols) and ("vnAngularRatePitch" in available_cols) and ("IAS" in available_cols) and ("Palt" in available_cols) and ("boomAlphaDer" in available_cols):
        # =IF(K2=0, 0.8139*X2-1.8903,IF(K2=20,0.8188*X2-2.2276,IF(K2=40,0.8085*X2-2.1983)))-(0.1264*(-AJ2/9.80655-1))+(3.08*(AC2*57.2958)/(I2*(1+H2/1000*0.017))*1.68718)
        offset = (0.1264*(-fdf["vnAccelVert"]/9.80655-1))+(3.08*(fdf["vnAngularRatePitch"]*57.2958)/(fdf["IAS"]*(1+fdf["Palt"]/1000*0.017))*1.68718)
        fdf.loc[fdf["flapsPos"] ==  0, "boomAlphDynaIMUCur"] = 0.8139 * fdf["boomAlphaDer"] - 1.8903 - offset
        fdf.loc[fdf["flapsPos"] == 20, "boomAlphDynaIMUCur"] = 0.8188 * fdf["boomAlphaDer"] - 2.2276 - offset
        fdf.loc[fdf["flapsPos"] == 40, "boomAlphDynaIMUCur"] = 0.8085 * fdf["boomAlphaDer"] - 2.1983 - offset
        available_cols.append("boomAlphDynaIMUCur")

    # boomAlphUpwaPitCur - Boom Alpha Upwash Corrected Only (Pitch Dervied Curves) (deg) 
    if ("flapsPos" in available_cols) and ("boomAlphaDer" in available_cols):
        # =IF(K2=0, 0.7751*X2-1.6016,IF(K2=20,0.7838*X2-1.83,IF(K2=40,0.8023*X2-2.3141)))
        fdf.loc[fdf["flapsPos"] ==  0, "boomAlphUpwaPitCur"] = 0.7751 * fdf["boomAlphaDer"] - 1.6016
        fdf.loc[fdf["flapsPos"] == 20, "boomAlphUpwaPitCur"] = 0.7838 * fdf["boomAlphaDer"] - 1.8300
        fdf.loc[fdf["flapsPos"] == 40, "boomAlphUpwaPitCur"] = 0.8023 * fdf["boomAlphaDer"] - 2.3141
        available_cols.append("boomAlphUpwaPitCur")

    # boomAlphUpwaIMUCur - Boom Alpha Upwash Corrected Only (IMU Derived Curves) (deg) 
    if ("flapsPos" in available_cols) and ("boomAlphaDer" in available_cols):
        # =IF(K2=0, 0.8139*X2-1.8903,IF(K2=20,0.8188*X2-2.2276,IF(K2=40,0.8085*X2-2.1983)))
        fdf.loc[fdf["flapsPos"] ==  0, "boomAlphUpwaIMUCur"] = 0.8139 * fdf["boomAlphaDer"] - 1.8903
        fdf.loc[fdf["flapsPos"] == 20, "boomAlphUpwaIMUCur"] = 0.8188 * fdf["boomAlphaDer"] - 2.2276
        fdf.loc[fdf["flapsPos"] == 40, "boomAlphUpwaIMUCur"] = 0.8085 * fdf["boomAlphaDer"] - 2.1983
        available_cols.append("boomAlphUpwaIMUCur")

    # vnBankAng - Bank Angle (deg) 
    if ("vnRoll" in available_cols):
        # =ABS(AM2)
        fdf["vnBankAng"] = fdf["vnRoll"].abs()
        available_cols.append("vnBankAng")

    # TrnRateDeg - Turn Rate (deg/sec) 
    if ("vnAngularRateYaw" in available_cols):
        # =ABS(AD2*57.2958)
        fdf["TrnRateDeg"] = fdf["vnAngularRateYaw"].abs() * 57.2958
        available_cols.append("TrnRateDeg")

    # TrnRadFt - Turn Radius (feet) 
    if ("TAS" in available_cols) and ("vnBankAng" in available_cols):
        # =IF(DS2>20,(DN2^2/(11.26*TAN(DS2*0.017453))))
        fdf.loc[fdf["vnBankAng"] >  20, "TrnRadFt"] = (fdf["TAS"] ** 2) / (11.26 * np.tan(fdf["vnBankAng"] * 0.017453))
      # fdf.loc[fdf["vnBankAng"] <= 20, "TrnRadFt"] = NaN
        fdf["TrnRadFt"] = 1
        available_cols.append("TrnRadFt")

    # efisRollDisag - EFIS Roll Disag 
    if ("vnRoll" in available_cols) and ("efisRoll" in available_cols):
        # =AM2-CB2
        fdf["efisRollDisag"] = fdf["vnRoll"] - fdf["efisRoll"]
        available_cols.append("efisRollDisag")

    # efisPitchDisag - EFIS Pitch Disag 
    if ("vnPitch" in available_cols) and ("efisPitch" in available_cols):
        # =AL2-CA2
        fdf["efisPitchDisag"] = fdf["vnPitch"] - fdf["efisPitch"]
        available_cols.append("efisPitchDisag")

    # efisPaltDisag - EFIS Palt Disag 
    if ("efisPalt" in available_cols) and ("Palt" in available_cols):
        # =CF2-H2
        fdf["efisPaltDisag"] = fdf["efisPalt"] - fdf["Palt"]
        available_cols.append("efisPaltDisag")

    # v2IAS - V2 KIAS 
    if ("IAS" in available_cols):
        # =1.0238*I2-4.2467
        fdf["v2IAS"] = 1.0238 * fdf["IAS"] - 4.2467
        available_cols.append("v2IAS")

    # v2IASVs - V2 Vs KIAS 
    if ("flapsPos" in available_cols) and ("vnGSmth" in available_cols):
        # =IF(K2=0,44.2*SQRT(ABS(DM2)),IF(K2=20,41.95*SQRT(ABS(DM2)),IF(K2=40,40.07*SQRT(ABS(DM2)))))
        fdf.loc[fdf["flapsPos"] ==  0, "v2IASVs"] = 44.20 * np.sqrt(fdf["vnGSmth"].abs())
        fdf.loc[fdf["flapsPos"] == 20, "v2IASVs"] = 41.95 * np.sqrt(fdf["vnGSmth"].abs())
        fdf.loc[fdf["flapsPos"] == 40, "v2IASVs"] = 40.07 * np.sqrt(fdf["vnGSmth"].abs())
        available_cols.append("v2IASVs")

    # StallMarv2IAS - Stall Margin V2 KIAS 
    if ("v2IAS" in available_cols) and ("v2IASVs" in available_cols):
        # =DY2-DZ2
        fdf["StallMarv2IAS"] = fdf["v2IAS"]-fdf["v2IASVs"]
        available_cols.append("StallMarv2IAS")

    # v2CAS - V2 KCAS (COPY OF IAS)
    if ("IAS" in available_cols):
        # =I2
        fdf["v2CAS"] = fdf["IAS"]
        available_cols.append("v2CAS")

    # v2CASVs - V2 Vs KCAS 
    if ("flapsPos" in available_cols) and ("vnGSmth" in available_cols):
        # =IF(K2=0,47.32*SQRT(ABS(DM2)),IF(K2=20,45.12*SQRT(ABS(DM2)),IF(K2=40,43.29*SQRT(ABS(DM2)))))
        fdf.loc[fdf["flapsPos"] ==  0, "v2CASVs"] = 47.32 * np.sqrt(fdf["vnGSmth"].abs())
        fdf.loc[fdf["flapsPos"] == 20, "v2CASVs"] = 45.12 * np.sqrt(fdf["vnGSmth"].abs())
        fdf.loc[fdf["flapsPos"] == 40, "v2CASVs"] = 43.29 * np.sqrt(fdf["vnGSmth"].abs())
        available_cols.append("v2CASVs")

    # v2StallMarCAS - Stall Margin V2 KCAS 
    if ("v2CAS" in available_cols) and ("v2CASVs" in available_cols):
        # =EB2-EC2
        fdf["v2StallMarCAS"] = fdf["v2CAS"] - fdf["v2CASVs"]
        available_cols.append("v2StallMarCAS")

    # EFISIAS - EFIS KIAS (COPY OF efisIAS)
    if ("efisIAS" in available_cols):
        # =BZ2
        fdf["EFISIAS"] = fdf["efisIAS"]
        available_cols.append("EFISIAS")

    # EFISIASVs - EFIS Vs KIAS 
    if ("flapsPos" in available_cols) and ("vnGSmth" in available_cols):
        # =IF(K2=0,50.3*SQRT(ABS(DM2)),IF(K2=20,48.65*SQRT(ABS(DM2)),IF(K2=40,47.76*SQRT(ABS(DM2)))))
        fdf.loc[fdf["flapsPos"] ==  0, "EFISIASVs"] = 50.30 * np.sqrt(fdf["vnGSmth"].abs())
        fdf.loc[fdf["flapsPos"] == 20, "EFISIASVs"] = 48.65 * np.sqrt(fdf["vnGSmth"].abs())
        fdf.loc[fdf["flapsPos"] == 40, "EFISIASVs"] = 47.76 * np.sqrt(fdf["vnGSmth"].abs())
        available_cols.append("EFISIASVs")

    # efisStallMarIAS - Stall Margin EFIS KIAS 
    if ("EFISIAS" in available_cols) and ("EFISIASVs" in available_cols):
        # =EE2-EF2
        fdf["efisStallMarIAS"] = fdf["EFISIAS"] - fdf["EFISIASVs"]
        available_cols.append("efisStallMarIAS")

    # efisCAS - EFIS KCAS 
    if ("efisIAS" in available_cols):
        # =1.0169*BZ2-2.115
        fdf["efisCAS"] = 1.0169 * fdf["efisIAS"] - 2.115
        available_cols.append("efisCAS")

    # efisCASVs - EFIS Vs KCAS 
    if ("flapsPos" in available_cols) and ("vnGSmth" in available_cols):
        # =IF(K2=0,49.04*SQRT(ABS(DM2)),IF(K2=20,49.47*SQRT(ABS(DM2)),IF(K2=40,46.45*SQRT(ABS(DM2)))))
        fdf.loc[fdf["flapsPos"] ==  0, "efisCASVs"] = 49.04 * np.sqrt(fdf["vnGSmth"].abs())
        fdf.loc[fdf["flapsPos"] == 20, "efisCASVs"] = 49.47 * np.sqrt(fdf["vnGSmth"].abs())
        fdf.loc[fdf["flapsPos"] == 40, "efisCASVs"] = 46.45 * np.sqrt(fdf["vnGSmth"].abs())
        available_cols.append("efisCASVs")

    # efisStallMarCAS - Stall Margin EFIS KCAS 
    if ("efisCAS" in available_cols) and ("efisCASVs" in available_cols):
        # =EH2-EI2
        fdf["efisStallMarCAS"] = fdf["efisCAS"] - fdf["efisCASVs"]
        available_cols.append("efisStallMarCAS")

    # AlphMar - Alpha Margin 
    if ("flapsPos" in available_cols) and ("AngleofAttack" in available_cols):
        # =IF(K3=0,15.85-J2,IF(K2=20,15.4-J2,IF(K2=40,15.2-J2)))
        fdf.loc[fdf["flapsPos"] ==  0, "AlphMar"] = 15.85 - fdf["AngleofAttack"]
        fdf.loc[fdf["flapsPos"] == 20, "AlphMar"] = 15.40 - fdf["AngleofAttack"]
        fdf.loc[fdf["flapsPos"] == 40, "AlphMar"] = 15.20 - fdf["AngleofAttack"]
        available_cols.append("AlphMar")

# UP TO HERE

    # AbsAlph - Abs Alpha
    # Based on priCP3Smth
    # priCP3Smth = priP45SmthW / priPFwdSmthW
    if ("flapsPos" in available_cols) and ("v2CP3Smth" in available_cols):
        # =IF(K2=0, 23.67*CQ2+5.423,IF(K2=20,25.039*CQ2+5.7465,IF(K2=40,25.443*CQ2+5.569)))
        fdf.loc[fdf["flapsPos"] ==  0, "AbsAlph"] = 23.670 * fdf["v2CP3Smth"] + 5.4230
        fdf.loc[fdf["flapsPos"] == 20, "AbsAlph"] = 25.039 * fdf["v2CP3Smth"] + 5.7465
        fdf.loc[fdf["flapsPos"] == 40, "AbsAlph"] = 25.443 * fdf["v2CP3Smth"] + 5.5690
        available_cols.append("AbsAlph")
#'=IF(priFlapsPos=0,
# 10.58   * priCP3Smth^2 + 25.139 * priCP3Smth+6.1489
#                          25.039 * priCP3Smth+5.7465
#  8.5839 * priCP3Smth^2 + 21.974 * priCP3Smth+5.8102


    # AbsAlphMar - Abs Alpha Margin 
    if ("flapsPos" in available_cols) and ("AbsAlph" in available_cols):
        # =IF(K2=0,18.03-EN2,IF(K2=20,19.64-EN2,IF(K2=40,20.47-EN2)))
        fdf.loc[fdf["flapsPos"] ==  0, "AbsAlphMar"] = 18.03 - fdf["AbsAlph"]
        fdf.loc[fdf["flapsPos"] == 20, "AbsAlphMar"] = 19.64 - fdf["AbsAlph"]
        fdf.loc[fdf["flapsPos"] == 40, "AbsAlphMar"] = 20.47 - fdf["AbsAlph"]
        available_cols.append("AbsAlphMar")

    # efisCASVsG - EFIS Vs KCAS EFIS G 
    if ("flapsPos" in available_cols) and ("efisVerticalG" in available_cols):
        # =IF(K2=0,49.04*SQRT(ABS(CD2)),IF(K2=20,49.47*SQRT(ABS(CD2)),IF(K2=40,46.45*SQRT(ABS(CD2)))))
        fdf.loc[fdf["flapsPos"] ==  0, "efisCASVsG"] = 49.04 * np.sqrt(fdf["efisVerticalG"].abs())
        fdf.loc[fdf["flapsPos"] == 20, "efisCASVsG"] = 49.47 * np.sqrt(fdf["efisVerticalG"].abs())
        fdf.loc[fdf["flapsPos"] == 40, "efisCASVsG"] = 46.45 * np.sqrt(fdf["efisVerticalG"].abs())
        available_cols.append("efisCASVsG")

    # efisStallMarCASG - Stall Margin EFIS KCAS EFIS G 
    if ("efisCAS" in available_cols) and ("efisCASVsG" in available_cols):
        # =EH2-EO2
        fdf["efisStallMarCASG"] = fdf["efisCAS"] - fdf["efisCASVsG"]
        available_cols.append("efisStallMarCASG")

    # Print warnings so we can see them happen and fix them
    # numpy.seterr(all='warn')


    return fdf