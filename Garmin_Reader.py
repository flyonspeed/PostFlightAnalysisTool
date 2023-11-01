# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 20:44:28 2021
"""

import csv
import datetime
#import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------
# Reader class for Garmin data files
# -----------------------------------------------------------------------------

class Garmin_File():
    """Read Garmin data files, making corrections and adjustments along the way"""
    
    # Used to remap CSV data file labels into something more friendly for analysis
    label_remap = \
        {
        'Latitude (deg)'            : 'grmLatitude',
        'Longitude (deg)'           : 'grmLongitude',
        'Pitch (deg)'               : 'grmPitch',
        'Roll (deg)'                : 'grmRoll',
        'Magnetic Heading (deg)'    : 'grmHeading',
        'Wind Speed (kt)'           : 'grmWindSpd',
        'Wind Direction (deg)'      : 'grmWindDir',
        'Outside Air Temp (deg C)'  : 'grmOAT',
        'True Airspeed (kt)'        : 'grmKTAS',
        'Indicated Airspeed (kt)'   : 'grmKIAS',
        'Pressure Altitude (ft)'    : 'grmPalt',
        'Baro Altitude (ft)'        : 'grmBAlt',
        'AOA'                       : 'grmAOA',
        'AOA Cp'                    : 'grmAOACp',
        'Normal Acceleration (G)'   : 'grmGsNormal',
        'Lateral Acceleration (G)'  : 'grmGsLat',
        'GPS Ground Speed (kt)'     : 'grmGpsGndSpeed',
        'GPS Ground Track (deg)'    : 'grmGpsGndTrack',
        'Vertical Speed (ft/min)'   : 'grmVertSpeed',
        'Flaps'                     : 'grmFlaps',
        'Manifold Press (inch Hg)'  : 'grmManPres',
        'RPM'                       : 'grmRPM'
        }

    def __init__(self, filename):
        self.linenum = 0
        self.fh = open(filename, 'rt', newline='')
    
    def __iter__(self):
        for csv_line in self.fh:
            self.linenum += 1
            csv_line = csv_line.rstrip()
            if self.linenum == 1:
                csv_line = self.fh.__next__()
                csv_line = self.fix_labels(csv_line)
                self.fh.__next__()
            yield csv_line
            
    def fix_labels(self, csv_line):
        """Pound the csv label line into something usable"""
        
        # First split it into components
        labels = csv_line.split(",")
        
        # Fill in any blank labels
        blank_num = 1
        for label_idx in range(0, len(labels)):
            if labels[label_idx].strip() == "":
                labels[label_idx] = "blank {0}".format(blank_num)
                blank_num += 1

        # For all original set of labels
        for label_idx in range(0, len(labels)):
            try:
                # Remap labels
                labels[label_idx] = self.label_remap[labels[label_idx]]

            # Catch any remapping errors
            except KeyError as e:
                # print("Garmin label remap error - {} - {}".format(label_idx, labels[label_idx]))
                pass

        # Now put it back together into a CSV string
        csv_line = ",".join(labels)

        return csv_line
    

# ---------------------------------------------------------------------------
# Utility routines for reading and parsing Garmin data files
# ---------------------------------------------------------------------------

def make_dataframe(garmin_filename, garmin_time_correction):
    
    # Note: time correction is in seconds
    
    # Read the CSV file
    # -----------------

    garmin_data_array = []
    garmin_file = Garmin_File(garmin_filename)
    garmin_reader = csv.DictReader(garmin_file)
    garmin_reader.__next__()
    for garmin_row in garmin_reader:

        # Convert strings to numbers and generally fix things up in a row of data
        if convert_garmin_row(garmin_row) == False:
            print("Format error in {}, line {}".format(garmin_filename, garmin_reader.line_num))
            continue

        # We got to here so store the data                
        garmin_data_array.append(garmin_row)

    # Make a time index value for each row
    # ------------------------------------

   # Get a UTC Time value to use as an index
    array_idx = 0
    index_time = []
    while array_idx < len(garmin_data_array):

        # Calculate and store a time index value which is milliseconds since midnight UTC
        data_time_utc = (garmin_data_array[array_idx]["grmZulu"] - 
                         garmin_data_array[array_idx]["grmZulu"].replace(hour=0, minute=0, second=0, microsecond=0)).seconds * 1000
        if (data_time_utc < 0) or (data_time_utc > 60*60*24*1000):
            print("Time difference error in Garmin data in {}, line {}".format(garmin_filename, array_idx))
            
        index_time.append(data_time_utc)

        array_idx += 1

    # Make a pandas dataframe of flight test data
    # -------------------------------------------
    garmin_dataframe = pd.DataFrame(garmin_data_array, index_time)

    # Resample 1 Hz Garmin data to 50 Hz
    new_index_list = range(garmin_dataframe.index[0], garmin_dataframe.index[-1]+20, 20)
    new_index = pd.Index(new_index_list)
    garmin_dataframe = garmin_dataframe.reindex(new_index)

    # Fill in missing upsampled values
    garmin_dataframe['grmLatitude'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmLongitude'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmPitch'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmRoll'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmHeading'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmWindSpd'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmWindDir'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmOAT'].ffill(inplace=True)
    garmin_dataframe['grmKTAS'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmKIAS'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmPalt'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmBAlt'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmAOA'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmAOACp'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmGsNormal'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmGsLat'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmGpsGndSpeed'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmGpsGndTrack'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmVertSpeed'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmFlaps'].ffill(inplace=True)
    garmin_dataframe['grmManPres'].interpolate(limit=50, inplace=True, limit_area='inside')
    garmin_dataframe['grmRPM'].interpolate(limit=50, inplace=True, limit_area='inside')

    # Get rid of grmZulu, Excel writer can't handle it
    garmin_dataframe.drop(['grmZulu'], axis='columns', inplace=True)

    return garmin_dataframe

# ---------------------------------------------------------------------------

def convert_garmin_row(garmin_row):
    
    success = True
    try:
        
        # Return if bad data
        if (garmin_row['GPS Fix Status'] != "3D"    ) and \
           (garmin_row['GPS Fix Status'] != "3D-"   ) and \
           (garmin_row['GPS Fix Status'] != "3DDiff"):
            return False
        
        # Make a Zulu time
        format_str   = '%Y-%m-%d %H:%M:%S %z'
        datetime_str = garmin_row['Date (yyyy-mm-dd)'] + ' ' + garmin_row['Time (hh:mm:ss)'] + ' ' + garmin_row['UTC Offset (hh:mm)'].replace(':','')
        lcl_datetime = datetime.datetime.strptime(datetime_str, format_str)
        
        garmin_row["grmZulu"] = lcl_datetime.astimezone(datetime.timezone(datetime.timedelta(0)))
            
        # There are a lot more columns that we don't want than we do want. So
        # iterate over all the columns. Convert and keep specific columns and
        # delete all the rest.

        garmin_data_keys = list(garmin_row.keys())
        for garmin_data_key in garmin_data_keys:

            if   garmin_data_key == 'grmLatitude'    or \
                 garmin_data_key == 'grmLongitude'   or \
                 garmin_data_key == 'grmKIAS'        or \
                 garmin_data_key == 'grmPitch'       or \
                 garmin_data_key == 'grmRoll'        or \
                 garmin_data_key == 'grmHeading'     or \
                 garmin_data_key == 'grmOAT'         or \
                 garmin_data_key == 'grmWindSpd'     or \
                 garmin_data_key == 'grmAOA'         or \
                 garmin_data_key == 'grmAOACp'       or \
                 garmin_data_key == 'grmGsNormal'    or \
                 garmin_data_key == 'grmGsLat'       or \
                 garmin_data_key == 'grmGpsGndSpeed' or \
                 garmin_data_key == 'grmGpsGndTrack' or \
                 garmin_data_key == 'grmVertSpeed'   or \
                 garmin_data_key == 'grmManPres'     or \
                 garmin_data_key == 'grmRPM' :
                if garmin_row[garmin_data_key] == '' :
                    garmin_row[garmin_data_key] = None
                else :
                    garmin_row[garmin_data_key] = float(garmin_row[garmin_data_key])

            # Longitude
            elif garmin_data_key == 'grmKTAS'        or \
                 garmin_data_key == 'grmPalt'        or \
                 garmin_data_key == 'grmBAlt'        or \
                 garmin_data_key == 'grmWindDir'     or \
                 garmin_data_key == 'grmFlaps' :
                if garmin_row[garmin_data_key] == '' :
                    garmin_row[garmin_data_key] = None
                else :
                    garmin_row[garmin_data_key] = int(garmin_row[garmin_data_key])

            elif garmin_data_key == "grmZulu":
                pass

            # Delete anything else
            else:
                del garmin_row[garmin_data_key]

                
    except:
        print("Error converting {0}".format(garmin_data_key))
        success = False

    return success
    


# =============================================================================

if __name__=='__main__':
    garmin__data_array = []

    print("Read Garmin Data...")
    garmin_filename = "..\Flight Test Data\RV-8 Data\RV8Data2Jun22\log_20220602_172202_KTEW.csv"
    garmin_dataframe = make_dataframe(garmin_filename, 0)

#    print("Lines : {0}".format(garmin_file.linenum))
    print("Done!")
    
    