# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 20:44:28 2021
"""

import csv
import datetime
#import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------
# Reader class for EFIS data files
# -----------------------------------------------------------------------------

class EFIS_File():
    """Read EFIS data files, making corrections and adjustments along the way"""
    
    def __init__(self, filename):
        self.linenum = 0
        self.fh = open(filename, 'rt', newline='')
    
    def __iter__(self):
        for csv_line in self.fh:
            self.linenum += 1
            csv_line = csv_line.rstrip()
            if self.linenum == 1:
                csv_line = self.fh.__next__()
                csv_line = self.fh.__next__()
                csv_line = self.fh.__next__()
                csv_line = self.fh.__next__()
                csv_line = self.fh.__next__()
                csv_line = self.fix_labels(csv_line)
            if self.linenum == 2:
                csv_line = self.fh.__next__()
            yield csv_line
            
    def fix_labels(self, csv_line):
        """Pound the csv label line into something usable"""
        
        # First split it into components
        labels = csv_line.split(",")
        
        # if len(labels) != 145:
        #     print("Error - Unknown EFIS data labels")
        #     return
        
        # Fill in any blank labels
        blank_num = 1
        # for label_idx in range(0, len(labels)):
        #     if labels[label_idx].strip() == "":
        #         labels[label_idx] = "blank {0}".format(blank_num)
        #         blank_num += 1

        # We need 145 non-blank labels
        for label_idx in range(0, 145):
            # If we ran out of labels stick a blank one on the end
            if label_idx >= len(labels):
                labels.append('')
            # Now if we encounter a blank label fill it in
            if (labels[label_idx].strip() == '') or \
               (labels[label_idx].strip() == '""'):
                labels[label_idx] = '"blank {0}"'.format(blank_num)
                blank_num += 1
    

        # Now put it back together into a CSV string
        csv_line = ",".join(labels)

        return csv_line
    

# ---------------------------------------------------------------------------
# Utility routines for reading and parsing EFIS data files
# ---------------------------------------------------------------------------

def make_dataframe(efis_filename, efis_time_correction):
    
    # Note: time correction is in seconds
    
    # Read the CSV file
    # -----------------

    efis_data_array = []
    efis_file = EFIS_File(efis_filename)
    efis_reader = csv.DictReader(efis_file)
    efis_reader.__next__()
    for efis_row in efis_reader:

        # Convert strings to numbers and generally fix things up in a row of data
        if convert_efis_row(efis_row) == False:
            print("Format error in {}, line {}".format(efis_filename, efis_reader.line_num))
            continue

        # We got to here so store the data                
        efis_data_array.append(efis_row)

    # Make a time index value for each row
    # ------------------------------------

   # Make a UTC Time value to use as an index
    array_idx = 0
    index_time = []
    while array_idx < len(efis_data_array):

        # Calculate and store a time index value which is milliseconds since midnight UTC
        data_time_utc = (efis_data_array[array_idx]["efisgpsZulu"] - 
                         efis_data_array[array_idx]["efisgpsZulu"].replace(hour=0, minute=0, second=0, microsecond=0)).seconds * 1000
        if (data_time_utc < 0) or (data_time_utc > 60*60*24*1000):
            print("Time difference error in EFIS data in {}, line {}".format(efis_filename, array_idx))
            
        index_time.append(data_time_utc)

        array_idx += 1

    # Make a pandas dataframe of flight test data
    # -------------------------------------------
    efis_dataframe = pd.DataFrame(efis_data_array, index_time)
    
    return efis_dataframe

# ---------------------------------------------------------------------------

def convert_efis_row(efis_row):
    
    success = True
    try:
        
        # Return if bad data
        if (efis_row['zulu is gps'] == 0) or (efis_row['date valid'] == 0):
            return False
        
        if efis_row['gps valid'] == 0:
            return False
        
        if (efis_row['lat'] == 0) or (efis_row['lon'] == 0):
            return False
        
        # Make a Zulu time
        efis_zulu = datetime.datetime(int(efis_row['zulu year'])+2000, int(efis_row['zulu mo']),  int(efis_row['zulu day']),
                                      int(efis_row['zulu hour']),      int(efis_row['zulu min']), int(efis_row['zulu sec']))
        
        efis_row["efisgpsZulu"] = efis_zulu
            
        # There are a lot more columns that we don't want than we do want. So
        # iterate over all the columns. Convert and keep specific columns and
        # delete all the rest.

        efis_data_keys = list(efis_row.keys())
        for efis_data_key in efis_data_keys:

            # Latitude
            if efis_data_key == "lat":
                efis_row["efisgpsLatitude"] = float(efis_row[efis_data_key])
                del efis_row[efis_data_key]

            # Longitude
            elif efis_data_key == "lon":
                efis_row["efisgpsLongitude"] = float(efis_row[efis_data_key])
                del efis_row[efis_data_key]

            # Calculated zulu time
            elif efis_data_key == "efisgpsZulu":
                pass
            
            # Extras to optionally include
            # pitch
            # roll
            # heading
            # airspeed
            # altitude

            # Delete anything else
            else:
                del efis_row[efis_data_key]
                
    except:
#        print("Error converting ")
       success = False

    return success
    


# =============================================================================

if __name__=='__main__':
    efis__data_array = []

    print("Read EFIS Data...")
    efis_filename = "Data/EFIS Data 11 Aug 21 (Edited 2).csv"
    efis_dataframe = make_dataframe(efis_filename, 0)

#    print("Lines : {0}".format(efis_file.linenum))
    print("Done!")
    