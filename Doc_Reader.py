# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 20:44:28 2021
"""

import csv
import datetime
#import numpy as np
import pandas as pd

import Utils

# -----------------------------------------------------------------------------
# Reader class for Docs data files
# -----------------------------------------------------------------------------

class Docs_File():
    """Read Docs data files, making corrections and adjustments along the way"""
    
    # Used to remap CSV data file labels into something more friendly for analysis
    label_remap = \
        {
        'timeStamp':            'docsTimeStamp',
        'Pfwd':                 'docsPfwd',
        'PfwdSmoothed':         'docsPfwdSmoothed',
        'P45':                  'docsP45',
        'P45Smoothed':          'docsP45Smoothed',
        'PStatic':              'docsPStatic',
        'Palt':                 'docsPalt',
        'IAS':                  'docsIAS',
        'AngleofAttack':        'docsAngleofAttack',
        'flapsPos':             'docsFlapsPos'
        }

    def __init__(self, filename):
        self.linenum = 0
        self.fh = open(filename, 'rt', newline='')
    
    def __iter__(self):
        for csv_line in self.fh:
            self.linenum += 1
            csv_line = csv_line.rstrip()
            if self.linenum == 1:
                csv_line = self.fix_labels(csv_line)
            if self.linenum == 2:
                csv_line = self.fh.__next__()
            yield csv_line
            
    def fix_labels(self, csv_line):
        """Pound the csv label line into something usable"""
        
        # First split it into components
        labels = csv_line.split(",")
        
        # Original set of labels
        for label_idx in range(0, len(labels)):
            try:
                # Remap labels
#                labels[label_idx] = self.label_remap[labels[label_idx]]
                # If a label doesn't start with "efis" then it gets a "docs" stuck on the front
                labels[label_idx] = labels[label_idx].strip()
                if labels[label_idx][:4] != "efis":
                    labels[label_idx] = "docs" + labels[label_idx][0].upper() + labels[label_idx][1:]

            # Catch any remapping errors
            except KeyError as e:
                print("Docs label remap error - {} - {}".format(label_idx, labels[label_idx]))
                pass

        # Now put it back together into a CSV string
        csv_line = ",".join(labels)

        return csv_line
    

# ---------------------------------------------------------------------------
# Utility routines for reading and parsing Docs data files
# ---------------------------------------------------------------------------

def make_dataframe(doc_filename, time_correction):
    
    # Note: time correction is in seconds
    
    # Read the CSV file
    # -----------------

    doc_data_array = []

    doc_file = Docs_File(doc_filename)
    doc_reader = csv.DictReader(doc_file)

    doc_reader.__next__()
    try:
        for doc_row in doc_reader:

            # Convert strings to numbers
            if convert_doc_row(doc_row) == False:
                print("Format error in {}, line {}".format(doc_filename, doc_reader.line_num))
                continue
                        
            # Do some data fixes, OK if it throws an excepton
            try:
                # Try getting rid of the cycle timer part
                (time_trimmed, cycle_counter) = doc_row["efisTime"].split(".")
                doc_row["efisTime"] = time_trimmed

                # Take out columns we don't want for now
                del doc_row["efisTAS"]
                del doc_row["efisOAT"]
                del doc_row["efisFuelRemaining"]
                del doc_row["efisFuelFlow"]
                del doc_row["efisMAP"]
                del doc_row["efisRPM"]
                del doc_row["efisPercentPower"]
                del doc_row["efisMagHeading"]
                del doc_row["efisAge"]

            except:
                continue

            # We got to here so store the data                
            doc_data_array.append(doc_row)

    # Catch any other read errors
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(doc_filename, doc_reader.line_num, e))


    # Make a time index value for each row
    # ------------------------------------

    # Check the goodness of the timeStamp
    #num_rows = len(doc_data_array)
    #timestamp_span = int(doc_data_array[len(doc_data_array)-1]["docsTimeStamp"]) - \
    #                 int(doc_data_array[0]                    ["docsTimeStamp"])
    #if num_rows != (timestamp_span / 20) + 1:
    #    print("Warning - non-continuous timestamps")

    # Time in the middle of the file is probably good so make a reference from that
    middle_index_ref     = int(len(doc_data_array) / 2)
    mid_time_string_ref  = doc_data_array[middle_index_ref]["efisTime"]
    (utc_hours_ref, utc_minutes_ref, utc_seconds_ref) = mid_time_string_ref.split(":")
    
    # Look for a line where the integer seconds increments.
    for middle_index in range(middle_index_ref+1, middle_index_ref+100):
        mid_time_string = doc_data_array[middle_index]["efisTime"]
        (utc_hours, utc_minutes, utc_seconds) = mid_time_string.split(":")
        if int(utc_seconds_ref) != int(utc_seconds):
            break
        
    mid_timestamp  = int(doc_data_array[middle_index]["docsTimeStamp"])
    mid_time_utc   = Utils.make_utc_from_str(mid_time_string)

   # Make a UTC Time value to use as an index
    array_idx = 0
    index_time = []
    while array_idx < len(doc_data_array):
        try:
            # Check for bad data
            if doc_data_array[array_idx]["efisTime"] is None:
                raise ValueError("Bad efisTime")
            
            # Make values for the data timestamp and UTC time
            data_timestamp = int(doc_data_array[array_idx]["docsTimeStamp"])
            
            # Calculate and store a time index value which is milliseconds since midnight
            data_time_utc = mid_time_utc + (data_timestamp - mid_timestamp)
            data_time_utc += time_correction * 1000
            data_time_utc = round(float(data_time_utc) / 20.0) * 20
            index_time.append(data_time_utc)

            array_idx += 1

        except Exception as error:
            print("Error '" + repr(error) + "' at line " + str(array_idx))
            doc_data_array.pop(array_idx)
        
    # Make a pandas dataframe of flight test data
    # -------------------------------------------
    doc_dataframe = pd.DataFrame(doc_data_array, index_time)
#    doc_dataframe.columns = doc_column_names
    doc_dups = doc_dataframe.index.duplicated()
    doc_dataframe = doc_dataframe.loc[~doc_dups,:]
        
    return doc_dataframe


# ---------------------------------------------------------------------------

def convert_doc_row(doc_row):
    
    success = True
    try:
        # Convert most (but not all) values from strings to numbers
        for doc_key in doc_row.keys():
            if   doc_key == "efisTime":
                pass
            elif doc_key == "docsTimeStamp" or \
                 doc_key == "efisAge":
                doc_row[doc_key] = int(doc_row[doc_key])
            else:
                doc_row[doc_key] = float(doc_row[doc_key])

    except:
       print("Error converting '{}'".format(doc_key))
       success = False
        
    return success
    
# =============================================================================

if __name__=='__main__':
    doc__data_array = []

    print("Read Docs Data...")
    docs_filename = "Data/Docs Box 11 Aug 21.csv"
    doc_dataframe = make_dataframe(docs_filename, 0)

#    print("Lines : {0}".format(efis_file.linenum))
    print("Done!")
    