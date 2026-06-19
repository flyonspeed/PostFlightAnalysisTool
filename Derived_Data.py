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

    # Secondary probe type
    sec_probe_type = "Garmin Probe"
    #sec_probe_type = "Spherical Probe"
    #sec_probe_type = "Cheap Probe"

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

    # FIX THESE EQUATIONS SO THEY MAKES SENSE

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
    # =secP45/secPfwd
    if ("secPFwd" in available_cols) and ("secP45" in available_cols):
        eq = "fdf['secP45'] / fdf['secPFwd']"
        ExCol.column_def["secCP3Inst"]["equation"] = eq_strip(eq)
        fdf["secCP3Inst"] = eval(eq)
        available_cols.append("secCP3Inst")

    # secCP3Smth - V3 CP3 Smoothed
    if ("secPFwdSmthW" in available_cols) and ("secP45SmthW" in available_cols):
        eq = "fdf['secP45SmthW'] / fdf['secPFwdSmthW']"
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
        # =0.00000000000070918*AD6^4-0.000000011698*AD6^3+0.000070109*AD6^2-0.21624*AD6+310.21
        # eq = "0.00000000000070918 * np.power(fdf['boomAlphaRaw'], 4) - " \
        #      "0.000000011698      * np.power(fdf['boomAlphaRaw'], 3) + " \
        #      "0.000070109         * np.power(fdf['boomAlphaRaw'], 2) - " \
        #      "0.21624             *          fdf['boomAlphaRaw']     + " \
        #      "310.21"
        eq = "0.00000000000070918 * fdf['boomAlphaRaw'] ** 4 - " \
             "0.000000011698      * fdf['boomAlphaRaw'] ** 3 + " \
             "0.000070109         * fdf['boomAlphaRaw'] ** 2 - " \
             "0.21624             * fdf['boomAlphaRaw']      + " \
             "310.21"
        ExCol.column_def["boomAlpha"]["equation"] = eq_strip(eq)
        fdf["boomAlpha"] = eval(eq)
        available_cols.append("boomAlpha")

    # boomBeta
    # '=0.00000000000020096*boomBetaRaw^4-0.0000000037124*boomBetaRaw^3+0.000025497*boomBetaRaw^2-0.037141*boomBetaRaw-72.506
    if ("boomBetaRaw" in available_cols):
        # eq = "0.00000000000020096 * np.power(fdf['boomBetaRaw'],4) - " \
        #      "0.0000000037124     * np.power(fdf['boomBetaRaw'],3) + " \
        #      "0.000025497         * np.power(fdf['boomBetaRaw'],2) - " \
        #      "0.037141            * fdf['boomBetaRaw']             - " \
        #      "72.506"
        eq = "0.00000000000020096 * fdf['boomBetaRaw'] ** 4 - " \
             "0.0000000037124     * fdf['boomBetaRaw'] ** 3 + " \
             "0.000025497         * fdf['boomBetaRaw'] ** 2 - " \
             "0.037141            * fdf['boomBetaRaw']      - " \
             "72.506"
        ExCol.column_def["boomBeta"]["equation"] = eq_strip(eq)
        fdf["boomBeta"] = eval(eq)
        available_cols.append("boomBeta")

    # boomIASCalc
    # '=SQRT(2*boomDynamic*100/1.225)*1.94384
    if ("boomDynamic" in available_cols):
        eq = "np.sqrt(2*fdf['boomDynamic']*100/1.225) * 1.94384"
        ExCol.column_def["boomIASCalc"]["equation"] = eq_strip(eq)
        fdf["boomIASCalc"] = eval(eq)
        available_cols.append("boomIASCalc")

    # boomTAS1
    # '=boomIASCalc * SQRT(1 / DenRatio)
    if ("boomIASCalc" in available_cols) and ("DenRatio" in available_cols):
        eq = "fdf['boomIASCalc'] * np.sqrt(1.0 / fdf['DenRatio'])"
        ExCol.column_def["boomTAS1"]["equation"] = eq_strip(eq)
        fdf["boomTAS1"] = eval(eq)
        available_cols.append("boomTAS1")

    # boomTAS2
    # '=boomIASCalc * SQRT((1.225 / ((boomStatic * 100) / (287.05 * (priOAT + 273.15)))))
    if ("boomIASCalc" in available_cols) and ("boomStatic" in available_cols) and ("priOAT" in available_cols):
        eq = "fdf['boomIASCalc'] * np.sqrt((1.225 / ((fdf['boomStatic'] * 100) / (287.05 * (fdf['priOAT'] + 273.15)))))"
        ExCol.column_def["boomTAS2"]["equation"] = eq_strip(eq)
        fdf["boomTAS2"] = eval(eq)
        available_cols.append("boomTAS2")

    # boomPAlt
    # '= (1-(boomStatic/1013.25)^0.190284)*145366.45
    # '=(1-(EJ6/1013.25)^0.190284)*145366.45
    if ("boomStatic" in available_cols):
        eq = "(1 - np.power((fdf['boomStatic']/1013.25), 0.190284)) * 145366.45"
        ExCol.column_def["boomPAlt"]["equation"] = eq_strip(eq)
        fdf["boomPAlt"] = eval(eq)
        available_cols.append("boomPAlt")


    # Area 6.  Primary System Airspeeds
    # ---------------------------------
    
    # priIAS
    # '=priIAS

    # priIASSmth
    if ("priIAS" in available_cols):
        eq = "fdf['priIAS'].rolling(25, center=True).mean()"
        ExCol.column_def["priIASSmth"]["equation"] = eq_strip(eq)
        fdf["priIASSmth"] = eval(eq)
        available_cols.append("priIASSmth")

    # priIASSmthRate
    if ("priIASSmth" in available_cols):
        eq = "fdf['priIASSmth'].diff(periods=5).rolling(25, center=True).mean() * 10.0"
        ExCol.column_def["priIASSmthRate"]["equation"] = eq_strip(eq)
        fdf["priIASSmthRate"] = eval(eq)
        available_cols.append("priIASSmthRate")

    # priCAS
    # '=0.9935*priIAS+0.7972
    if ("priIAS" in available_cols):
        eq = "0.9935 * fdf['priIAS'] + 0.7972"
        ExCol.column_def["priCAS"]["equation"] = eq_strip(eq)
        fdf["priCAS"] = eval(eq)
        available_cols.append("priCAS")

    # priCASSmth
    if ("priCAS" in available_cols):
        eq = "fdf['priCAS'].rolling(25, center=True).mean()"
        ExCol.column_def["priCASSmth"]["equation"] = eq_strip(eq)
        fdf["priCASSmth"] = eval(eq)
        available_cols.append("priCASSmth")    
        
    # priCASSmthRate
    if ("priCASSmth" in available_cols):
        eq = "fdf['priCASSmth'].diff(periods=5).rolling(25, center=True).mean() * 10.0"
        ExCol.column_def["priCASSmthRate"]["equation"] = eq_strip(eq)
        fdf["priCASSmthRate"] = eval(eq)
        available_cols.append("priCASSmthRate")

    # priTAS
    # '=priTAS

    # priTASSmth
    if ("priTAS" in available_cols):
        eq = "fdf['priTAS'].rolling(25, center=True).mean()"
        ExCol.column_def["priTASSmth"]["equation"] = eq_strip(eq)
        fdf["priTASSmth"] = eval(eq)
        available_cols.append("priTASSmth")
        
    # priTASSmthRate
    if ("priTASSmth" in available_cols):
        eq = "fdf['priTASSmth'].diff(periods=10) * 5.0"
        ExCol.column_def["priTASSmthRate"]["equation"] = eq_strip(eq)
        fdf["priTASSmthRate"] = eval(eq)
        available_cols.append("priTASSmthRate")

    # priTASMS - TAS M/S 
    # =I2*(1+(H2/1000*0.017))*0.5144
    if ("priTAS" in available_cols):
        eq = "fdf['priTAS'] * 0.5144"
        ExCol.column_def["priTASMS"]["equation"] = eq_strip(eq)
        fdf["priTASMS"] = eval(eq)
        available_cols.append("priTASMS")

    # priTASFPS - TAS FPS 
    # =DO2*2.28084
    if ("priTAS" in available_cols):
        eq = "fdf['priTAS'] * 1.68781"
        ExCol.column_def["priTASFPS"]["equation"] = eq_strip(eq)
        fdf["priTASFPS"] = eval(eq)
        available_cols.append("priTASFPS")

    # Area 7.  Secondary System Airspeeds
    # -----------------------------------
    
    # secIASCalc
    # '=SQRT(2*((secPFwdSmthMB+secPStatic)-priPStatic)*100/1.225)*1.94384
    if ("secPFwdSmthMB" in available_cols) and ("secPStatic" in available_cols) and ("priPStatic" in available_cols):
        eq = "np.sqrt(2*(fdf['secPFwdSmthMB']+fdf['secPStatic']-fdf['priPStatic'])*100/1.225)*1.94384"
        ExCol.column_def["secIASCalc"]["equation"] = eq_strip(eq)
        fdf["secIASCalc"] = eval(eq)
        available_cols.append("secIASCalc")

    # secIASSmth
    if ("secIASCalc" in available_cols):
        eq = "fdf['secIASCalc'].rolling(25, center=True).mean()"
        ExCol.column_def["secIASSmth"]["equation"] = eq_strip(eq)
        fdf["secIASSmth"] = eval(eq)
        available_cols.append("secIASSmth")

    # secIASSmthRate
    if ("secIASSmth" in available_cols):
        eq = "fdf['secIASSmth'].diff(periods=5).rolling(25, center=True).mean() * 10.0"
        ExCol.column_def["secIASSmthRate"]["equation"] = eq_strip(eq)
        fdf["secIASSmthRate"] = eval(eq)
        available_cols.append("secIASSmthRate")

    # secCAS
    if ("secIASCalc" in available_cols):
        eq = "0.9853 * fdf['secIASCalc'] + 2.9687"; # Garmin Probe
        # eq = "1.0068 * fdf['secIASCalc'] - 1.5028"; # Spherical Probe
        ExCol.column_def["secCAS"]["equation"] = sec_probe_type + "\n" + eq_strip(eq)
        fdf["secCAS"] = eval(eq)
        available_cols.append("secCAS")

    # secCASSmth
    if ("secCAS" in available_cols):
        eq = "fdf['secCAS'].rolling(25, center=True).mean()"
        ExCol.column_def["secCASSmth"]["equation"] = eq_strip(eq)
        fdf["secCASSmth"] = eval(eq)
        available_cols.append("secCASSmth")

    # secCASSmthRate
    if ("secCASSmth" in available_cols):
        eq = "fdf['secCASSmth'].diff(periods=5).rolling(25, center=True).mean() * 10.0"
        ExCol.column_def["secCASSmthRate"]["equation"] = eq_strip(eq)
        fdf["secCASSmthRate"] = eval(eq)
        available_cols.append("secCASSmthRate")

    # Area 8.  Attitude, Performance and G
    # ------------------------------------
    
    # 
    # vnPitch
    # '=vnPitch

    # vnPitchRateDeg - VN Pitch Rate (deg/sec) 
    # =vnPitchRateDeg*57.2958
    if ("vnAngularRatePitch" in available_cols):
        eq = "fdf['vnAngularRatePitch'] * 57.2958"
        ExCol.column_def["vnPitchRateDeg"]["equation"] = eq_strip(eq)
        fdf["vnPitchRateDeg"] = eval(eq)
        available_cols.append("vnPitchRateDeg")

    # vnPitchRateSmthDeg - VN Pitch Rate Smoothed (deg/sec) 
    if ("vnPitchRateDeg" in available_cols):
        eq = "fdf['vnPitchRateDeg'].rolling(25, center=True).mean()"
        ExCol.column_def["vnPitchRateSmthDeg"]["equation"] = eq_strip(eq)
        fdf["vnPitchRateSmthDeg"] = eval(eq)
        available_cols.append("vnPitchRateSmthDeg")

    # vnRoll
    # '=vnRoll

    # vnRollRateDeg - VN Roll Rate (deg/sec) 
    # =vnAngularRateRoll*57.2958
    if ("vnAngularRateRoll" in available_cols):
        eq = "fdf['vnAngularRateRoll'] * 57.2958"
        ExCol.column_def["vnRollRateDeg"]["equation"] = eq_strip(eq)
        fdf["vnRollRateDeg"] = eval(eq)
        available_cols.append("vnRollRateDeg")

    # vnRollRateSmthDeg - VN Roll Rate Smoothed (deg/sec) 
    if ("vnRollRateDeg" in available_cols):
        eq = "fdf['vnRollRateDeg'].rolling(25, center=True).mean()"
        ExCol.column_def["vnRollRateSmthDeg"]["equation"] = eq_strip(eq)
        fdf["vnRollRateSmthDeg"] = eval(eq)
        available_cols.append("vnRollRateSmthDeg")

    # boomBeta
    # '=boomBeta

    # boomBetaRateDeg
    # '=vnAngularRateYaw * 180 / 3.1416
    if ("vnAngularRateYaw" in available_cols):
        eq = "fdf['vnAngularRateYaw'] * 180 / 3.1416"
        ExCol.column_def["boomBetaRateDeg"]["equation"] = eq_strip(eq)
        fdf["boomBetaRateDeg"] = eval(eq)
        available_cols.append("boomBetaRateDeg")

    # boomBetaRateSmthDeg
    if ("boomBetaRateDeg" in available_cols):
        eq = "fdf['boomBetaRateDeg'].rolling(50, center=True).mean()"
        ExCol.column_def["boomBetaRateSmthDeg"]["equation"] = eq_strip(eq)
        fdf["boomBetaRateSmthDeg"] = eval(eq)
        available_cols.append("boomBetaRateSmthDeg")

    # vnFltPth - VN Flight Path Angle (deg) 
    # =ASIN(-AG2/DO2)*180/PI()
    if ("vnVelNedDown" in available_cols) and ("priTASMS" in available_cols):
        eq = "np.arcsin(-fdf['vnVelNedDown']/fdf['priTASMS']) * 180 / 3.1416"
        ExCol.column_def["vnFltPth"]["equation"] = eq_strip(eq)
        # Ignore harmless warnings so they won't print
        np.seterr(all='ignore')
        fdf["vnFltPth"] =  eval(eq)
        np.seterr(all='print')
        available_cols.append("vnFltPth")

    # vnFltPthCor
    # '=ASIN(-vnVelNedDown/priTASMS)*180/PI()-(priEarthVerticalG/9.80955)
    if ("vnVelNedDown" in available_cols) and ("priTASMS" in available_cols) and ("priEarthVerticalG" in available_cols):
        eq = "np.arcsin(-fdf['vnVelNedDown']/fdf['priTASMS'])*180/3.1416-(fdf['priEarthVerticalG']/9.80955)"
        ExCol.column_def["vnFltPthCor"]["equation"] = eq_strip(eq)
        fdf["vnFltPthCor"] = eval(eq)
        available_cols.append("vnFltPthCor")

    # vnTHdg - VN True Heading (deg) 
    # =IF(AK2>0,AK2,IF(AK2<0,360-ABS(AK2)))
    if ("vnYaw" in available_cols):
        ExCol.column_def["vnTHdg"]["equation"] = "if vnYaw >= 0 vnTHdg = vnYaw\nif vnYaw < 0 vnTHdg = 360-abs(vnYaw)"
        fdf.loc[fdf["vnYaw"] >= 0, "vnTHdg"] = fdf["vnYaw"]
        fdf.loc[fdf["vnYaw"] <  0, "vnTHdg"] = 360 - fdf["vnYaw"].abs()
        available_cols.append("vnTHdg")

    # vnIVVI - VN IVVI (FPM) 
    # =-(vnVelNedDown/0.00508)
    if ("vnVelNedDown" in available_cols):
        eq = "-fdf['vnVelNedDown'] / 0.00508"
        ExCol.column_def["vnIVVI"]["equation"] = eq_strip(eq)
        fdf["vnIVVI"] = eval(eq)
        available_cols.append("vnIVVI")

    # vnTrnRateDeg
    # '=ABS(vnAngularRateYaw*57.2958)
    if ("vnAngularRateYaw" in available_cols):
        eq = "fdf['vnAngularRateYaw'].abs() * 57.2958"
        ExCol.column_def["vnTrnRateDeg"]["equation"] = eq_strip(eq)
        fdf["vnTrnRateDeg"] = eval(eq)
        available_cols.append("vnTrnRateDeg")

    # vnTrnRateDegSmth
    if ("vnTrnRateDeg" in available_cols):
        eq = "fdf['vnTrnRateDeg'].rolling(50, center=True).mean()"
        ExCol.column_def["vnTrnRateDegSmth"]["equation"] = eq_strip(eq)
        fdf["vnTrnRateDegSmth"] = eval(eq)
        available_cols.append("vnTrnRateDegSmth")

    # vnTrnRadFt
    # '=(priTAS^2/(11.26*TAN(ABS(vnRoll)*0.017453)))
    if ("priTAS" in available_cols) and ("vnRoll" in available_cols):
        eq = "fdf['priTAS'] ** 2/(11.26*np.tan(fdf['vnRoll'].abs()*0.017453))"
        ExCol.column_def["vnTrnRadFt"]["equation"] = eq_strip(eq)
        fdf["vnTrnRadFt"] = eval(eq)
        available_cols.append("vnTrnRadFt")

    # priGSmth
    # abf(priVerticalG)
    if ("priVerticalG" in available_cols):
        eq = "fdf['priVerticalG'].rolling(50, center=True).mean()"
        ExCol.column_def["priGSmth"]["equation"] = eq_strip(eq)
        fdf["priGSmth"] = eval(eq)
        available_cols.append("priGSmth")

    # secGSmth
    # abf(secVerticalG)
    if ("secVerticalG" in available_cols):
        eq = "fdf['secVerticalG'].rolling(50, center=True).mean()"
        ExCol.column_def["secGSmth"]["equation"] = eq_strip(eq)
        fdf["secGSmth"] = eval(eq)
        available_cols.append("secGSmth")

    # vnG - VN G 
    # vnGSmth - VN G Smoothed 
    # =-(AJ2/9.80655)
    if "vnAccelVert" in available_cols:
        eq = "-fdf['vnAccelVert'] / 9.80655"
        ExCol.column_def["vnG"]["equation"] = eq_strip(eq)
        fdf["vnG"] = eval(eq)
        available_cols.append("vnG")

        eq = "fdf['vnG'].rolling(25, center=True).mean()"
        ExCol.column_def["vnGSmth"]["equation"] = eq_strip(eq)
        fdf["vnGSmth"] = eval(eq)
        available_cols.append("vnGSmth")


    # Area 9.  Angle of Attack
    # ------------------------
    
    # vnDerAlph - VN Derived Alpha (deg) 
    # vnDrAlphSmth
    # =AL2-DQ2
    if ("vnPitch" in available_cols) and ("vnFltPthCor" in available_cols):
        eq = "fdf['vnPitch'] - fdf['vnFltPthCor']"
        ExCol.column_def["vnDerAlph"]["equation"] = eq_strip(eq)
        fdf["vnDerAlph"] = eval(eq)
        available_cols.append("vnDerAlph")

        eq = "fdf['vnDerAlph'].rolling(25, center=True).mean()"
        ExCol.column_def["vnDrAlphSmth"]["equation"] = eq_strip(eq)
        fdf["vnDrAlphSmth"] = eval(eq)
        available_cols.append("vnDrAlphSmth")

    # vnDrAlphRate
    # vnDrAlphRateSmth
    if ("vnDerAlph" in available_cols):
        eq = "fdf['vnDerAlph'].diff(periods=5) * 10.0"
        ExCol.column_def["vnDrAlphRate"]["equation"] = eq_strip(eq)
        fdf["vnDrAlphRate"] = eval(eq)
        available_cols.append("vnDrAlphRate")

        eq = "fdf['vnDrAlphRate'].rolling(25, center=True).mean()"
        ExCol.column_def["vnDrAlphRateSmth"]["equation"] = eq_strip(eq)
        fdf["vnDrAlphRateSmth"] = eval(eq)
        available_cols.append("vnDrAlphRateSmth")

    # boomAlphaCor
    # boomAlphCorSmth
    # '=IF(priFlapsPos=0,0.7917*boomAlpha-1.2758,IF(priFlapsPos=20,0.7979*boomAlpha-1.6647,IF(priFlapsPos=40,0.7863*boomAlpha-1.7172)))-(0.1264*(-vnAccelVert/9.80655-1))+(3.08*(vnAngularRatePitch*57.2958)/(priTAS*1.68781)+(10.19*(vnAngularRateRoll*57.2958)/(priTAS*1.68781)))
    # abf(boomAlphaCor)
    if ("priFlapsPos" in available_cols) and ("vnAccelVert" in available_cols) and ("vnAngularRatePitch" in available_cols) and ("vnAngularRateRoll" in available_cols) and ("priTAS" in available_cols):
        eq_corr_1 = "-(0.1264*(-fdf['vnAccelVert']/9.80655-1))"
        eq_corr_2 = "+( 3.08 * (fdf['vnAngularRatePitch']* 57.2958) / (fdf['priTAS']*1.68781))"
        eq_corr_3 = "+(10.19 * (fdf['vnAngularRateRoll'] * 57.2958) / (fdf['priTAS']*1.68781))"
        eq_1 = "0.7917 * fdf['boomAlpha'] - 1.2758" + eq_corr_1 + eq_corr_2 + eq_corr_3
        eq_2 = "0.7979 * fdf['boomAlpha'] - 1.6647" + eq_corr_1 + eq_corr_2 + eq_corr_3
        eq_3 = "0.7863 * fdf['boomAlpha'] - 1.7172" + eq_corr_1 + eq_corr_2 + eq_corr_3
        
        ExCol.column_def["boomAlphaCor"]["equation"] = eq_strip("'Flaps 0'  "  + eq_1 + " + Corrections \n" + 
                                                                "'Flaps 20'  " + eq_2 + " + Corrections \n" + 
                                                                "'Flaps 40'  " + eq_3 + " + Corrections")
        fdf.loc[fdf['priFlapsPos'] ==  0, 'boomAlphaCor'] = eval(eq_1)
        fdf.loc[fdf['priFlapsPos'] == 20, 'boomAlphaCor'] = eval(eq_2)
        fdf.loc[fdf['priFlapsPos'] == 40, 'boomAlphaCor'] = eval(eq_3)
        available_cols.append("boomAlphaCor")

        eq = "fdf['boomAlphaCor'].rolling(25, center=True).mean()"
        ExCol.column_def["boomAlphCorSmth"]["equation"] = eq_strip(eq)
        fdf["boomAlphCorSmth"] = eval(eq)
        available_cols.append("boomAlphCorSmth")

    # boomAlphaRate
    # boomAlphaRateSmth
    if ("boomAlphaCor" in available_cols):
        eq = "fdf['boomAlphaCor'].diff(periods=5) * 10.0"
        ExCol.column_def["boomAlphaRate"]["equation"] = eq_strip(eq)
        fdf["boomAlphaRate"] = eval(eq)
        available_cols.append("boomAlphaRate")

        eq = "fdf['boomAlphaRate'].rolling(25, center=True).mean()"
        ExCol.column_def["boomAlphaRateSmth"]["equation"] = eq_strip(eq)
        fdf["boomAlphaRateSmth"] = eval(eq)
        available_cols.append("boomAlphaRateSmth")


    # CockpitAngleofAttack
    # CockpitAngleofAttackSmth
    # =priAngleOfAttack
    if ("priAngleOfAttack" in available_cols):
        eq = "fdf['priAngleOfAttack'].rolling(50, center=True).mean()"
        ExCol.column_def["CockpitAngleofAttackSmth"]["equation"] = eq_strip(eq)
        fdf["CockpitAngleofAttackSmth"] = eval(eq)
        available_cols.append("CockpitAngleofAttackSmth")

    # CockpitAngleofAttackRate
    # CockpitAngleofAttackRateSmth
    if ("priAngleOfAttack" in available_cols):
        eq = "fdf['priAngleOfAttack'].diff(periods=5) * 10.0"
        ExCol.column_def["CockpitAngleofAttackRate"]["equation"] = eq_strip(eq)
        fdf["CockpitAngleofAttackRate"] = eval(eq)
        available_cols.append("CockpitAngleofAttackRate")

        eq = "fdf['CockpitAngleofAttackRate'].rolling(25, center=True).mean()"
        ExCol.column_def["CockpitAngleofAttackRateSmth"]["equation"] = eq_strip(eq)
        fdf["CockpitAngleofAttackRateSmth"] = eval(eq)
        available_cols.append("CockpitAngleofAttackRateSmth")

    # priAlpha
    # priAlphaSmth
    # '=IF(priFlapsPos=0,6.5805*priCP3Smth^2+22.763*priCP3Smth+4.3907,IF(priFlapsPos=20,-4.0083*priCP3Smth^2+29.537*priCP3Smth+2.6034,IF(priFlapsPos=40,-5.6802*priCP3Smth^2+31.567*priCP3Smth+1.0169)))
    # MAYBE USE priCP3 INSTEAD?
    if ("priFlapsPos" in available_cols) and ("priCP3Smth" in available_cols):
        eq_1 = " 6.5805 * fdf['priCP3Smth'] ** 2 + 22.763 * fdf['priCP3Smth'] + 4.3907"
        eq_2 = "-4.0083 * fdf['priCP3Smth'] ** 2 + 29.537 * fdf['priCP3Smth'] + 2.6034"
        eq_3 = "-5.6802 * fdf['priCP3Smth'] ** 2 + 31.567 * fdf['priCP3Smth'] + 1.0169"
        
        ExCol.column_def["priAlpha"]["equation"] = eq_strip("'Flaps 0'  " + eq_1 + "\n'Flaps 20'  " + eq_2 + "\n'Flaps 40'  " + eq_3)
        fdf.loc[fdf['priFlapsPos'] ==  0, 'priAlpha'] = eval(eq_1)
        fdf.loc[fdf['priFlapsPos'] == 20, 'priAlpha'] = eval(eq_2)
        fdf.loc[fdf['priFlapsPos'] == 40, 'priAlpha'] = eval(eq_3)
        available_cols.append("priAlpha")

        eq = "fdf['priAlpha'].rolling(25, center=True).mean()"
        ExCol.column_def["priAlphaSmth"]["equation"] = eq_strip(eq)
        fdf["priAlphaSmth"] = eval(eq)
        available_cols.append("priAlphaSmth")

    # priAlphaRate
    # priAlphaRateSmth
    if ("priAlpha" in available_cols):
        eq = "fdf['priAlpha'].diff(periods=5) * 10.0"
        ExCol.column_def["priAlphaRate"]["equation"] = eq_strip(eq)
        fdf["priAlphaRate"] = eval(eq)
        available_cols.append("priAlphaRate")

        eq = "fdf['priAlphaRate'].rolling(25, center=True).mean()"
        ExCol.column_def["priAlphaRateSmth"]["equation"] = eq_strip(eq)
        fdf["priAlphaRateSmth"] = eval(eq)
        available_cols.append("priAlphaRateSmth")

    # secAlphaCP3
    # secAlphaCP3Smth
    if ("priFlapsPos" in available_cols) and ("secCP3Inst" in available_cols):
        # Garmin probe
        eq_1 = "-6.869 * fdf['secCP3Inst'] ** 2 + 28.607 * fdf['secCP3Inst'] + 3.1241"
        eq_2 = "0.9601 * fdf['secCP3Inst'] ** 2 + 23.808 * fdf['secCP3Inst'] + 2.4466"
        eq_3 = "7.5118 * fdf['secCP3Inst'] ** 2 + 20.735 * fdf['secCP3Inst'] + 1.0269"
        # Spherical probe
        # eq_1 = "1.0726 * fdf['secCP3Inst'] ** 2 + 21.136 * fdf['secCP3Inst'] + 10.164"
        # eq_2 = "8.4879 * fdf['secCP3Inst'] ** 2 + 20.827 * fdf['secCP3Inst'] + 8.6943"
        # eq_3 = "7.2186 * fdf['secCP3Inst'] ** 2 + 21.981 * fdf['secCP3Inst'] + 7.6559"
        # Cheap probe
        # eq_1 = "0.0682 * fdf['secCP3Inst'] ** 2 + 18.396 * fdf['secCP3Inst'] + 10.427"
        # eq_2 = "3.341  * fdf['secCP3Inst'] ** 2 + 18.493 * fdf['secCP3Inst'] + 8.8715"
        # eq_3 = "5.907  * fdf['secCP3Inst'] ** 2 + 18.691 * fdf['secCP3Inst'] + 6.8747"

        ExCol.column_def["secAlphaCP3"]["equation"] = sec_probe_type + "\n" + eq_strip("'Flaps 0'  " + eq_1 + "\n'Flaps 20'  " + eq_2 + "\n'Flaps 40'  " + eq_3)
        fdf.loc[fdf['priFlapsPos'] ==  0, 'secAlphaCP3'] = eval(eq_1)
        fdf.loc[fdf['priFlapsPos'] == 20, 'secAlphaCP3'] = eval(eq_2)
        fdf.loc[fdf['priFlapsPos'] == 40, 'secAlphaCP3'] = eval(eq_3)
        available_cols.append("secAlphaCP3")

        eq = "fdf['secAlphaCP3'].rolling(25, center=True).mean()"
        ExCol.column_def["secAlphaCP3Smth"]["equation"] = eq_strip(eq)
        fdf["secAlphaCP3Smth"] = eval(eq)
        available_cols.append("secAlphaCP3Smth")

    # secAlphaCP3Rate
    # secAlphaCP3RateSmth
    if ("secAlphaCP3" in available_cols):
        eq = "fdf['secAlphaCP3'].diff(periods=5) * 10.0"
        ExCol.column_def["secAlphaCP3Rate"]["equation"] = eq_strip(eq)
        fdf["secAlphaCP3Rate"] = eval(eq)
        available_cols.append("secAlphaCP3Rate")

        eq = "fdf['secAlphaCP3Rate'].rolling(25, center=True).mean()"
        ExCol.column_def["secAlphaCP3RateSmth"]["equation"] = eq_strip(eq)
        fdf["secAlphaCP3RateSmth"] = eval(eq)
        available_cols.append("secAlphaCP3RateSmth")

    # secAlphaCP4
    # secAlphaCP4Smth
    if ("priFlapsPos" in available_cols) and ("secCP4Inst" in available_cols):
        # Garmin probe
        eq_1 = "-6.869 * fdf['secCP4Inst'] ** 2 + 28.607 * fdf['secCP4Inst'] + 3.1241"
        eq_2 = "0.9601 * fdf['secCP4Inst'] ** 2 + 23.808 * fdf['secCP4Inst'] + 2.4466"
        eq_3 = "7.5118 * fdf['secCP4Inst'] ** 2 + 20.735 * fdf['secCP4Inst'] + 1.0269"
        # Spherical probe
        # eq_1 = "1.0726 * fdf['secCP4Inst'] ** 2 + 21.136 * fdf['secCP4Inst'] + 10.164"
        # eq_2 = "8.4879 * fdf['secCP4Inst'] ** 2 + 20.827 * fdf['secCP4Inst'] + 8.6943"
        # eq_3 = "7.2186 * fdf['secCP4Inst'] ** 2 + 21.981 * fdf['secCP4Inst'] + 7.6559"
        # Cheap probe
        # eq_1 = "0.0682 * fdf['secCP4Inst'] ** 2 + 18.396 * fdf['secCP4Inst'] + 10.427"
        # eq_2 = "3.341  * fdf['secCP4Inst'] ** 2 + 18.493 * fdf['secCP4Inst'] + 8.8715"
        # eq_3 = "5.907  * fdf['secCP4Inst'] ** 2 + 18.691 * fdf['secCP4Inst'] + 6.8747"

        ExCol.column_def["secAlphaCP4"]["equation"] = sec_probe_type + "\n" + eq_strip("'Flaps 0'  " + eq_1 + "\n'Flaps 20'  " + eq_2 + "\n'Flaps 40'  " + eq_3)
        fdf.loc[fdf['priFlapsPos'] ==  0, 'secAlphaCP4'] = eval(eq_1)
        fdf.loc[fdf['priFlapsPos'] == 20, 'secAlphaCP4'] = eval(eq_2)
        fdf.loc[fdf['priFlapsPos'] == 40, 'secAlphaCP4'] = eval(eq_3)
        available_cols.append("secAlphaCP4")

        eq = "fdf['secAlphaCP4'].rolling(25, center=True).mean()"
        ExCol.column_def["secAlphaCP4Smth"]["equation"] = eq_strip(eq)
        fdf["secAlphaCP4Smth"] = eval(eq)
        available_cols.append("secAlphaCP4Smth")

    # secAlphaCP4Rate
    # secAlphaCP4RateSmth
    if ("secAlphaCP4" in available_cols):
        eq = "fdf['secAlphaCP4'].diff(periods=5) * 10.0"
        ExCol.column_def["secAlphaCP4Rate"]["equation"] = eq_strip(eq)
        fdf["secAlphaCP4Rate"] = eval(eq)
        available_cols.append("secAlphaCP4Rate")

        eq = "fdf['secAlphaCP4Rate'].rolling(25, center=True).mean()"
        ExCol.column_def["secAlphaCP4RateSmth"]["equation"] = eq_strip(eq)
        fdf["secAlphaCP4RateSmth"] = eval(eq)
        available_cols.append("secAlphaCP4RateSmth")

    # priAbsAlph
    # priAbsAlphaSmth
    # DOUBLE CHECK THIS EQUATION
    # '=IF(priFlapsPos=0,10.58*priCP3Smth^2+25.139*priCP3Smth+6.1489,IF(priFlapsPos=20,25.039*priCP3Smth+5.7465,IF(priFlapsPos=40,8.5839*priCP3Smth^2+21.974*priCP3Smth+5.8102)))
    if ("priFlapsPos" in available_cols) and ("priCP3Smth" in available_cols):
        eq_1 = "10.58   * fdf['priCP3Smth'] ** 2 + 25.139 * fdf['priCP3Smth'] + 6.1489"
        eq_2 = "                                   25.039 * fdf['priCP3Smth'] + 5.7465"
        eq_3 = " 8.5839 * fdf['priCP3Smth'] ** 2 + 21.974 * fdf['priCP3Smth'] + 5.8102"
        
        ExCol.column_def["priAbsAlph"]["equation"] = eq_strip("'Flaps 0'  " + eq_1 + "\n'Flaps 20'  " + eq_2 + "\n'Flaps 40'  " + eq_3)
        fdf.loc[fdf['priFlapsPos'] ==  0, 'priAbsAlph'] = eval(eq_1)
        fdf.loc[fdf['priFlapsPos'] == 20, 'priAbsAlph'] = eval(eq_2)
        fdf.loc[fdf['priFlapsPos'] == 40, 'priAbsAlph'] = eval(eq_3)
        available_cols.append("priAbsAlph")

        eq = "fdf['priAbsAlph'].rolling(25, center=True).mean()"
        ExCol.column_def["priAbsAlphaSmth"]["equation"] = eq_strip(eq)
        fdf["priAbsAlphaSmth"] = eval(eq)
        available_cols.append("priAbsAlphaSmth")

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
    if ("boomAlphCorSmth" in available_cols) and ("CockpitAngleofAttackSmth" in available_cols):
        eq = "np.abs(fdf['boomAlphCorSmth'] - fdf['CockpitAngleofAttackSmth'])"
        ExCol.column_def["boomvsCockpit"]["equation"] = eq_strip(eq)
        fdf["boomvsCockpit"] = eval(eq)
        available_cols.append("boomvsCockpit")

    # vnvsCockpit
    # '=ABS(vnDrAlphSmth-CockpitAngleofAttackSmth)
    if ("vnDrAlphSmth" in available_cols) and ("CockpitAngleofAttackSmth" in available_cols):
        eq = "np.abs(fdf['vnDrAlphSmth'] - fdf['CockpitAngleofAttackSmth'])"
        ExCol.column_def["vnvsCockpit"]["equation"] = eq_strip(eq)
        fdf["vnvsCockpit"] = eval(eq)
        available_cols.append("vnvsCockpit")

    # boomvspri
    # '=ABS(boomAlphCorSmth-priAlphaSmth)
    if ("boomAlphCorSmth" in available_cols) and ("priAlphaSmth" in available_cols):
        eq = "np.abs(fdf['boomAlphCorSmth'] - fdf['priAlphaSmth'])"
        ExCol.column_def["boomvspri"]["equation"] = eq_strip(eq)
        fdf["boomvspri"] = eval(eq)
        available_cols.append("boomvspri")

    # vnvspri
    # '=ABS(vnDrAlphSmth-priAlphaSmth)
    if ("vnDrAlphSmth" in available_cols) and ("priAlphaSmth" in available_cols):
        eq = "np.abs(fdf['vnDrAlphSmth'] - fdf['priAlphaSmth'])"
        ExCol.column_def["vnvspri"]["equation"] = eq_strip(eq)
        fdf["vnvspri"] = eval(eq)
        available_cols.append("vnvspri")

    # boomvssecCP3
    # '=ABS(boomAlphCorSmth-secAlphaCP3Smth)
    if ("boomAlphCorSmth" in available_cols) and ("secAlphaCP3Smth" in available_cols):
        eq = "np.abs(fdf['boomAlphCorSmth'] - fdf['secAlphaCP3Smth'])"
        ExCol.column_def["boomvssecCP3"]["equation"] = eq_strip(eq)
        fdf["boomvssecCP3"] = eval(eq)
        available_cols.append("boomvssecCP3")

    # vnvssecCP3
    # '=ABS(vnDrAlphSmth-secAlphaCP3Smth)
    if ("vnDrAlphSmth" in available_cols) and ("secAlphaCP3Smth" in available_cols):
        eq = "np.abs(fdf['vnDrAlphSmth'] - fdf['secAlphaCP3Smth'])"
        ExCol.column_def["vnvssecCP3"]["equation"] = eq_strip(eq)
        fdf["vnvssecCP3"] = eval(eq)
        available_cols.append("vnvssecCP3")

    # boomvssecCP4
    # '=ABS(boomAlphCorSmth-secAlphaCP4Smth)
    if ("boomAlphCorSmth" in available_cols) and ("secAlphaCP4Smth" in available_cols):
        eq = "np.abs(fdf['boomAlphCorSmth'] - fdf['secAlphaCP4Smth'])"
        ExCol.column_def["boomvssecCP4"]["equation"] = eq_strip(eq)
        fdf["boomvssecCP4"] = eval(eq)
        available_cols.append("boomvssecCP4")

    # vnvssecCP4
    # '=ABS(vnDrAlphSmth-secAlphaCP4Smth)
    if ("vnDrAlphSmth" in available_cols) and ("secAlphaCP4Smth" in available_cols):
        eq = "np.abs(fdf['vnDrAlphSmth'] - fdf['secAlphaCP4Smth'])"
        ExCol.column_def["vnvssecCP4"]["equation"] = eq_strip(eq)
        fdf["vnvssecCP4"] = eval(eq)
        available_cols.append("vnvssecCP4")


    # Area 12. Disagreements
    # ----------------------
    
    # priDisagvnRoll
    # '=ABS(priRoll-vnRoll)
    if ("priRoll" in available_cols) and ("vnRoll" in available_cols):
        eq = "np.abs(fdf['priRoll'] - fdf['vnRoll'])"
        ExCol.column_def["priDisagvnRoll"]["equation"] = eq_strip(eq)
        fdf["priDisagvnRoll"] = eval(eq)
        available_cols.append("priDisagvnRoll")

    # priDisagvnPitch
    # '=ABS(priPitch-vnPitch)
    if ("priPitch" in available_cols) and ("vnPitch" in available_cols):
        eq = "np.abs(fdf['priPitch'] - fdf['vnPitch'])"
        ExCol.column_def["priDisagvnPitch"]["equation"] = eq_strip(eq)
        fdf["priDisagvnPitch"] = eval(eq)
        available_cols.append("priDisagvnPitch")

    # priDisagefisPAlt
    # '=ABS(priAltitude-efisPAlt)
    if ("priAltitude" in available_cols) and ("efisPAlt" in available_cols):
        eq = "np.abs(fdf['priAltitude'] - fdf['efisPAlt'])"
        ExCol.column_def["priDisagefisPAlt"]["equation"] = eq_strip(eq)
        fdf["priDisagefisPAlt"] = eval(eq)
        available_cols.append("priDisagefisPAlt")

    # priDisagefisKIAS
    # '=ABS(priIAS-efisIAS)
    if ("priIAS" in available_cols) and ("efisIAS" in available_cols):
        eq = "np.abs(fdf['priIAS'] - fdf['efisIAS'])"
        ExCol.column_def["priDisagefisKIAS"]["equation"] = eq_strip(eq)
        fdf["priDisagefisKIAS"] = eval(eq)
        available_cols.append("priDisagefisKIAS")

    # priDisagboomPAlt
    # '=ABS(boomPAlt-priAltitude)
    if ("boomPAlt" in available_cols) and ("priAltitude" in available_cols):
        eq = "np.abs(fdf['boomPAlt'] - fdf['priAltitude'])"
        ExCol.column_def["priDisagboomPAlt"]["equation"] = eq_strip(eq)
        fdf["priDisagboomPAlt"] = eval(eq)
        available_cols.append("priDisagboomPAlt")

    # priDisagboomKIAS
    # '=ABS(priIAS-boomBeta)
    if ("priIAS" in available_cols) and ("boomBeta" in available_cols):
        eq = "np.abs(fdf['priIAS'] - fdf['boomBeta'])"
        ExCol.column_def["priDisagboomKIAS"]["equation"] = eq_strip(eq)
        fdf["priDisagboomKIAS"] = eval(eq)
        available_cols.append("priDisagboomKIAS")

    # priDisagboomTAS
    # '=ABS(priTAS-boomTAS1)
    if ("priTAS" in available_cols) and ("boomTAS1" in available_cols):
        eq = "np.abs(fdf['priTAS'] - fdf['boomTAS1'])"
        ExCol.column_def["priDisagboomTAS"]["equation"] = eq_strip(eq)
        fdf["priDisagboomTAS"] = eval(eq)
        available_cols.append("priDisagboomTAS")


    # Area 13.  Aerodynamic Margin
    # ----------------------------
    
    # priKIASStall
    # '=IF(priFlapsPos=0,46.47*SQRT(ABS(vnGSmth)),IF(priFlapsPos=20,44.92*SQRT(ABS(vnGSmth)),IF(priFlapsPos=40,42.88*SQRT(ABS(vnGSmth)))))
    if ("priFlapsPos" in available_cols) and ("vnGSmth" in available_cols):
        eq_1 = "46.47 * np.sqrt(fdf['vnGSmth'].abs())"
        eq_2 = "44.92 * np.sqrt(fdf['vnGSmth'].abs())"
        eq_3 = "42.88 * np.sqrt(fdf['vnGSmth'].abs())"
        
        ExCol.column_def["priKIASStall"]["equation"] = eq_strip("'Flaps 0'  " + eq_1 + "\n'Flaps 20'  " + eq_2 + "\n'Flaps 40'  " + eq_3)
        fdf.loc[fdf['priFlapsPos'] ==  0, 'priKIASStall'] = eval(eq_1)
        fdf.loc[fdf['priFlapsPos'] == 20, 'priKIASStall'] = eval(eq_2)
        fdf.loc[fdf['priFlapsPos'] == 40, 'priKIASStall'] = eval(eq_3)
        available_cols.append("priKIASStall")
        
    # priKIASStallMar
    # =priIAS-priKIASStall
    if ("priIAS" in available_cols) and ("priKIASStall" in available_cols):
        eq = "fdf['priIAS'] - fdf['priKIASStall']"
        ExCol.column_def["priKIASStallMar"]["equation"] = eq_strip(eq)
        fdf["priKIASStallMar"] = eval(eq)
        available_cols.append("priKIASStallMar")

    # priAOAStallMarSmth
    # '=IF(priFlapsPos=0,18.72-priAlphaSmth,IF(priFlapsPos=20,18.18-priAlphaSmth,IF(priFlapsPos=40,17.86-priAlphaSmth)))
    if ("priFlapsPos" in available_cols) and ("priAlphaSmth" in available_cols):
        eq_1 = "18.72 - fdf['priAlphaSmth']"
        eq_2 = "18.18 - fdf['priAlphaSmth']"
        eq_3 = "17.86 - fdf['priAlphaSmth']"
        
        ExCol.column_def["priAOAStallMarSmth"]["equation"] = eq_strip("'Flaps 0'  " + eq_1 + "\n'Flaps 20'  " + eq_2 + "\n'Flaps 40'  " + eq_3)
        fdf.loc[fdf['priFlapsPos'] ==  0, 'priAOAStallMarSmth'] = eval(eq_1)
        fdf.loc[fdf['priFlapsPos'] == 20, 'priAOAStallMarSmth'] = eval(eq_2)
        fdf.loc[fdf['priFlapsPos'] == 40, 'priAOAStallMarSmth'] = eval(eq_3)
        available_cols.append("priAOAStallMarSmth")
        
    # CockpitAOASmthMar
    # '=IF(priFlapsPos=0,20.09-CockpitAngleofAttackSmth,IF(priFlapsPos=20,20.04-CockpitAngleofAttackSmth,IF(priFlapsPos=40,20.1-CockpitAngleofAttackSmth)))
    if ("priFlapsPos" in available_cols) and ("CockpitAngleofAttackSmth" in available_cols):
        eq_1 = "20.09 - fdf['CockpitAngleofAttackSmth']"
        eq_2 = "20.04 - fdf['CockpitAngleofAttackSmth']"
        eq_3 = "20.10 - fdf['CockpitAngleofAttackSmth']"
        
        ExCol.column_def["CockpitAOASmthMar"]["equation"] = eq_strip("'Flaps 0'  " + eq_1 + "\n'Flaps 20'  " + eq_2 + "\n'Flaps 40'  " + eq_3)
        fdf.loc[fdf['priFlapsPos'] ==  0, 'CockpitAOASmthMar'] = eval(eq_1)
        fdf.loc[fdf['priFlapsPos'] == 20, 'CockpitAOASmthMar'] = eval(eq_2)
        fdf.loc[fdf['priFlapsPos'] == 40, 'CockpitAOASmthMar'] = eval(eq_3)
        available_cols.append("CockpitAOASmthMar")

    # priAbsAlphaSmthMar
    # '=IF(priFlapsPos=0,22.96-priAbsAlphaSmth,IF(priFlapsPos=20,20.06-priAbsAlphaSmth,IF(priFlapsPos=40,22.02-priAbsAlphaSmth)))
    if ("priFlapsPos" in available_cols) and ("priAbsAlphaSmth" in available_cols):
        eq_1 = "22.96-fdf['priAbsAlphaSmth']"
        eq_2 = "20.06-fdf['priAbsAlphaSmth']"
        eq_3 = "22.02-fdf['priAbsAlphaSmth']"
        
        ExCol.column_def["priAbsAlphaSmthMar"]["equation"] = eq_strip("'Flaps 0'  " + eq_1 + "\n'Flaps 20'  " + eq_2 + "\n'Flaps 40'  " + eq_3)
        fdf.loc[fdf['priFlapsPos'] ==  0, 'priAbsAlphaSmthMar'] = eval(eq_1)
        fdf.loc[fdf['priFlapsPos'] == 20, 'priAbsAlphaSmthMar'] = eval(eq_2)
        fdf.loc[fdf['priFlapsPos'] == 40, 'priAbsAlphaSmthMar'] = eval(eq_3)
        available_cols.append("priAbsAlphaSmthMar")

    # secKIASStall

    # secKIASStallMar

    # secAOAMarSmth


   
    # Print warnings so we can see them happen and fix them
    # numpy.seterr(all='warn')


    return fdf