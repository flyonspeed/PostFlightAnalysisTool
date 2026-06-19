# This Python file uses the following encoding: utf-8
import os
import sys
import io
import datetime

from pathlib import Path

import csv
import datetime
import pandas as pd

import Alpha_Beta_Filter as abf

# -----------------------------------------------------------------------------

def to_replay(dataframe, filename):

    # Offsets for Skypark
    #offset_lon = -0.003
    #offset_lat =  0.0008
    #offset_alt = 245
    #low_limit_alt = 245

    # No offsets
    #offset_lon    =  0.0
    #offset_lat    =  0.0
    #offset_alt    =    0
    #low_limit_alt =    0

    # Offsets to correct at Skypark
    offset_lon    =  0.0005
    offset_lat    =  0.00067
    offset_alt    =   -40
    low_limit_alt =    247

    # Offsets for Skypark at DeFuniak
    #offset_lon    =  0.51181
    #offset_lat    = -0.12074
    #offset_alt    = 285
    #low_limit_alt = 285

    # Init the alpha-beta filters
    #abf_pitch     = abf.AlphaBetaFilter(0.02, 0.1)
    #abf_roll      = abf.AlphaBetaFilter(0.02, 0.1)
    #abf_alt        = abf.AlphaBetaFilter(0.02, 0.01, 0.5, init_sample=low_limit_alt)
    abf_alt        = abf.AlphaBetaFilter(0.02, 0.01, 0.5, init_sample=dataframe.iloc[0]["Palt"] + offset_alt)

    abf_turn_rate = abf.AlphaBetaFilter(0.02, 0.1)
    abf_slip      = abf.AlphaBetaFilter(0.02, 0.005, 0.5)

    # Open the X-Plane FDR file
    xph = open(filename, "w")

    # Write the header
    xph.write(
        "I\n" +
        "1\n" +
        "\n" +
        "ACFT,Aircraft/Laminar Research/Cessna 172SP/Cessna_172SP.acf\n" +
        "TAIL,N12345,\n" +
        "DATE,11/04/2021,\n" +
        "TIME,18:00:00\n" +
        "PRES,29.92,\n" +
        "TEMP,65,\n" +
        "WIND,0,0,\n\n")

    start_time = None

    for index, row in dataframe.iterrows():
        if start_time == None:
            start_time = index

        # Calculate some values
        fdr_lat       = row["vnGnssLat"]  + offset_lat
        fdr_lon       = row["vnGnssLon"]  + offset_lon

        fdr_alt       = abf_alt.update(row["Palt"] + offset_alt)
        if fdr_alt < low_limit_alt:
            fdr_alt = low_limit_alt

        fdr_time      = (index - start_time) / 1000.0
        fdr_roll      = row["efisRoll"] # row["vnRoll"]
        fdr_pitch     = row["efisPitch"] # row["vnPitch"]
        fdr_turn_rate = abf_turn_rate.update(row["YawRate"] * 5.0)
        fdr_slip      = abf_slip.update(-row["vnAccelLat"]*10)
        vert_speed    = -row["vnVelNedDown"]*3.28*60

        xph.write(
            "DATA," +
            "{:.3f},".format(fdr_time) +            # time secon   Time in seconds from the beginning of the recording.
            "{:.0f},".format(20.0) +                #  temp deg C  Temperature in degrees C of the ambient air near the airplane at your current altitude.
            "{:.6f},".format(fdr_lon) +             #   lon degre  Longitude in degrees.
            "{:.6f},".format(fdr_lat) +             #   lat degre  Latitude in degrees.
            "{:.0f},".format(fdr_alt) +             # h msl    ft  Height above mean sea level (in TRUE feet) regardless of any barometric pressure settings or other errors.
            "{:.0f},".format(0.0) +                 # radio altft  Radio altimeter indication.
            "{:.0f},".format(0.0) +                 #  ailn ratio  Aileron deflection as a ratio from -1.0 (left) to +1.0 (right)
            "{:.0f},".format(0.0) +                 #  elev ratio  Elevator deflection as a ratio from -1.0 (nose down) to +1.0 (nose up)
            "{:.0f},".format(0.0) +                 #  rudd ratio  Rudder deflection as a ratio from -1.0 (left) to +1.0 (right)
            "{:.2f},".format(fdr_pitch) +           #  ptch   deg  Pitch in degrees (positive up).
            "{:.2f},".format(fdr_roll) +            #  roll   deg  Roll in degrees (positive right).
            "{:.1f},".format(row["vnYaw"]) +        #  hdng  TRUE  Heading in degrees TRUE.
            "{:.0f},".format(row["IAS"]) +          # speed  KIAS  Indicated speed in knots.
            "{:.0f},".format(vert_speed) +          #   VVI ft/mn  Indicated vertical speed in feet per minute.
            "{:.2f},".format(fdr_slip) +                 #  slip   deg  Indicated slip in degrees. +10 is ball full left.
            "{:.0f},".format(fdr_turn_rate) +       #  turn   deg  Indicated rate-of-turn in degrees per second (positive right). +25 is standard rate to the right.
            "{:.0f},".format(0.0) +                 #  mach     #  Indicated Mach number.
            "{:.0f},".format(0.0) +                 #   AOA   deg  Indicated Angle of Attack.
            "{:.0f},".format(0.0) +                 # stall  warn  Stall warning (0 to 1).
            "{:.2f},".format(row["flapsPos"]/40.0) +#  flap  rqst  Flap handle position. 0.0 is retracted and 1.0 is extended.
            "{:.2f},".format(row["flapsPos"]/40.0) +#  flap actul  Flap-1 deflection ratio. 0.0 is retracted and 1.0 is extended.
            "{:.0f},".format(0.0) +                 #  slat ratio  Slat-1 deflection ratio. 0.0 is retracted and 1.0 is extended.
            "{:.0f},".format(0.0) +                 #  sbrk ratio  Speedbrake deflection ratio. 0.0 is retracted; 1.0 is extended; 1.5 is ground-deployed.
            "{:.0f},".format(0.0) +                 #  gear handl  Gear handle. 0 is up and 1 is down.
            "{:.0f},".format(0.0) +                 # Ngear  down  Gear #1 (nose?) deployment ratio: 0.0 is retracted and 1.0 is down.
            "{:.0f},".format(0.0) +                 # Lgear  down  Gear #2 (left?) deployment ratio: 0.0 is retracted and 1.0 is down.
            "{:.0f},".format(0.0) +                 # Rgear  down  Gear #3 (right?) deployment ratio: 0.0 is retracted and 1.0 is down.
            "{:.0f},".format(0.0) +                 #  elev  trim  Elevator trim. -1.0 is nose down and 1.0 is nose up.
            "{:.0f},".format(11590) +               # NAV-1   frq  Nav-1 frequency. 5-digit integer form with no decimal like 12150.
            "{:.0f},".format(11190) +               # NAV-2   frq  Nav-2 frequency. 5-digit integer form with no decimal like 12150
            "{:.0f},".format(3.0) +                 # NAV-1  type  Nav-1 type. NONE=0; NDB=2; VOR=3; LOC=5; ILS=10.
            "{:.0f},".format(10.0) +                # NAV-2  type  Nav-2 type. NONE=0; NDB=2; VOR=3; LOC=5; ILS=10.
            "{:.0f},".format(120.0) +               # OBS-1   deg  OBS-1 in degrees 0 to 360.
            "{:.0f},".format(175.0) +               # OBS-2   deg  OBS-2 in degrees 0 to 360.
            "{:.0f},".format(0.0) +                 # DME-1    nm  0.0 means no DME found... any positive value means we are getting DME data.
            "{:.0f},".format(0.0) +                 # DME-2    nm  0.0 means no DME found... any positive value means we are getting DME data.
            "{:.0f},".format(0.0) +                 # NAV-1 h-def  Horizontal (localizer) deflection. -2.5 to 2.5 dots (positive fly right).
            "{:.0f},".format(0.0) +                 # NAV-2 h-def  Horizontal (localizer) deflection. -2.5 to 2.5 dots (positive fly right).
            "{:.0f},".format(0.0) +                 # NAV-1 n/t/f  Nav-1 NAV/TO/FROM: nav=0; to=1; from=2.
            "{:.0f},".format(0.0) +                 # NAV-2 n/t/f  Nav-1 NAV/TO/FROM: nav=0; to=1; from=2.
            "{:.0f},".format(0.0) +                 # NAV-1 v-def  Vertical (glideslope) deflection. -2.5 to 2.5 dots (positive fly up).
            "{:.0f},".format(0.0) +                 # NAV-2 v-def  Vertical (glideslope) deflection. -2.5 to 2.5 dots (positive fly up).
            "{:.0f},".format(0.0) +                 #    OM  over  Over marker (0/1)
            "{:.0f},".format(0.0) +                 #    MM  over  Over marker (0/1)
            "{:.0f},".format(0.0) +                 #    IM  over  Over marker (0/1)
            "{:.0f},".format(0.0) +                 # f-dir   0/1  Flight director on (0/1).
            "{:.0f},".format(0.0) +                 # f-dir  ptch  Flight director pitch in degrees (positive up).
            "{:.0f},".format(0.0) +                 # f-dir  roll  Flight director roll in degrees (positive right).
            "{:.0f},".format(0.0) +                 # ktmac   0/1  Autopilot is holding knots or mach number (knots=0 and mach=1)
            "{:.0f},".format(0.0) +                 # throt  mode  Auto-throttle mode: off=0 and on=1
            "{:.0f},".format(0.0) +                 #   hdg  mode  Autopilot heading mode: 0=wing-level; 1=heading; 2=localizer or other CDI
            "{:.0f},".format(0.0) +                 #   alt  mode  Autopilot altitude mode: 3=pitch sync; 4=vvi; 5=airspeed; 6=airspeed with alt arm; 7=alt hold; 8=terrain-follow; 9=glideslope hold
            "{:.0f},".format(0.0) +                 #  hnav  mode  Localizer CDI is ARMED for capture.
            "{:.0f},".format(0.0) +                 # glslp  mode  Glideslope CDI is ARMED for capture.
            "{:.0f},".format(0.0) +                 #  back  mode  ABack-course on (0/1).
            "{:.0f},".format(0.0) +                 # speed selec  Autopilot speed selection: knots or Mach number.
            "{:.0f},".format(0.0) +                 #   hdg selec  Autopilot heading selection in degrees magnetic.
            "{:.0f},".format(0.0) +                 #   vvi selec  Autopilot vertical speed selection in feet per minute
            "{:.0f},".format(0.0) +                 #   alt selec  Autopilot altitude selection in feet MSL indicated.
            "{:.2f},".format(29.92) +               #  baro in hg  Barometric pressure dialed into the altimeter in inches HG.
            "{:.0f},".format(0.0) +                 #    DH    ft  Decision height dialed into the radio alt in feet AGL.
            "{:.0f},".format(0.0) +                 # Mcaut   0/1  Master Caution alerting (0/1).
            "{:.0f},".format(0.0) +                 # Mwarn   0/1  Master Warning alerting (0/1).
            "{:.0f},".format(0.0) +                 #  GPWS   0/1  Ground Proximity Warning (0/1).
            "{:.0f},".format(0.0) +                 # Mmode   0-4  Map mode: 0 through 4 can give some different map results.
            "{:.0f},".format(0.0) +                 # Mrang   0-6  Map range: 0 through 6 will give different map ranges.
            "{:.0f},".format(0.75) +                # throt ratio  Throttle ratio 0.0 to 1.0 (but emergency settings can actually exceed 1.0).
            "{:.2f},".format(0.75) +                # throt ratio  Throttle ratio 0.0 to 1.0 (but emergency settings can actually exceed 1.0).
            "{:.2f},".format(0.75) +                # throt ratio  Throttle ratio 0.0 to 1.0 (but emergency settings can actually exceed 1.0).
            "{:.0f},".format(0.75) +                # throt ratio  Throttle ratio 0.0 to 1.0 (but emergency settings can actually exceed 1.0).
            "{:.0f},".format(75) +                  #  prop cntrl  Propeller RPM command (per engine) decimal percent
            "{:.0f},".format(0.0) +                 #  prop cntrl  Propeller RPM command (per engine)
            "{:.0f},".format(0.0) +                 #  prop cntrl  Propeller RPM command (per engine)
            "{:.0f},".format(0.0) +                 #  prop cntrl  Propeller RPM command (per engine)
            "{:.0f},".format(75) +                  #  prop   rpm  Propeller RPM actual (per engine).
            "{:.0f},".format(0.0) +                 #  prop   rpm  Propeller RPM actual (per engine).
            "{:.0f},".format(0.0) +                 #  prop   rpm  Propeller RPM actual (per engine).
            "{:.0f},".format(0.0) +                 #  prop   rpm  Propeller RPM actual (per engine).
            "{:.0f},".format(0.0) +                 #  prop   deg  Propeller pitch in degrees (per engine).
            "{:.0f},".format(0.0) +                 #  prop   deg  Propeller pitch in degrees (per engine).
            "{:.0f},".format(0.0) +                 #  prop   deg  Propeller pitch in degrees (per engine).
            "{:.0f},".format(0.0) +                 #  prop   deg  Propeller pitch in degrees (per engine).
            "{:.0f},".format(0.0) +                 #    N1     %  N1 (per engine).
            "{:.0f},".format(0.0) +                 #    N1     %  N1 (per engine).
            "{:.0f},".format(0.0) +                 #    N1     %  N1 (per engine).
            "{:.0f},".format(0.0) +                 #    N1     %  N1 (per engine).
            "{:.0f},".format(0.0) +                 #    N2     %  N2 (per engine).
            "{:.0f},".format(0.0) +                 #    N2     %  N2 (per engine).
            "{:.0f},".format(0.0) +                 #    N2     %  N2 (per engine).
            "{:.0f},".format(0.0) +                 #    N2     %  N2 (per engine).
            "{:.0f},".format(27.0) +                #   MPR  inch  Engine Manifold Pressure (per engine).
            "{:.0f},".format(0.0) +                 #   MPR  inch  Engine Manifold Pressure (per engine).
            "{:.0f},".format(0.0) +                 #   MPR  inch  Engine Manifold Pressure (per engine).
            "{:.0f},".format(0.0) +                 #   MPR  inch  Engine Manifold Pressure (per engine).
            "{:.0f},".format(0.0) +                 #   EPR   ind  Engine Pressure Ratio (per engine).
            "{:.0f},".format(0.0) +                 #   EPR   ind  Engine Pressure Ratio (per engine).
            "{:.0f},".format(0.0) +                 #   EPR   ind  Engine Pressure Ratio (per engine).
            "{:.0f},".format(0.0) +                 #   EPR   ind  Engine Pressure Ratio (per engine).
            "{:.0f},".format(0.0) +                 #  torq ft*lb  Engine torque (per engine).
            "{:.0f},".format(0.0) +                 #  torq ft*lb  Engine torque (per engine).
            "{:.0f},".format(0.0) +                 #  torq ft*lb  Engine torque (per engine).
            "{:.0f},".format(0.0) +                 #  torq ft*lb  Engine torque (per engine).
            "{:.0f},".format(50.0) +                #    FF lb/hr  Fuel Flow (per engine).
            "{:.0f},".format(0.0) +                 #    FF lb/hr  Fuel Flow (per engine).
            "{:.0f},".format(0.0) +                 #    FF lb/hr  Fuel Flow (per engine).
            "{:.0f},".format(0.0) +                 #    FF lb/hr  Fuel Flow (per engine).
            "{:.0f},".format(0.0) +                 #   ITT deg C  Turbine Inlet Temperature (per engine).
            "{:.0f},".format(0.0) +                 #   ITT deg C  Turbine Inlet Temperature (per engine).
            "{:.0f},".format(0.0) +                 #   ITT deg C  Turbine Inlet Temperature (per engine).
            "{:.0f},".format(0.0) +                 #   ITT deg C  Turbine Inlet Temperature (per engine).
            "{:.0f},".format(63.0) +                #   EGT deg C  Exhaust Gas Temperature (per engine).
            "{:.0f},".format(0.0) +                 #   EGT deg C  Exhaust Gas Temperature (per engine).
            "{:.0f},".format(0.0) +                 #   EGT deg C  Exhaust Gas Temperature (per engine).
            "{:.0f},".format(0.0) +                 #   EGT deg C  Exhaust Gas Temperature (per engine).
            "{:.0f},".format(150.0) +               #   CHT deg C  Cylinder Head Temperature (per engine).
            "{:.0f},".format(0.0) +                 #   CHT deg C  Cylinder Head Temperature (per engine).
            "{:.0f},".format(0.0) +                 #   CHT deg C  Cylinder Head Temperature (per engine).
            "{:.0f}\n".format(0.0)                  #   CHT deg C  Cylinder Head Temperature (per engine).            
            )
 
    xph.close()


# =============================================================================

if __name__=='__main__':
    v2__data_array = []

    print("Write X-Plane Data...")

    #xp_filename  = "Data/2021-11-04 Data Edited 20211109 - Bob 2 - DM1.csv"
    #fdr_filename = "Data/2021-11-04 - DM1.fdr"
    #print("  ", fdr_filename)
    #xp_dataframe = pd.read_csv(xp_filename)
    #xp_dataframe.index = xp_dataframe["msecSinceMidnite"].values
    #to_replay(xp_dataframe, fdr_filename)

    #xp_filename  = "Data/2021-11-04 Data Edited 20211109 - Bob 2 - DM46.csv"
    #fdr_filename = "Data/2021-11-04 - DM46.fdr"
    #print("  ", fdr_filename)
    #xp_dataframe = pd.read_csv(xp_filename)
    #xp_dataframe.index = xp_dataframe["msecSinceMidnite"].values
    #to_replay(xp_dataframe, fdr_filename)

    #xp_filename  = "Data/2021-11-04 Data Edited 20211109 - Bob 2 - DM48.csv"
    #fdr_filename = "Data/2021-11-04 - DM48.fdr"
    #print("  ", fdr_filename)
    #xp_dataframe = pd.read_csv(xp_filename)
    #xp_dataframe.index = xp_dataframe["msecSinceMidnite"].values
    #to_replay(xp_dataframe, fdr_filename)

    xp_filename  = "Data/11 Aug 21 - Merged 20210908T094540 - DM3.csv"
    fdr_filename = "Data/11 Aug 21 - DM3.fdr"
    print("  ", fdr_filename)
    xp_dataframe = pd.read_csv(xp_filename)
    xp_dataframe.index = xp_dataframe["msecSinceMidnite"].values
    to_replay(xp_dataframe.iloc[500:4500], fdr_filename)



    print("Done!")
