# -*- coding: utf-8 -*-
"""
Created on Wed Mar 1 2022

@author: Bob Baggerman
"""

import math
import numpy as np
import pandas as pd

import Alpha_Beta_Filter as abf


def add_derived_cols(fdf):

    # Catch harmless warnings so they won't print
    # numpy.seterr(all='warn')

    available_cols = fdf.columns.values.tolist()
    data_sample_period = 1.0 / 50.0 # 50 Hz

    # TAS - TAS Knots
    if (("IAS" in available_cols) and ("Palt" in available_cols)) and not ("TAS" in available_cols):
        # =I2*(1+(H2/1000*0.017))
        fdf["TAS"] = fdf["IAS"] * (1 + (fdf["Palt"] / 1000 * 0.017)) # MAKE SURE THIS IS RIGHT ()
        available_cols.append("TAS")

    # TASMS - TAS M/S 
    if ("IAS" in available_cols) and ("Palt" in available_cols):
        # =I2*(1+(H2/1000*0.017))*0.5144
        fdf["TASMS"] = fdf["IAS"] * (1 + (fdf["Palt"] / 1000 * 0.017)) * 0.5144 # MAKE SURE THIS IS RIGHT ()
        available_cols.append("TASMS")

    # TASFPS - TAS FPS 
    if ("TASMS" in available_cols):
        # =DO2*2.28084
        fdf["TASFPS"] = fdf["TASMS"] * 2.28084
        available_cols.append("TASFPS")

    # vnGndSpeed - Ground Speed
    # vnGndTrack - Ground Track
    if ("vnGnssVelNedNorth" in available_cols) and ("vnGnssVelNedEast" in available_cols):
        fdf["vnGndSpeed"] = ((fdf["vnGnssVelNedNorth"] ** 2) + \
                             (fdf["vnGnssVelNedEast"]  ** 2)).apply(math.sqrt) * 1.9438
        fdf["vnGndTrack"] = (np.arctan2(fdf["vnGnssVelNedEast"], fdf["vnGnssVelNedNorth"]) * 180.0 / 3.1416).mod(360)
        available_cols.append("vnGndSpeed")
        available_cols.append("vnGndTrack")

    # Pressure Ratio
    # =(1-H2/145442)^5.25586
    if "Palt" in available_cols:
        fdf["PRatio"] = (1 - (fdf["Palt"] / 145442)) ** 5.25586
        available_cols.append("PRatio")

    # boomAlphaDer - Boom alpha in degrees
    if ("boomAlphaRaw" in available_cols):
        # =0.00000000000070918*V5^4-0.000000011698*V5^3+0.000070109*V5^2-0.21624*V5+310.21
        fdf["boomAlphaDer"] = 0.00000000000070918 * np.power(fdf["boomAlphaRaw"], 4) - \
                              0.000000011698      * np.power(fdf["boomAlphaRaw"], 3) + \
                              0.000070109         * np.power(fdf["boomAlphaRaw"], 2) - \
                              0.21624             *          fdf["boomAlphaRaw"]     + \
                              310.21
        available_cols.append("boomAlphaDer")

    # boomBetaDer - Boom beta in degrees
    # if ("BoomBetaDer" in available_cols) and ("P45" in available_cols):
        # # BLANK
        # fdf["BoomBetaDer"] = 1
        # available_cols.append("BoomBetaDer")

    # v2CP3Inst - V2 CP3 Inst (P45/Pfwd)
    if ("Pfwd" in available_cols) and ("P45" in available_cols):
        # =E2/C2
        fdf["v2CP3Inst"] = fdf["P45"] / fdf["Pfwd"]  
        available_cols.append("v2CP3Inst")

    # v2CP3Smth - V2 CP3 Smooth (P45/Pfwd)
    if ("PfwdSmoothed" in available_cols) and ("P45Smoothed" in available_cols):
        # =F2/D2
        fdf["v2CP3Smth"] = fdf["P45Smoothed"] / fdf["PfwdSmoothed"]
        available_cols.append("v2CP3Smth")

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

    # v3CP3Inst - V3 CP3 Instantaneous
    if ("docsPfwd" in available_cols) and ("docsP45" in available_cols):
        # =(Q2+8192)/(S2+8192)
        fdf["v3CP3Inst"] = (fdf["docsPfwd"]+8192) / (fdf["docsP45"]+8192)
        available_cols.append("v3CP3Inst")

    # v3CP3Smth - V3 CP3 Smoothed
    if ("docsPfwdSmoothed" in available_cols) and ("docsP45Smoothed" in available_cols):
        # =(R2+8192)/(T2+8192)
        fdf["v3CP3Smth"] = (fdf["docsPfwdSmoothed"]+8192) / (fdf["docsP45Smoothed"]+8192)
        available_cols.append("v3CP3Smth")

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

    # vnFltPth - VN Flight Path Angle (deg) 
    if ("vnVelNedDown" in available_cols) and ("TASMS" in available_cols):
        # =ASIN(-AG2/DO2)*180/PI()
        # Ignore harmless warnings so they won't print
        np.seterr(all='ignore')
        fdf["vnFltPth"] =  np.arcsin(-fdf["vnVelNedDown"]/fdf["TASMS"]) * 180 / 3.1416
        np.seterr(all='print')
        available_cols.append("vnFltPth")

    # vnIVVI - VN IVVI (FPM) 
    if ("vnVelNedDown" in available_cols):
        # =-(AG2/0.00508)
        fdf["vnIVVI"] = -fdf["vnVelNedDown"] / 0.00508
        available_cols.append("vnIVVI")

    # vnDerAlph - VN Derived Alpha (deg) 
    if ("vnPitch" in available_cols) and ("vnFltPth" in available_cols):
        # =AL2-DQ2
        fdf["vnDerAlph"] = fdf["vnPitch"] - fdf["vnFltPth"]
        available_cols.append("vnDerAlph")

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

    # vnTHdg - VN True Heading (deg) 
    if ("vnYaw" in available_cols):
        # =IF(AK2>0,AK2,IF(AK2<0,360-ABS(AK2)))
        fdf.loc[fdf["vnYaw"] >= 0, "vnTHdg"] = fdf["vnYaw"]
        fdf.loc[fdf["vnYaw"] <  0, "vnTHdg"] = 360 - fdf["vnYaw"].abs()
        available_cols.append("vnTHdg")

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

    # AbsAlph - Abs Alpha 
    if ("flapsPos" in available_cols) and ("v2CP3Smth" in available_cols):
        # =IF(K2=0, 23.67*CQ2+5.423,IF(K2=20,25.039*CQ2+5.7465,IF(K2=40,25.443*CQ2+5.569)))
        fdf.loc[fdf["flapsPos"] ==  0, "AbsAlph"] = 23.670 * fdf["v2CP3Smth"] + 5.4230
        fdf.loc[fdf["flapsPos"] == 20, "AbsAlph"] = 25.039 * fdf["v2CP3Smth"] + 5.7465
        fdf.loc[fdf["flapsPos"] == 40, "AbsAlph"] = 25.443 * fdf["v2CP3Smth"] + 5.5690
        available_cols.append("AbsAlph")

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