# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 14:19:13 2021

@author: HP
"""

import sys

import csv
import datetime
import pandas as pd

import Utils

# -----------------------------------------------------------------------------
# Reader class for V2 data files
# -----------------------------------------------------------------------------

class V2_File():
    """Read V2 data files, making corrections and adjustments along the way"""
    
    # Used to remap CSV data file labels into something more friendly for analysis
    label_remap = \
        {
        'Pitch_1':          'Pitch',
        'Roll_1':           'Roll',
        'AngularRateRoll':  'vnAngularRateRoll',
        'AngularRatePitch': 'vnAngularRatePitch',
        'AngularRateYaw':   'vnAngularRateYaw',
        'VelNedNorth':      'vnVelNedNorth',
        'VelNedEast':       'vnVelNedEast',
        'VelNedDown':       'vnVelNedDown',
        'AccelFwd':         'vnAccelFwd',
        'AccelLat':         'vnAccelLat',
        'AccelVert':        'vnAccelVert',
        'Yaw':              'vnYaw',
        'Pitch_2':          'vnPitch',
        'Roll_2':           'vnRoll',
        'LinAccFwd':        'vnLinAccFwd',
        'LinAccLat':        'vnLinAccLat',
        'LinAccVert':       'vnLinAccVert',
        'YawSigma':         'vnYawSigma',
        'RollSigma':        'vnRollSigma',
        'PitchSigma':       'vnPitchSigma',
        'GnssVelNedNorth':  'vnGnssVelNedNorth',
        'GnssVelNedEast':   'vnGnssVelNedEast',
        'GnssVelNedDown':   'vnGnssVelNedDown',
        'GPSFix':           'vnGPSFix',
        'TimeUTC':          'vnTimeUTC',
        ' TimeUTC':         'vnTimeUTC'
         }

    def __init__(self, filename):
        self.linenum = 0
        self.fh = open(filename, 'rt', newline='')

    def __iter__(self):
        for csv_line in self.fh:
            self.linenum += 1
            csv_line = csv_line.rstrip()
            if self.linenum == 1:
                # csv_line = self.fh.__next__()
                csv_line = self.fix_labels(csv_line)
                pass
            yield csv_line
            
    def fix_labels(self, csv_line):
        """Pound the csv label line into something usable"""
        
        # First split it into components
        labels = csv_line.split(",")
        
        # Original set of labels
        pitch_num = 1
        roll_num  = 1
        for label_idx in range(0, len(labels)):
            try:
                # "Pitch" and "Roll" can appear twice so it needs to be handled specially
                if labels[label_idx] == "Pitch":
                    labels[label_idx] = "Pitch_{}".format(pitch_num)
                    pitch_num += 1
                if labels[label_idx] == "Roll":
                    labels[label_idx] = "Roll_{}".format(roll_num)
                    roll_num += 1

                # Remap labels
                labels[label_idx] = labels[label_idx].strip()
                labels[label_idx] = self.label_remap[labels[label_idx]]

            # Catch any remapping errors
            except KeyError as e:
#                print("V2 label remap error - {} - {}".format(label_idx, labels[label_idx]))
                pass

        # Now put it back together into a CSV string
        csv_line = ",".join(labels)

        return csv_line
    


# ---------------------------------------------------------------------------
# V2 Data Routines
# ---------------------------------------------------------------------------

def make_dataframe(v2_filename):

    # Read the CSV file
    # -----------------

    v2_data_array = []

    v2_file = V2_File(v2_filename)
    v2_reader = csv.DictReader(v2_file)
    v2_reader.__next__()

    try:
        for v2_row in v2_reader:
                
            # Convert strings to numbers
            if convert_v2_row(v2_row) == False:
                print("Format error in {}, line {}".format(v2_filename, v2_reader.line_num))
                continue
                
            # Try getting rid of the cycle timer part
            try:
                (time_trimmed, cycle_counter) = v2_row["vnTimeUTC"].split(".")
                v2_row["vnTimeUTC"] = time_trimmed
            except:
                continue

            # Dont' store if GPS fix isn't good yet because time will be messed up
            if v2_row["vnGPSFix"] == "0":
                continue

            # We got to here so store the data                
            v2_data_array.append(v2_row)

    # Catch any other read errors
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(v2_filename, v2_reader.line_num, e))

    # Make a time index value for each row
    # ------------------------------------

    # Check the goodness of the timeStamp
    #num_rows = len(v2_data_array)
    #timestamp_span = int(v2_data_array[len(v2_data_array)-1]["timeStamp"]) - \
    #                 int(v2_data_array[0]                   ["timeStamp"])
    #if num_rows != (timestamp_span / 20) + 1:
    #    print("Warning - non-continuous timestamps")
    
    # Time in the middle of the file is probably good so make a reference from that
    middle_index_ref     = int(len(v2_data_array) / 2)
    mid_time_string_ref  =     v2_data_array[middle_index_ref]["vnTimeUTC"]
    (utc_hours_ref, utc_minutes_ref, utc_seconds_ref) = mid_time_string_ref.split(":")
    
    # Look for a line where the integer seconds increments.
    for middle_index in range(middle_index_ref+1, middle_index_ref+100):
        mid_time_string  = v2_data_array[middle_index]["vnTimeUTC"]
        (utc_hours, utc_minutes, utc_seconds) = mid_time_string.split(":")
        if int(utc_seconds_ref) != int(utc_seconds):
            break
        
    mid_timestamp  = int(v2_data_array[middle_index]["timeStamp"])
    mid_time_utc   = Utils.make_utc_from_str(mid_time_string)

   # Make a UTC Time value to use as an index
    array_idx = 0
    index_time = []
    while array_idx < len(v2_data_array):
        # Make values for the data timestamp and UTC time
        data_timestamp = int(v2_data_array[array_idx]["timeStamp"])

        # Calculate and store a time index value which is milliseconds since midnight
        # Align time stamps on 20 millisecond values
        data_time_utc  = mid_time_utc + (data_timestamp - mid_timestamp)
        data_time_utc  = round(float(data_time_utc) / 20.0) * 20
        index_time.append(data_time_utc)

        array_idx += 1

    # Make a pandas dataframe of flight test data
    # -------------------------------------------
    v2_dataframe = pd.DataFrame(v2_data_array, index_time)
    v2_dups = v2_dataframe.index.duplicated()
    v2_dataframe = v2_dataframe.loc[~v2_dups,:]

    return v2_dataframe


# ---------------------------------------------------------------------------

def convert_v2_row(v2_row):

    success = True
    try:
        for v2_key in v2_row.keys():
            if   v2_key == " TimeUTC"  or \
                 v2_key == "TimeUTC"   or \
                 v2_key == "vnTimeUTC":
                pass
            elif v2_key == "timeStamp" or \
                 v2_key == "flapsPos"  or \
                 v2_key == "DataMark"  or \
                 v2_key == "boomAge"   or \
                 v2_key == "vnGPSFix"  or \
                 v2_key == "DataAge":
                v2_row[v2_key] = int(v2_row[v2_key])
            else:
                v2_row[v2_key] = float(v2_row[v2_key])

    except:
        print("Error converting ")
        success = False
            
    return success

# =============================================================================

if __name__=='__main__':
    v2__data_array = []

    print("Read V2 Data...")
    v2_filename = "Data/log_1-5.csv"
    make_dataframe(v2_filename)


#    print("Lines : {0}".format(efis_file.linenum))
    print("Done!")
    