from collections import OrderedDict

# Column definition, ordered list of dictionary items
column_def = OrderedDict()

# -----------------------------------------------------------------------------
# Column formats
# -----------------------------------------------------------------------------

def make_column_def_dict(df_name, output=True, hidden=False, comment="", col_color="FFFFFF", col_text="", border=False, sec_title=""):
    # Make column header cell
    if col_text == "" :
        col_text = df_name

   # Make comment
    comment = comment
        
    return dict( df_name     = df_name, 
                 col_output  = output,
                 col_hide    = hidden,
                 col_text    = col_text,
                 col_color   = col_color,   # #RRGGBB
                 comment     = comment,
                 border      = border,
                 sec_title   = sec_title,
                 equation    = ""
                 )

# -----------------------------------------------------------------------------

color_primary    = "#FFFF00"     # yellow
color_boom       = "#FFC000"     # brown
color_ins        = "#92D050"     # green
color_secondary  = "#00B0F0"     # blue
color_efis       = "#B9B9B9"     # gray
color_smoothed_p = "#EFEFD8"     # gray / yellow
color_smoothed_s = "#E0E0FF"     # gray / blue
color_area_1     = "#EFEFEF"     # gray
color_area_2     = "#DFDFDF"     # gray
color_area_3     = "#EFEFEF"     # gray
color_area_3p    = "#EFEFD8"     # gray / yellow
color_area_3s    = "#E0E0FF"     # gray / blue
color_area_4     = "#DFDFDF"     # gray
color_area_5     = "#EFEFEF"     # gray
color_area_6     = "#DFDFDF"     # gray
color_area_7     = "#EFEFEF"     # gray
color_area_8     = "#DFDFDF"     # gray
color_area_9     = "#EFEFEF"     # gray
color_area_10    = "#DFDFDF"     # gray
color_area_11    = "#EFEFEF"     # gray
color_area_12    = "#DFDFDF"     # gray
color_area_13    = "#EFEFEF"     # gray
color_change     = "#FF8080"     # light red

bHide = True

# Column labels based on Master Workbook 6
" A"; column_def["msecSinceMidnite"] = make_column_def_dict("msecSinceMidnite",                                border=True,
        col_text="Milliseconds Since Midnight (ms)",
        comment="")
" B"; column_def["priTimeStamp"]  =make_column_def_dict("priTimeStamp",         col_color=color_primary,   
        col_text="Primary Time Stamp (ms)",
        comment="Time Stamp",
        sec_title="Primary System (V3 Hardware Configuration)")
" C"; column_def["priPFwd"]  = make_column_def_dict("priPFwd",              col_color=color_primary,
        col_text="Primary PFWD (counts)",
        comment="Dynon PFwd Pressure.  Differential pressure sensor type MS4525D0 (<1% error).  Shares pitot pressure with primary aircraft system.")
" D"; column_def["priPFwdSmoothed"]  = make_column_def_dict("priPFwdSmoothed",      col_color=color_primary,  hidden=True,
        col_text="Primary PFWD Smoothed (counts) DON'T USE",
        comment="Dynon PFwd Pressure. Smoothing algorithm applied (despiked with median filter, then running average).")
" E"; column_def["priP45"]  = make_column_def_dict("priP45",               col_color=color_primary,                 
        col_text="Primary P45 (counts)",
        comment="Dynon P45 Pressure.  Differential pressure sensor type MS4525D0 (<1% error).")
" F"; column_def["priP45Smoothed"]  = make_column_def_dict("priP45Smoothed",       col_color=color_primary,  hidden=True,                 
        col_text="Primary P45 Smoothed (counts) DON'T USE",
        comment="Dynon P45 Pressure. Smoothing algorithm applied (despiked with median filter, then running average).")
" G"; column_def["priPStatic"]  = make_column_def_dict("priPStatic",           col_color=color_primary,                 
        col_text="Primary Static Pressure (mb)",
        comment="Static Pressure.  Sensor:  Honeywell SSCSRNN1.6BA7A3 (.25% Accuracy).  Attached to aircraft primary static system.")
" H"; column_def["priPAlt"]  = make_column_def_dict("priPAlt",              col_color=color_primary,                 
        col_text="Primary Pressure Altitude (ft)",
        comment="Pressure Altitude")
" I"; column_def["priIAS"]  = make_column_def_dict("priIAS",               col_color=color_primary,                 
        col_text="Primary KIAS",
        comment="Indicated Airspeed.  Computed from PFwd, correction factor applied to match EFIS IAS. Displayed on optional visual display.")
" J"; column_def["priAngleOfAttack"]  = make_column_def_dict("priAngleOfAttack",     col_color=color_primary,                 
        col_text="Primary AOA (deg FRL)",
        comment="Computed angle of attack:  relative wind to fuselage reference line.  Multiple curves programmed to accommodate flap positions.  Displayed on optional visual display.")
" K"; column_def["priFlapsPos"]  = make_column_def_dict("priFlapsPos",          col_color=color_primary,                 
        col_text="Primary Flap Position (deg)",
        comment="Flap Position.  Information provided via linear potentiometer connected to flap actuator.")
" L"; column_def["priDataMark"]  = make_column_def_dict("priDataMark",          col_color=color_primary,                 
        col_text="Primary Data Mark",
        comment="Pilot initiated data mark.  Data marks record in assending order from each system re-boot.")
" M"; column_def["priOAT"]  = make_column_def_dict("priOAT",               col_color=color_primary,                 
        col_text="Primary OAT (C)",
        comment="Outside Air Temperature.  HiLetgo DS18B20 Type")
" N"; column_def["priTAS"]  = make_column_def_dict("priTAS",               col_color=color_primary,                 
        col_text="Primary KTAS",
        comment="Knots True Airspeed")
" O"; column_def["priIMUTemp"]  = make_column_def_dict("priIMUTemp",           col_color=color_primary,                 
        col_text="Primary IMU Temp (C)",
        comment="IMU Temperature.")
" P"; column_def["priVerticalG"]  = make_column_def_dict("priVerticalG",         col_color=color_primary,                 
        col_text="Primary IMU Vertical G",
        comment="IMU Vertical G.  Displayed on optional visual display.")
" Q"; column_def["priLateralG"]  = make_column_def_dict("priLateralG",          col_color=color_primary,                 
        col_text="Primary IMU Lateral G",
        comment="IMU Lateral G")
" R"; column_def["priForwardG"]  = make_column_def_dict("priForwardG",          col_color=color_primary,                 
        col_text="Primary IMU Forward G",
        comment="IMU Forward G")
" S"; column_def["priRollRate"]  = make_column_def_dict("priRollRate",          col_color=color_primary,                 
        col_text="Primary IMU Roll Rate (deg/sec)",
        comment="IMU Roll Rate.  Negative value = left")
" T"; column_def["priPitchRate"]  = make_column_def_dict("priPitchRate",         col_color=color_primary,                 
        col_text="Primary IMU Pitch Rate (deg/sec)",
        comment="IMU Pitch Rate.  Negative value = nose down")
" U"; column_def["priYawRate"]  = make_column_def_dict("priYawRate",           col_color=color_primary,                 
        col_text="Primary IMU Yaw Rate (deg/sec)",
        comment="IMU Yaw Rate.  Negative value = left")
" V"; column_def["priPitch"]  = make_column_def_dict("priPitch",             col_color=color_primary,                 
        col_text="Primary IMU Pitch (deg)",
        comment="IMU Pitch ")
" W"; column_def["priRoll"]  = make_column_def_dict("priRoll",              col_color=color_primary,                 
        col_text="Primary IMU Roll (deg)",
        comment="IMU Roll ")
" X"; column_def["priEarthVerticalG"]  = make_column_def_dict("priEarthVerticalG",    col_color=color_primary,                 
        col_text="Primary Earth Vertical G",
        comment="")
" Y"; column_def["priFlightPath"]  = make_column_def_dict("priFlightPath",        col_color=color_primary,                 
        col_text="Primary Derived Flight Path Angle (deg)",
        comment="")
" Z"; column_def["priVSI"]  = make_column_def_dict("priVSI",               col_color=color_primary,                 
        col_text="Primary Kalman Filtered IVVI (FPM)",
        comment="")
"AA"; column_def["priAltitude"]  = make_column_def_dict("priAltitude",          col_color=color_primary,    border=True,
        col_text="Primary Kalman Filtered Altitude (ft)",
        comment="")
                                                                                        
# Boom                                                                                 
"AB"; column_def["boomStaticRaw"]  = make_column_def_dict("boomStaticRaw",        col_color=color_boom,                    
        col_text="Boom Static Pressure (counts)",
        comment="Air Data Boom Static Pressure.  Recorded value software selectable.  Default:  Raw data.  To convert raw data to bar, .00012207*counts-1638.  Factory-provided curve.  Accuracy +/- .25%.",
        sec_title="Air Boom Data")
"AC"; column_def["boomDynamicRaw"]  = make_column_def_dict("boomDynamicRaw",       col_color=color_boom,                    
        col_text="Boom Dynamic Pressure (counts)",
        comment="Air Data Boom Dynamic Pressure.  Recorded value software selectable.  Default:  Raw data.  To convert raw data to bar,(.01525902*(counts-1638)-100.  Factory-provided curve.  Accuracy +/- .25%.")
"AD"; column_def["boomAlphaRaw"]  = make_column_def_dict("boomAlphaRaw",         col_color=color_boom,                    
        col_text="Boom Alpha (counts)",
        comment="Air Data Boom Alpha.  Recorded value software selectable.  Default:  Raw data. See Air Data Boom Vane Calibration Tab.  4th order poly fit required for accuracy.  2% pot accuracy.  ")
"AE"; column_def["boomBetaRaw"]  = make_column_def_dict("boomBetaRaw",          col_color=color_boom,                    
        col_text="Boom Beta (counts)",
        comment="Air Data Boom Beta.  Recorded value software selectable.  Default:  Raw data.  See Air Data Boom Vane Calibration Tab.  4th order poly fit required for accuracy.   2% Pot accuracy.")
"AF"; column_def["boomIAS"]  = make_column_def_dict("boomIAS",              col_color=color_boom,                    
        col_text="Boom KIAS",
        comment="Boom computed IAS.  Not recorded if software is set in raw data mode.")
"AG"; column_def["boomAge"]  = make_column_def_dict("boomAge",              col_color=color_boom,       border=True,
        col_text="Boom Age (ms)",
        comment="Boom data age")
                                                                                       
# GNSS/INS                                                                             
"AH"; column_def["vnAngularRateRoll"]  = make_column_def_dict("vnAngularRateRoll",   col_color=color_ins,                      
        col_text="GNSS/INS Roll Rate (rad/sec)",
        comment="Angular Roll Rate",
        sec_title="VN-300 GNSS/INS")
"AI"; column_def["vnAngularRatePitch"]  = make_column_def_dict("vnAngularRatePitch",  col_color=color_ins,                      
        col_text="GNSS/INS Pitch Rate (rad/sec)",
        comment="Angular Pitch Rate")
"AJ"; column_def["vnAngularRateYaw"]  = make_column_def_dict("vnAngularRateYaw",    col_color=color_ins,                      
        col_text="GNSS/INS Yaw Rate (rad/sec)",
        comment="Angular Yaw Rate")
"AK"; column_def["vnVelNedNorth"]  = make_column_def_dict("vnVelNedNorth",       col_color=color_ins,                      
        col_text="GNSS/INS Velocity North (m/sec)",
        comment="Velocity (NED) North")
"AL"; column_def["vnVelNedEast"]  = make_column_def_dict("vnVelNedEast",        col_color=color_ins,                      
        col_text="GNSS/INS Velocity East (m/sec)",
        comment="Velocity (NED) East")
"AM"; column_def["vnVelNedDown"]  = make_column_def_dict("vnVelNedDown",        col_color=color_ins,                      
        col_text="GNSS/INS Velocity Down (m/sec)",
        comment="Velocity (NED) Down")
"AN"; column_def["vnAccelFwd"]  = make_column_def_dict("vnAccelFwd",          col_color=color_ins,                      
        col_text="GNSS/INS Forward Accel (m/sec2)",
        comment="Acceleration Forward")
"AO"; column_def["vnAccelLat"]  = make_column_def_dict("vnAccelLat",          col_color=color_ins,                      
        col_text="GNSS/INS Lateral Accel (m/sec2)",
        comment="Acceleration Lateral")
"AP"; column_def["vnAccelVert"]  = make_column_def_dict("vnAccelVert",         col_color=color_ins,                      
        col_text="GNSS/INS Vertical Accel (m/sec2)",
        comment="Acceleration Vertical")
"AQ"; column_def["vnYaw"]  = make_column_def_dict("vnYaw",               col_color=color_ins,                      
        col_text="GNSS/INS Yaw (deg)",
        comment="GPS-derived Inertially Stabilized True Heading")
"AR"; column_def["vnPitch"]  = make_column_def_dict("vnPitch",             col_color=color_ins,                      
        col_text="GNSS/INS Pitch (deg)",
        comment="Pitch.  Static accuracy +/- 0.5 deg, dynamic accuracy +/- 0.03 deg")
"AS"; column_def["vnRoll"]  = make_column_def_dict("vnRoll",              col_color=color_ins,                      
        col_text="GNSS/INS Roll (deg)",
        comment="Roll.  Static accuracy +/- 0.5 deg, dynamic accuracy +/- 0.03 deg")
"AT"; column_def["vnLinAccFwd"]  = make_column_def_dict("vnLinAccFwd",         col_color=color_ins,                      
        col_text="GNSS/INS Linear Accel Forward (m/sec2)",
        comment="Linear Acceleration Forward")
"AU"; column_def["vnLinAccLat"]  = make_column_def_dict("vnLinAccLat",         col_color=color_ins,                      
        col_text="GNSS/INS Linear Accel Lateral (m/sec2)",
        comment="Linear Acceleration Lateral")
"AV"; column_def["vnLinAccVert"]  = make_column_def_dict("vnLinAccVert",        col_color=color_ins,                      
        col_text="GNSS/INS Linear Accel Vertical (m/sec2)",
        comment="Linear Acceleration Vertical")
"AW"; column_def["vnYawSigma"]  = make_column_def_dict("vnYawSigma",          col_color=color_ins,                      
        col_text="GNSS/INS Yaw Sigma (deg)",
        comment="Estimated yaw accuracy (1 Sigma) reported in deg [only accurate with GPS signal present]")
"AX"; column_def["vnRollSigma"]  = make_column_def_dict("vnRollSigma",         col_color=color_ins,                      
        col_text="GNSS/INS Roll Sigma (deg)",
        comment="Estimated roll accuracy (1 Sigma) reported in deg [only accurate with GPS signal present]")
"AY"; column_def["vnPitchSigma"]  = make_column_def_dict("vnPitchSigma",        col_color=color_ins,                      
        col_text="GNSS/INS Pitch Sigma (deg)",
        comment="Estimated pitch accuracy (1 Sigma) reported in deg [only accurate with GPS signal present]")
"AZ"; column_def["vnGnssVelNedNorth"]  = make_column_def_dict("vnGnssVelNedNorth",   col_color=color_ins,                      
        col_text="GNSS/INS Velocity North (m/sec)",
        comment="GNSS Velocity (NED) North.  5Hz Refresh Rate.")
"BA"; column_def["vnGnssVelNedEast"]  = make_column_def_dict("vnGnssVelNedEast",    col_color=color_ins,                      
        col_text="GNSS/INS Velocity East (m/sec)",
        comment="GNSS Velocity (NED) East.  5 Hz Refresh Rate.")
"BB"; column_def["vnGnssVelNedDown"]  = make_column_def_dict("vnGnssVelNedDown",    col_color=color_ins,                      
        col_text="GNSS/INS Velocity Down (m/sec)",
        comment="GNSS Velocity (NED) Down.  5 Hz Refresh Rate.")
"BC"; column_def["vnGnssLat"]  = make_column_def_dict("vnGnssLat",           col_color=color_ins,                      
        col_text="GNSS/INS Latitude (+ North - South)",
        comment="Latitude")
"BD"; column_def["vnGnssLon"]  = make_column_def_dict("vnGnssLon",           col_color=color_ins,                      
        col_text="GNSS/INS Longitude (+ East - West)",
        comment="Longitude")
"BE"; column_def["vnGPSFix"]  = make_column_def_dict("vnGPSFix",            col_color=color_ins,                      
        col_text="GNSS/INS GPS Quality",
        comment="Quality of GPS Solution:  0 = No fix; 1 = Time Only; 2 = 2D Solution; 3 = 3D Solution")
"BF"; column_def["vnDataAge"]  = make_column_def_dict("vnDataAge",           col_color=color_ins,                      
        col_text="GNSS/INS Data Age (ms)",
        comment="VN-300 data age")
"BG"; column_def["vnTimeUTC_1"]  = make_column_def_dict("vnTimeUTC",           col_color=color_ins,         border=True,
        col_text="GNSS/INS Zulu Time",
        comment="Time UTC.  HH:MM:SS:Cycles.  5Hz signal.  Cycles added by V2 computer during data logging (50Hz).  During analysis, use custom formatting for this column 'hh:mm:ss.00'")

# Secondary ("Docs")
"BH"; column_def["secTimeStamp"]  = make_column_def_dict("secTimeStamp",        col_color=color_secondary,                
        col_text="Secondary Time Stamp (ms)",
        comment="Secondary DAS ('Doc's Box') Time Stamp",
        sec_title="Secondary System (Separate probe, partial harness, located next to primary sensor on lower left wing)")
"BI"; column_def["secPFwd"]  = make_column_def_dict("secPFwd",             col_color=color_secondary,                
        col_text="Secondary PFWD (counts)",
        comment="Secondary Probe PFwd")
"BJ"; column_def["secPFwdSmoothed"]  = make_column_def_dict("secPFwdSmoothed",     col_color=color_secondary,   hidden=True,
        col_text="Secondary PFWD Smoothed (counts) DON'T USE",
        comment="Secondary Probe PFwd Smoothed")
"BK"; column_def["secP45"]  = make_column_def_dict("secP45",              col_color=color_secondary,                
        col_text="Secondary P45 (counts)",
        comment="Secondary Probe P45")
"BL"; column_def["secP45Smoothed"]  = make_column_def_dict("secP45Smoothed",      col_color=color_secondary,  hidden=True,
        col_text="Secondary P45 Smoothed (counts) DON'T USE",
        comment="Secondary Probe P45 Smoothed")
"BM"; column_def["secPStatic"]  = make_column_def_dict("secPStatic",          col_color=color_secondary,                
        col_text="Secondary Static Pressure (mb)",
        comment="Secondary Probe Static Pressure (Note: Secondary static port vented to interior of wing, this not an accurate static source)")
"BN"; column_def["secPAlt"]  = make_column_def_dict("secPAlt",             col_color=color_secondary,                
        col_text="Secondary Pressure Altitude (ft)",
        comment="Secondary Probe Pressure Altitude")
"BO"; column_def["secIAS"]  = make_column_def_dict("secIAS",              col_color=color_secondary,                
        col_text="Secondary KIAS",
        comment="Secondary Probe KIAS (Note: only accurate if probe has dynamic pressure source)")
"BP"; column_def["secAngleOfAttack"]  = make_column_def_dict("secAngleOfAttack",    col_color=color_secondary,                
        col_text="Secondary AOA (not accurate) See Derived Data",
        comment="Secondary Probe Angle of Attack (Deg relative to fuselage reference line--only one calibration curve supported [flap position indicator not currently wired to secondary DAS])")
"BQ"; column_def["secFlapsPos"]  = make_column_def_dict("secFlapsPos",         col_color=color_secondary,                
        col_text="Secondary Flap Position (disabled)",
        comment="Secondary Probe Flap Position (Note:  Secondary DAS currently not wired to accommodate flap position.  Default 40 always recorded in current configuration).")
"BR"; column_def["secDataMark"]  = make_column_def_dict("secDataMark",         col_color=color_secondary,                
        col_text="Secondary Data Mark (disabled)",
        comment="Data Mark (Not used in this DAS)")
"BS"; column_def["secIMUTemp"]  = make_column_def_dict("secIMUTemp",          col_color=color_secondary,                
        col_text="Secondary IMU Temp C",
        comment="IMU Temperature.")
"BT"; column_def["secVerticalG"]  = make_column_def_dict("secVerticalG",        col_color=color_secondary,                
        col_text="Secondary Vertical G",
        comment="IMU Vertical G")
"BU"; column_def["secLateralG"]  = make_column_def_dict("secLateralG",         col_color=color_secondary,                
        col_text="Secondary Lateral G",
        comment="IMU Lateral G")
"BV"; column_def["secForwardG"]  = make_column_def_dict("secForwardG",         col_color=color_secondary,                
        col_text="Secondary Forward G",
        comment="IMU Forward G")
"BW"; column_def["secRollRate"]  = make_column_def_dict("secRollRate",         col_color=color_secondary,                
        col_text="Secondary IMU Roll Rate (deg/sec)",
        comment="IMU Roll Rate.  Negative value = left")
"BX"; column_def["secPitchRate"]  = make_column_def_dict("secPitchRate",        col_color=color_secondary,                
        col_text="Secondary IMU Pitch Rate (deg/sec)",
        comment="IMU Pitch Rate.  Negative value = nose down")
"BY"; column_def["secYawRate"]  = make_column_def_dict("secYawRate",          col_color=color_secondary,                
        col_text="Secondary IMU Yaw Rate (deg/sec)",
        comment="IMU Yaw Rate.  Negative value = left")
"BZ"; column_def["secPitch"]  = make_column_def_dict("secPitch",            col_color=color_secondary,                
        col_text="Secondary IMU Pitch (deg)",
        comment="IMU Pitch ")
"CA"; column_def["secRoll"]  = make_column_def_dict("secRoll",             col_color=color_secondary,                
        col_text="Secondary IMU Roll (deg)",
        comment="IMU Roll ")
"CB"; column_def["secEarthVerticalG"]  = make_column_def_dict("secEarthVerticalG",   col_color=color_secondary,                
        col_text="Secondary Earth Vertical G",
        comment="Secondary DAS Earth Vertical G")
"CC"; column_def["secFlightPath"]  = make_column_def_dict("secFlightPath",       col_color=color_secondary,                
        col_text="Secondary Derived Flight Path Angle (deg)",
        comment="Secondary DAS Flight Path Angle")
"CD"; column_def["secVSI"]  = make_column_def_dict("secVSI",              col_color=color_secondary,                
        col_text="Secondary Kalman Filtered IVVI (FPM)",
        comment="Derivied Kalman Filtered VSI")
"CE"; column_def["secAltitude"]  = make_column_def_dict("secAltitude",         col_color=color_secondary,   border=True,
        col_text="Secondary Kalman Filtered Altitude (ft)",
        comment="Derived Kalman Filtered Altitude")

# EFIS
"CF"; column_def["efisIAS"]  = make_column_def_dict("efisIAS",             col_color=color_efis,                     
        col_text="EFIS KIAS",
        comment="",
        sec_title="EFIS")
"CG"; column_def["efisPitch"]  = make_column_def_dict("efisPitch",           col_color=color_efis,                     
        col_text="EFIS Pitch (deg)",
        comment="")
"CH"; column_def["efisRoll"]  = make_column_def_dict("efisRoll",            col_color=color_efis,                     
        col_text="EFIS Roll (deg)",
        comment="")
"CI"; column_def["efisLateralG"]  = make_column_def_dict("efisLateralG",        col_color=color_efis,                     
        col_text="EFIS Lateral G",
        comment="")
"CJ"; column_def["efisVerticalG"]  = make_column_def_dict("efisVerticalG",       col_color=color_efis,                     
        col_text="EFIS Vertical G",
        comment="EFIS Vertical G")
"CK"; column_def["efisPercentLift"]  = make_column_def_dict("efisPercentLift",     col_color=color_efis,                     
        col_text="EFIS % Lift (not accurate)",
        comment="EFIS Percent Lift (Dynon AOA manifold disconnected, not correct even when calibrated)")
"CL"; column_def["efisPAlt"]  = make_column_def_dict("efisPAlt",            col_color=color_efis,                     
        col_text="EFIS Pressure Altitude (ft)",
        comment="EFIS Pressure Altitude")
"CM"; column_def["efisVSI"]  = make_column_def_dict("efisVSI",             col_color=color_efis,                     
        col_text="EFIS VSI (FPM)",
        comment="EFIS VSI")
"CN"; column_def["efisAge"]  = make_column_def_dict("efisAge",             col_color=color_efis,                     
        col_text="EFIS Data Age (ms)",
        comment="")
"CO"; column_def["efisTime"]  = make_column_def_dict("efisTime",            col_color=color_efis,        border=True,
        col_text="EFIS Zulu Time",
        comment="EFIS Time (Z).  Recorded at 50HZ.  HH:MM:SS:Cycles (0-63 [64Hz transmition rate], occasional data point dropped to accommodate 50Hz recording rate).  During analysis, use custom formatting for this column 'hh:mm:ss.00''")

# Sliding window smoothed values
"  "; column_def["priPFwdSmthW"]  = make_column_def_dict("priPFwdSmthW",        col_color=color_smoothed_p,                 
        col_text="Primary PFwd Window Smoothed (counts)",
        comment="Dynon PFwd Pressure smoothed with centered sliding window.",
        sec_title="Sliding Window Smoothed Values")
"  "; column_def["priP45SmthW"]  = make_column_def_dict("priP45SmthW",         col_color=color_smoothed_p,
        col_text="Primary P45 Window Smoothed (counts)",
        comment="Dynon P45 Pressure smoothed with centered sliding window.")
"  "; column_def["priPStaticSmth"]  = make_column_def_dict("priPStaticSmth",      col_color=color_smoothed_p,
        col_text="Primary Static Pressure Smoothed (mb)",
        comment="Static Pressure Smoothed.")

"  "; column_def["secPFwdSmthW"]  = make_column_def_dict("secPFwdSmthW",        col_color=color_smoothed_s,
        col_text="Secondary PFwd Window Smoothed (counts)",
        comment="Secondary Probe PFwd Pressure smoothed with centered sliding window.")
"  "; column_def["secP45SmthW"]  = make_column_def_dict("secP45SmthW",         col_color=color_smoothed_s,
        col_text="Secondary P45 Window Smoothed (counts)",
        comment="Secondary Probe P45 Pressure smoothed with centered sliding window.")
"  "; column_def["secPStaticSmth"]  = make_column_def_dict("secPStaticSmth",      col_color=color_smoothed_s, border=True,
        col_text="Secondary Static Pressure Smoothed (mb)",
        comment="Secondary Probe Static Pressure Smoothed")


# Area 1 - Time, GPS Gnd Speed and Track
"CP"; column_def["vnTimeUTC_2"]  = make_column_def_dict("vnTimeUTC",           col_color=color_area_1,                   
        col_text="GNSS/INS Zulu Time",
        sec_title="Area 1:  Time, GPS Gnd Speed, Track and Winds Aloft")
"CQ"; column_def["vnGndSpeed"]  = make_column_def_dict("vnGndSpeed",          col_color=color_area_1,                   
        col_text="GNSS/INS Ground Speed (kts)")
"CR"; column_def["vnGndTrack"]  = make_column_def_dict("vnGndTrack",          col_color=color_area_1,                   
        col_text="GNSS/INS True Ground Track (deg)")
"CS"; column_def["vnWindDir"]  = make_column_def_dict("vnWindDir",           col_color=color_area_1,                   
        col_text="GNSS/INS Wind True Direction (deg)")
"CT"; column_def["vnWindSpd"]  = make_column_def_dict("vnWindSpd",           col_color=color_area_1,      border=True,
        col_text="GNSS/INS Wind Speed (kts)")

# Area 2 - Convert GNSS/INS Data from Metric to English Measurements and G
"CU"; column_def["vnVelNedNorthFPS"]  = make_column_def_dict("vnVelNedNorthFPS",    col_color=color_area_2,                   
        col_text="GNSS/INS (NED) Velocity North (ft/sec)",
        sec_title="Area 2:  Convert GNSS/INS Data from Metric to English Measurements and G")
"CV"; column_def["vnVelNedEastFPS"]  = make_column_def_dict("vnVelNedEastFPS",     col_color=color_area_2,                   
        col_text="GNSS/INS (NED) Velocity East (ft/sec)")
"CW"; column_def["vnVelNedDownFPS"]  = make_column_def_dict("vnVelNedDownFPS",     col_color=color_area_2,                   
        col_text="GNSS/INS (NED) Velocity Down (ft/sec)")
"CX"; column_def["vnFwdG"]  = make_column_def_dict("vnFwdG",              col_color=color_area_2,                   
        col_text="GNSS/INS Forward G")
"CY"; column_def["vnLatG"]  = make_column_def_dict("vnLatG",              col_color=color_area_2,                   
        col_text="GNSS/INS Lateral G")
"CZ"; column_def["vnLinAccFwdG"]  = make_column_def_dict("vnLinAccFwdG",        col_color=color_area_2,                   
        col_text="GNSS/INS Linear Acceleration Forward (G)")
"DA"; column_def["vnLinAccLatG"]  = make_column_def_dict("vnLinAccLatG",        col_color=color_area_2,                   
        col_text="GNSS/INS Linear Acceleration Lateral (G)")
"DB"; column_def["vnLinAccVertG"]  = make_column_def_dict("vnLinAccVertG",       col_color=color_area_2,      border=True,
        col_text="GNSS/INS Linear Acceleration Vertical (G)")

# Area 3 -  Pressures (PSI and mb) and Coefficient of Pressures
"DC"; column_def["priPFwdSmthPSI"]  = make_column_def_dict("priPFwdSmthPSI",      col_color=color_area_3p,                   
        col_text="Primary PFwd Smoothed (PSI)",
        comment="Calculation differs from Workbook 6",
        sec_title="Area 3.  Pressures (PSI and mb) and Coefficient of Pressures")
"DD"; column_def["priP45SmthPSI"]  = make_column_def_dict("priP45SmthPSI",       col_color=color_area_3p,
        col_text="Primary P45 Smoothed (PSI)",
        comment="Calculation differs from Workbook 6")
"DE"; column_def["secPFwdSmthPSI"]  = make_column_def_dict("secPFwdSmthPSI",      col_color=color_area_3s,
        col_text="Secondary PFwd Smoothed (PSI)",
        comment="Calculation differs from Workbook 6")
"DF"; column_def["secP45SmthPSI"]  = make_column_def_dict("secP45SmthPSI",       col_color=color_area_3s,
        col_text="Secondary P45 Smoothed (PSI)",
        comment="Calculation differs from Workbook 6")
"DG"; column_def["priPFwdSmthMB"]  = make_column_def_dict("priPFwdSmthMB",       col_color=color_area_3p,
        col_text="Primary PFwd Smoothed (mb)",
        comment="Calculation differs from Workbook 6")
"DH"; column_def["priP45SmthMB"]  = make_column_def_dict("priP45SmthMB",        col_color=color_area_3p,
        col_text="Primary P45 Smoothed (mb)",
        comment="Calculation differs from Workbook 6")
"DI"; column_def["secPFwdSmthMB"]  = make_column_def_dict("secPFwdSmthMB",       col_color=color_area_3s,
        col_text="Secondary PFwd Smoothed (mb)",
        comment="Calculation differs from Workbook 6")
"DJ"; column_def["secP45SmthMB"]  = make_column_def_dict("secP45SmthMB",        col_color=color_area_3s,
        col_text="Secondary P45 Smoothed (mb)",
        comment="Calculation differs from Workbook 6")
"DK"; column_def["priCP3Inst"]  = make_column_def_dict("priCP3Inst",          col_color=color_area_3p,                   
        col_text="Primary P45/PFwd Instantaneos")
"DL"; column_def["priCP3Smth"]  = make_column_def_dict("priCP3Smth",          col_color=color_area_3p,                   
        col_text="Primary P45/PFwd Smoothed")
"DM"; column_def["secCP3Inst"]  = make_column_def_dict("secCP3Inst",          col_color=color_area_3s,                   
        col_text="Secondary P45/PFwd Instantaneous")
"DN"; column_def["secCP3Smth"]  = make_column_def_dict("secCP3Smth",          col_color=color_area_3s,                   
        col_text="Secondary P45/PFwd Smoothed")

"DO"; column_def["priCP4Inst"]  = make_column_def_dict("priCP4Inst",          col_color=color_area_3p,                   
        col_text="Primary ATAN2 (PFwd,P45) Instantaneous")
"DP"; column_def["priCP4Smth"]  = make_column_def_dict("priCP4Smth",          col_color=color_area_3p,                   
        col_text="Primary ATAN2 (PFwd,P45) Smoothed")
"DQ"; column_def["secCP4Inst"]  = make_column_def_dict("secCP4Inst",          col_color=color_area_3s,                   
        col_text="Secondary ATAN2 (PFwd,P45) Instantaneous")
"DR"; column_def["secCP4Smth"]  = make_column_def_dict("secCP4Smth",          col_color=color_area_3s,                   
        col_text="Secondary ATAN2 (PFwd,P45) Smoothed")

"DS"; column_def["priFwd-45/q"]  = make_column_def_dict("priFwd-45/q",         col_color=color_area_3p,                   
        col_text="Primary (PFwd-P45)/q Smoothed (PSI)")
"DT"; column_def["secFwd-45/q"]  = make_column_def_dict("secFwd-45/q",         col_color=color_area_3s,      border=True,
        col_text="Secondary (PFwd-P45)/q Smoothed (PSI)")

# Area 4 - Atmospherics
"DU"; column_def["OATF"]  = make_column_def_dict("OATF",                col_color=color_area_4,                   
        col_text="OAT Deg F",
        sec_title="Area 4.  Atmospherics")
"DV"; column_def["StdTempF"]  = make_column_def_dict("StdTempF",            col_color=color_area_4,                   
        col_text="Standard Temp (deg F)")
"DW"; column_def["StdTempDeltaF"]  = make_column_def_dict("StdTempDeltaF",       col_color=color_area_4,                   
        col_text="Standard Temp Delta (deg F)")
"DX"; column_def["StdTempC"]  = make_column_def_dict("StdTempC",            col_color=color_area_4,                   
        col_text="Standard Temp (deg C)")
"DY"; column_def["StdTempDeltaC"]  = make_column_def_dict("StdTempDeltaC",       col_color=color_area_4,                   
        col_text="Standard Temp Delta (deg C)")
"DZ"; column_def["StdTempK"]  = make_column_def_dict("StdTempK",            col_color=color_area_4,                   
        col_text="Standard Temp (deg K)")
"EA"; column_def["PresRatio"]  = make_column_def_dict("PresRatio",           col_color=color_area_4,                   
        col_text="Pressure Ratio")
"EB"; column_def["DenRatio"]  = make_column_def_dict("DenRatio",            col_color=color_area_4,                   
        col_text="Density Ratio",
        comment="Calculation differs from Workbook 6")
"EC"; column_def["DenAlt"]  = make_column_def_dict("DenAlt",              col_color=color_area_4,      border=True,
        col_text="Density Altitude (ft)")

# Area 5 - Air Data Boom Uncorrected Angles, Pressures and Airspeeds
"ED"; column_def["boomStatic"]  = make_column_def_dict("boomStatic",          col_color=color_area_5,                   
        col_text="Air Data Boom Static Pressure (mb)",
        sec_title="Area 5.  Air Data Boom Uncorrected Angles, Pressures and Airspeeds")
"EE"; column_def["boomDynamic"]  = make_column_def_dict("boomDynamic",         col_color=color_area_5,                   
        col_text="Air Data Boom Dynamic Pressure (mb)")
"EF"; column_def["boomAlpha"]  = make_column_def_dict("boomAlpha",           col_color=color_area_5,                   
        col_text="Air Data Boom Uncorrected Alpha Angle (deg)")
"EG"; column_def["boomBeta"]  = make_column_def_dict("boomBeta",            col_color=color_area_5,                   
        col_text="Air Data Boom Uncorrected Beta Angle (deg)")
"EH"; column_def["boomIASCalc"]  = make_column_def_dict("boomIASCalc",         col_color=color_area_5,                   
        col_text="Air Data Boom KIAS Calculated")
"EI"; column_def["boomTAS1"]  = make_column_def_dict("boomTAS1",            col_color=color_area_5,                   
        col_text="Air Data Boom KTAS Method 1 (using Density Ratio)")
"EJ"; column_def["boomTAS2"]  = make_column_def_dict("boomTAS2",            col_color=color_area_5,                   
        col_text="Air Data Boom KTAS Method 2 (Temp and Pressure)")
"EK"; column_def["boomPAlt"]  = make_column_def_dict("boomPAlt",            col_color=color_area_5,      border=True,
        col_text="Air Data Boom Pressure Altitude (ft)")

# Area 6 - Primary System Airspeeds
"EL"; column_def["priIAS_2"]  = make_column_def_dict("priIAS",              col_color=color_area_6,                   
        col_text="Primary KIAS",
        sec_title="Area 6.  Primary System Airspeeds")
"EM"; column_def["priIASSmth"]  = make_column_def_dict("priIASSmth",          col_color=color_area_6,                   
        col_text="Primary KIAS Smoothed")
"EN"; column_def["priIASSmthRate"]  = make_column_def_dict("priIASSmthRate",      col_color=color_area_6,                   
        col_text="Primary KIAS Smoothed ROC (dKIAS/dt)")
"EO"; column_def["priCAS"]  = make_column_def_dict("priCAS",              col_color=color_area_6,                   
        col_text="Primary KCAS")
"EP"; column_def["priCASSmth"]  = make_column_def_dict("priCASSmth",          col_color=color_area_6,                   
        col_text="Primary KCAS Smoothed")
"EQ"; column_def["priCASSmthRate"]  = make_column_def_dict("priCASSmthRate",      col_color=color_area_6,                   
        col_text="Primary KCAS Smoothed ROC (dKCAS/dt)")
"ER"; column_def["priTAS_2"]  = make_column_def_dict("priTAS",              col_color=color_area_6,                   
        col_text="Primary KTAS")
"ES"; column_def["priTASSmth"]  = make_column_def_dict("priTASSmth",          col_color=color_area_6,                   
        col_text="Primary KTAS Smoothed")
"ET"; column_def["priTASSmthRate"]  = make_column_def_dict("priTASSmthRate",      col_color=color_area_6,                   
        col_text="Primary KTAS Smoothed ROC (dTAS/dt)")
"EU"; column_def["priTASMS"]  = make_column_def_dict("priTASMS",            col_color=color_area_6,                   
        col_text="Primary TAS (M/Sec)")
"EV"; column_def["priTASFPS"]  = make_column_def_dict("priTASFPS",           col_color=color_area_6,      border=True,
        col_text="Primary TAS (Ft/Sec)")

# Area 7 - Secondary System Airspeeds
"EW"; column_def["secIASCalc"]  = make_column_def_dict("secIASCalc",          col_color=color_area_7,                   
        col_text="Secondary KIAS Calculated",
        sec_title="Area 7.  Secondary System Airspeeds")
"EX"; column_def["secIASSmth"]  = make_column_def_dict("secIASSmth",          col_color=color_area_7,                   
        col_text="Secondary KIAS Smoothed")
"EY"; column_def["secIASSmthRate"]  = make_column_def_dict("secIASSmthRate",      col_color=color_area_7,                   
        col_text="Secondary KIAS Smoothed ROC (dKIAS/dt)")
"EZ"; column_def["secCAS"]  = make_column_def_dict("secCAS",              col_color=color_area_7,                   
        col_text="Secondary KCAS")
"FA"; column_def["secCASSmth"]  = make_column_def_dict("secCASSmth",          col_color=color_area_7,                   
        col_text="Secondary KCAS Smoothed")
"FB"; column_def["secCASSmthRate"]  = make_column_def_dict("secCASSmthRate",      col_color=color_area_7,      border=True,
        col_text="Secondary KCAS Smoothed ROC (dKCAS/dt)")

# Area 8 - Attitude, Performance and G
"FC"; column_def["vnPitch_2"]  = make_column_def_dict("vnPitch",             col_color=color_area_8,                   
        col_text="GNSS/INS Pitch (deg, + Up, - Down)",
        sec_title="Area 8.  Attitude, Performance and G")
"FD"; column_def["vnPitchRateDeg"]  = make_column_def_dict("vnPitchRateDeg",      col_color=color_area_8,                   
        col_text="GNSS/INS Pitch Rate (deg/sec)")
"FE"; column_def["vnPitchRateSmthDeg"]  = make_column_def_dict("vnPitchRateSmthDeg",  col_color=color_area_8,                   
        col_text="GNSS/INS Pitch Rate Smoothed (deg/sec)")
"FF"; column_def["vnRoll_2"]  = make_column_def_dict("vnRoll",              col_color=color_area_8,                   
        col_text="GNSS/INS Roll (deg, - Left, + Right)")
"FG"; column_def["vnRollRateDeg"]  = make_column_def_dict("vnRollRateDeg",       col_color=color_area_8,                   
        col_text="GNSS/INS Roll Rate (deg/sec)")
"FH"; column_def["vnRollRateSmthDeg"]  = make_column_def_dict("vnRollRateSmthDeg",   col_color=color_area_8,                   
        col_text="GNSS/INS Roll Rate Smoothed (deg/sec)")
"FI"; column_def["boomBeta_2"]  = make_column_def_dict("boomBeta",            col_color=color_area_8,                   
        col_text="Air Data Boom Yaw Angle (deg, + Left Yaw, - Right Yaw)")
"FJ"; column_def["boomBetaRateDeg"]  = make_column_def_dict("boomBetaRateDeg",     col_color=color_area_8,                   
        col_text="GNSS/INS Yaw Rate (deg/sec)")
"FK"; column_def["boomBetaRateSmthDeg"]  = make_column_def_dict("boomBetaRateSmthDeg", col_color=color_area_8,                   
        col_text="GNSS/INS Yaw Rate Smoothed (deg/sec)")
"FL"; column_def["vnFltPth"]  = make_column_def_dict("vnFltPth",            col_color=color_area_8,                   
        col_text="GNSS/INS Flight Path Angle (deg)")
"FM"; column_def["vnFltPthCor"]  = make_column_def_dict("vnFltPthCor",         col_color=color_area_8,                   
        col_text="GNSS/INS Flight Path Angle Corrected (deg)")
"FN"; column_def["vnTHdg"]  = make_column_def_dict("vnTHdg",              col_color=color_area_8,                   
        col_text="GNSS/INS True Heading (deg)")
"FO"; column_def["vnIVVI"]  = make_column_def_dict("vnIVVI",              col_color=color_area_8,                   
        col_text="GNSS/INS IVVI (FPM)")
"FP"; column_def["vnTrnRateDeg"]  = make_column_def_dict("vnTrnRateDeg",        col_color=color_area_8,                   
        col_text="GNSS/INS Turn Rate (deg/sec)")
"FQ"; column_def["vnTrnRateDegSmth"]  = make_column_def_dict("vnTrnRateDegSmth",    col_color=color_area_8,                   
        col_text="GNSS/INS Turn Rate Smoothed (deg/sec)")
"FR"; column_def["vnTrnRadFt"]  = make_column_def_dict("vnTrnRadFt",          col_color=color_area_8,                   
        col_text="GNSS/INS Turn Radius (ft)")
"FS"; column_def["priGSmth"]  = make_column_def_dict("priGSmth",            col_color=color_area_8,                   
        col_text="Primary G Smoothed")
"FT"; column_def["secGSmth"]  = make_column_def_dict("secGSmth",            col_color=color_area_8,                   
        col_text="Secondary G Smoothed")
"FU"; column_def["vnG"]  = make_column_def_dict("vnG",                 col_color=color_area_8,                   
        col_text="GNSS/INS G")
"FV"; column_def["vnGSmth"]  = make_column_def_dict("vnGSmth",             col_color=color_area_8,      border=True,
        col_text="GNSS/INS G Smoothed")

# Area 9 - Angle of Attack
"FW"; column_def["vnDerAlph"]  = make_column_def_dict("vnDerAlph",           col_color=color_area_9,                   
        col_text="GNSS/INS Derived AOA (deg)",
        sec_title="Area 9.  Angle of Attack")
"FX"; column_def["vnDrAlphSmth"]  = make_column_def_dict("vnDrAlphSmth",        col_color=color_area_9,                   
        col_text="GNSS/INS Derived AOA Smoothed (deg)")
"FY"; column_def["vnDrAlphRate"]  = make_column_def_dict("vnDrAlphRate",        col_color=color_area_9,                   
        col_text="GNSS/INS Derived AOA Rate (deg/sec)")
"FZ"; column_def["vnDrAlphRateSmth"]  = make_column_def_dict("vnDrAlphRateSmth",    col_color=color_area_9,                   
        col_text="GNSS/INS Derived AOA Rate Smoothed (deg/sec)")
"GA"; column_def["boomAlphaCor"]  = make_column_def_dict("boomAlphaCor",        col_color=color_area_9,                   
        col_text="Air Data Boom Corrected AOA (deg)")
"GB"; column_def["boomAlphCorSmth"]  = make_column_def_dict("boomAlphCorSmth",     col_color=color_area_9,                   
        col_text="Air Data Boom Corrected AOA Smoothed (deg)")
"GC"; column_def["boomAlphaRate"]  = make_column_def_dict("boomAlphaRate",       col_color=color_area_9,                   
        col_text="Air Data Boom Corrected AOA Rate (deg/sec)")
"GD"; column_def["boomAlphaRateSmth"]  = make_column_def_dict("boomAlphaRateSmth",   col_color=color_area_9,                   
        col_text="Air Data Boom Corrected AOA Rate Smoothed (deg/sec)")
"GE"; column_def["CockpitAngleofAttack"]  = make_column_def_dict("CockpitAngleofAttack",        col_color=color_area_9,           
        col_text="Cockpit Recorded AOA (deg)")
"GF"; column_def["CockpitAngleofAttackSmth"]  = make_column_def_dict("CockpitAngleofAttackSmth",    col_color=color_area_9,           
        col_text="Cockpit Recorded AOA Smoothed (deg)")
"GG"; column_def["CockpitAngleofAttackRate"]  = make_column_def_dict("CockpitAngleofAttackRate",    col_color=color_area_9,           
        col_text="Cockpit Recorded AOA Rate (deg/sec)")
"GH"; column_def["CockpitAngleofAttackRateSmth"]  = make_column_def_dict("CockpitAngleofAttackRateSmth",col_color=color_area_9,           
        col_text="Cockpit Recorded AOA Rate Smoothed (deg/sec)")
"GI"; column_def["priAlpha"]  = make_column_def_dict("priAlpha",            col_color=color_area_9,                   
        col_text="Primary AOA (deg)")
"GJ"; column_def["priAlphaSmth"]  = make_column_def_dict("priAlphaSmth",        col_color=color_area_9,                   
        col_text="Primary AOA Smoothed (deg)")
"GK"; column_def["priAlphaRate"]  = make_column_def_dict("priAlphaRate",        col_color=color_area_9,                   
        col_text="Primary AOA Rate (deg/sec)")
"GL"; column_def["priAlphaRateSmth"]  = make_column_def_dict("priAlphaRateSmth",    col_color=color_area_9,                   
        col_text="Primary AOA Rate Smoothed (deg/sec)")
"GM"; column_def["secAlphaCP3"]  = make_column_def_dict("secAlphaCP3",         col_color=color_area_9,                   
        col_text="Secondary AOA (deg)")
"GN"; column_def["secAlphaCP3Smth"]  = make_column_def_dict("secAlphaCP3Smth",     col_color=color_area_9,                   
        col_text="Secondary AOA Smoothed (deg)")
"GO"; column_def["secAlphaCP3Rate"]  = make_column_def_dict("secAlphaCP3Rate",     col_color=color_area_9,                   
        col_text="Secondary AOA Rate (deg/sec)")
"GP"; column_def["secAlphaCP3RateSmth"]  = make_column_def_dict("secAlphaCP3RateSmth", col_color=color_area_9,                   
        col_text="Secondary AOA Rate Smoothed (deg/sec)")
"GQ"; column_def["secAlphaCP4"]  = make_column_def_dict("secAlphaCP4",         col_color=color_area_9,                   
        col_text="Secondary AOA Arctan (PFWD,P45) (deg)")
"GR"; column_def["secAlphaCP4Smth"]  = make_column_def_dict("secAlphaCP4Smth",     col_color=color_area_9,                   
        col_text="Secondary AOA Arctan (PFWD,P45) Smoothed (deg)")
"GS"; column_def["secAlphaCP4Rate"]  = make_column_def_dict("secAlphaCP4Rate",     col_color=color_area_9,                   
        col_text="Secondary AOA Arctan (PFWD,P45) Rate (deg/sec)")
"GT"; column_def["secAlphaCP4RateSmth"]  = make_column_def_dict("secAlphaCP4RateSmth", col_color=color_area_9,                   
        col_text="Secondary AOA Arctan (PFWD,P45) Rate Smoothed (deg/sec)")
"GU"; column_def["priAbsAlph"]  = make_column_def_dict("priAbsAlph",          col_color=color_area_9,                   
        col_text="Primary Absolute Alpha (deg)")
"GV"; column_def["priAbsAlphaSmth"]  = make_column_def_dict("priAbsAlphaSmth",     col_color=color_area_9,     border=True,
        col_text="Primary Absolute Alpha Smoothed (deg)")

# Area 10 - Side Slip
"GW"; column_def["boomBeta_3"]  = make_column_def_dict("boomBeta",            col_color=color_area_10,                  
        col_text="Air Data Boom Uncorrected Beta Angle (deg)",
        sec_title="Area 10.  Sideslip")
"GX"; column_def["boomBetaCor"]  = make_column_def_dict("boomBetaCor",         col_color=color_area_10,                  
        col_text="Air Data Boom Corrected Yaw (deg)")
"GY"; column_def["boomBetaCorSmth"]  = make_column_def_dict("boomBetaCorSmth",     col_color=color_area_10,                  
        col_text="Air Data Boom Corrected Yaw Smoothed (deg)")
"GZ"; column_def["boomBetaRate"]  = make_column_def_dict("boomBetaRate",        col_color=color_area_10,                  
        col_text="Air Data Boom Corrected Yaw Rate (deg/sec)")
"HA"; column_def["boomBetaRateSmth"]  = make_column_def_dict("boomBetaRateSmth",    col_color=color_area_10,    border=True,
        col_text="Air Data Boom Corrected Yaw Rate Smoothed (deg/sec)")

# Area 11 - AOA Accuracy
"HB"; column_def["boomvsCockpit"]  = make_column_def_dict("boomvsCockpit",       col_color=color_area_11,                  
        col_text="Air Data Boom vs Cockpit Recorded AOA (deg)",
        sec_title="Area 11.  AOA Accuracy")
"HC"; column_def["vnvsCockpit"]  = make_column_def_dict("vnvsCockpit",         col_color=color_area_11,                  
        col_text="GNSS/INS Derived vs Cockpit Recorded AOA (deg)")
"HD"; column_def["boomvspri"]  = make_column_def_dict("boomvspri",           col_color=color_area_11,                  
        col_text="Air Data Boom vs Primary AOA (deg)")
"HE"; column_def["vnvspri"]  = make_column_def_dict("vnvspri",             col_color=color_area_11,                  
        col_text="GNSS/INS Derived vs Primary AOA (deg)")
"HF"; column_def["boomvssecCP3"]  = make_column_def_dict("boomvssecCP3",        col_color=color_area_11,                  
        col_text="Air Data Boom vs Secondary AOA P45/PFWD (deg)")
"HG"; column_def["vnvssecCP3"]  = make_column_def_dict("vnvssecCP3",          col_color=color_area_11,                  
        col_text="GNSS/INS Derived vs Secondary AOA P45/PFWD (deg)")
"HH"; column_def["boomvssecCP4"]  = make_column_def_dict("boomvssecCP4",        col_color=color_area_11,                  
        col_text="Air Data Boom vs Secondary AOA Arctan(PFWD,P45) (deg)")
"HI"; column_def["vnvssecCP4"]  = make_column_def_dict("vnvssecCP4",          col_color=color_area_11,    border=True,
        col_text="GNSS/INS Derived vs Secondary AOA Arctan(PFWD,P45) (deg)")

# Area 12 - Disagreements
"HJ"; column_def["priDisagvnRoll"]  = make_column_def_dict("priDisagvnRoll",      col_color=color_area_12,                  
        col_text="Primary vs GNSS/INS Roll Disag (deg)",
        sec_title="Area 12. Disagreements")
"HK"; column_def["priDisagvnPitch"]  = make_column_def_dict("priDisagvnPitch",     col_color=color_area_12,                  
        col_text="Primary vs GNSS/INS Pitch Disag (deg)")
"HL"; column_def["priDisagefisPAlt"]  = make_column_def_dict("priDisagefisPAlt",    col_color=color_area_12,                  
        col_text="Primary vs EFIS Pressure Altitude Disag (ft)")
"HM"; column_def["priDisagefisKIAS"]  = make_column_def_dict("priDisagefisKIAS",    col_color=color_area_12,                  
        col_text="Primary vs EFIS KIAS Disag")
"HN"; column_def["priDisagboomPAlt"]  = make_column_def_dict("priDisagboomPAlt",    col_color=color_area_12,                  
        col_text="Primary vs Air Data Boom Pressure Altitude Disag (ft)")
"HO"; column_def["priDisagboomKIAS"]  = make_column_def_dict("priDisagboomKIAS",    col_color=color_area_12,                  
        col_text="Primary vs Air Data Boom KIAS Disag")
"HP"; column_def["priDisagboomTAS"]  = make_column_def_dict("priDisagboomTAS",     col_color=color_area_12,    border=True,
        col_text="Primary KTAS vs Air Data Boom KTAS Disag")

# Area 13 - Aerodynamic Margin
"HQ"; column_def["priKIASStall"]  = make_column_def_dict("priKIASStall",        col_color=color_area_13,                  
        col_text="Primary KIAS Stall Speed",
        sec_title="Area 13.  Aerodynamic Margin")
"HR"; column_def["priKIASStallMar"]  = make_column_def_dict("priKIASStallMar",     col_color=color_area_13,                  
        col_text="Primary KIAS Stall Margin (kts)")
"HS"; column_def["priAOAStallMarSmth"]  = make_column_def_dict("priAOAStallMarSmth",  col_color=color_area_13,                  
        col_text="Primary AOA Smoothed Stall Margin (deg)")
"HT"; column_def["CockpitAOASmthMar"]  = make_column_def_dict("CockpitAOASmthMar",   col_color=color_area_13,                  
        col_text="Cockpit Recorded AOA Smoothed Stall Margin (deg)")
"HU"; column_def["priAbsAlphaSmthMar"]  = make_column_def_dict("priAbsAlphaSmthMar",  col_color=color_area_13,                  
        col_text="Primary Absolute Alpha Smoothed Stall Margin (deg)")
"HV"; column_def["secKIASStall"]  = make_column_def_dict("secKIASStall",        col_color=color_area_13,                  
        col_text="Secondary KIAS Stall Speed")
"HW"; column_def["secKIASStallMar"]  = make_column_def_dict("secKIASStallMar",     col_color=color_area_13,                  
        col_text="Secondary KIAS Stall Margin (kts)")
"HX"; column_def["secAOAMarSmth"]  = make_column_def_dict("secAOAMarSmth",       col_color=color_area_13,                  
        col_text="Secondary AOA Smoothed Stall Margin (deg)")


# Columns not used
  # column_def[""]  = make_column_def_dict("PRatio",                                                     col_text="")
# column_def[""]  = make_column_def_dict("boomAlphaDer",                                               col_text="Boom AOA Derived")
# column_def[""]  = make_column_def_dict("v2CP3Inst",                                                  col_text="")
# column_def[""]  = make_column_def_dict("v2CP3Smth",                                                  col_text="")
# column_def[""]  = make_column_def_dict("v2AlphPitchCur",                                             col_text="")
# column_def[""]  = make_column_def_dict("v2AlphDyna",                                                 col_text="")
# column_def[""]  = make_column_def_dict("v2AlphInstPitchCur",                                         col_text="")
# column_def[""]  = make_column_def_dict("v2AlphSmthIMUCur",                                           col_text="")
# column_def[""]  = make_column_def_dict("v3CP3Inst",                                                  col_text="")
# column_def[""]  = make_column_def_dict("v3CP3Smth",                                                  col_text="")
# column_def[""]  = make_column_def_dict("boomAlphDynaPitCur",                                         col_text="")
# column_def[""]  = make_column_def_dict("boomAlphDynaIMUCur",                                         col_text="")
# column_def[""]  = make_column_def_dict("boomAlphUpwaPitCur",                                         col_text="")
# column_def[""]  = make_column_def_dict("boomAlphUpwaIMUCur",                                         col_text="")
# column_def[""]  = make_column_def_dict("vnFltPth",                                                   col_text="")
# column_def[""]  = make_column_def_dict("vnIVVI",                                                     col_text="")
# column_def[""]  = make_column_def_dict("vnDerAlph",                                                  col_text="Ext IMU AOA Derived")
# column_def[""]  = make_column_def_dict("vnRollRateDeg",                                              col_text="")
# column_def[""]  = make_column_def_dict("vnRollRateSmthDeg",                                          col_text="")
# column_def[""]  = make_column_def_dict("vnPitchRateDeg",                                             col_text="")
# column_def[""]  = make_column_def_dict("vnPitchRateSmthDeg",                                         col_text="")
# column_def[""]  = make_column_def_dict("vnTHdg",                                                     col_text="")
# column_def[""]  = make_column_def_dict("vnG",                                                        col_text="")
# column_def[""]  = make_column_def_dict("vnGSmth",                                                    col_text="")
# column_def[""]  = make_column_def_dict("vnBankAng",                                                  col_text="")
# column_def[""]  = make_column_def_dict("TrnRateDeg",                                                 col_text="")
# column_def[""]  = make_column_def_dict("TrnRadFt",                                                   col_text="")
# column_def[""]  = make_column_def_dict("efisRollDisag",                                              col_text="")
# column_def[""]  = make_column_def_dict("efisPitchDisag",                                             col_text="")
# column_def[""]  = make_column_def_dict("efisPaltDisag",                                              col_text="")
# column_def[""]  = make_column_def_dict("v2IAS",                                                      col_text="")
# column_def[""]  = make_column_def_dict("v2IASVs",                                                    col_text="")
# column_def[""]  = make_column_def_dict("StallMarv2IAS",                                              col_text="")
# column_def[""]  = make_column_def_dict("v2CAS",                                                      col_text="")
# column_def[""]  = make_column_def_dict("v2CASVs",                                                    col_text="")
# column_def[""]  = make_column_def_dict("v2StallMarCAS",                                              col_text="")
# column_def[""]  = make_column_def_dict("EFISIAS",                                                    col_text="")
# column_def[""]  = make_column_def_dict("EFISIASVs",                                                  col_text="")
# column_def[""]  = make_column_def_dict("efisStallMarIAS",                                            col_text="")
# column_def[""]  = make_column_def_dict("efisCAS",                                                    col_text="")
# column_def[""]  = make_column_def_dict("efisCASVs",                                                  col_text="")
# column_def[""]  = make_column_def_dict("efisStallMarCAS",                                            col_text="")
# column_def[""]  = make_column_def_dict("AlphMar",                                                    col_text="")
# column_def[""]  = make_column_def_dict("AbsAlph",                                                    col_text="")
# column_def[""]  = make_column_def_dict("AbsAlphMar",                                                 col_text="")
# column_def[""]  = make_column_def_dict("efisCASVsG",                                                 col_text="")
# column_def[""]  = make_column_def_dict("efisStallMarCASG",                                           col_text="")

