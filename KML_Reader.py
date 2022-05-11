# -*- coding: utf-8 -*-


import datetime

#import dateutil
#from dateutil.parser import parse
from dateutil.parser import isoparse
import xml.etree.ElementTree as ET
import pandas as pd

import Utils

# ---------------------------------------------------------------------------
# Utility routines for reading and parsing KML data files
# ---------------------------------------------------------------------------

def make_dataframe(kml_filename, kml_time_correction):
    
    # Note: time correction is in seconds
    
    # Read the KML file
    # -----------------

    # Open KML document using minidom parser
    kml_tree = ET.parse(kml_filename)

    # Define the namespace mapping
    ns = {'kml' : 'http://www.opengis.net/kml/2.2', 'gx' : 'http://www.google.com/kml/ext/2.2'}

    # Process the main track tree
    kml_column_names = ['kmlTimeUTC', 'kmlLatitude', 'kmlLongitude', 'kmlAltitudeMeters']

    kml_track_when  = kml_tree.findall("./kml:Document/kml:Placemark/gx:Track/kml:when", ns)
    kml_track_coord = kml_tree.findall("./kml:Document/kml:Placemark/gx:Track/gx:coord", ns)
    kml_data_length = len(kml_track_when)

    if len(kml_track_coord) != kml_data_length:
        print("Malformed KML - Coordinate data length does not match time data length")
        return None

    kml_time_array  = []
    kml_coord_array = []

    # Read the KML data
    for track_idx in range(0, len(kml_track_when)):
#        print(kml_track_when[track_idx].text, " ", kml_track_coord[track_idx].text)
        # Time
#        kml_time = isoparse(kml_track_when[track_idx].text)
        kml_time = Utils.make_utc_from_str(kml_track_when[track_idx].text)
        kml_time_array.append(kml_time)

        # Lat, Lon, Alt
        (lat, lon, alt) = kml_track_coord[track_idx].text.split(" ")
        kml_coord_array.append((kml_track_when[track_idx].text, float(lat), float(lon), float(alt)))

        kml_dataframe = pd.DataFrame(data=kml_coord_array, index=kml_time_array, columns=kml_column_names)

    # Add extended data
    kml_extended_tree = kml_tree.findall("./kml:Document/kml:ExtendedData/kml:SchemaData/gx:SimpleArrayData", ns)
    for kml_extended_element in kml_extended_tree:
        if len(kml_extended_element) == kml_data_length:
            element_data_array = []

            if kml_extended_element.attrib['name'] == "acc_horiz":
                for element_data in kml_extended_element:
                    element_data_array.append(int(element_data.text))
                kml_dataframe.insert(len(kml_dataframe.columns), "kmlAccelHorizontal", element_data_array)

            if kml_extended_element.attrib['name'] == "acc_vert":
                for element_data in kml_extended_element:
                    element_data_array.append(int(element_data.text))
                kml_dataframe.insert(len(kml_dataframe.columns), "kmlAccelVertical", element_data_array)

            if kml_extended_element.attrib['name'] == "course":
                for element_data in kml_extended_element:
                    element_data_array.append(float(element_data.text))
                kml_dataframe.insert(len(kml_dataframe.columns), "kmlCourse", element_data_array)

            if kml_extended_element.attrib['name'] == "speed_kts":
                for element_data in kml_extended_element:
                    element_data_array.append(float(element_data.text))
                kml_dataframe.insert(len(kml_dataframe.columns), "kmlSpeedKts", element_data_array)

            if kml_extended_element.attrib['name'] == "altitude":
                for element_data in kml_extended_element:
                    element_data_array.append(float(element_data.text))
                kml_dataframe.insert(len(kml_dataframe.columns), "kmlAltitudeFeet", element_data_array)

            if kml_extended_element.attrib['name'] == "bank":
                for element_data in kml_extended_element:
                    element_data_array.append(float(element_data.text))
                kml_dataframe.insert(len(kml_dataframe.columns), "kmlBank", element_data_array)

            if kml_extended_element.attrib['name'] == "pitch":
                for element_data in kml_extended_element:
                    element_data_array.append(float(element_data.text))
                kml_dataframe.insert(len(kml_dataframe.columns), "kmlPitch", element_data_array)

        else:
            print("Malformed KML - Extended data length does not match time data length")

    return kml_dataframe


# =============================================================================

if __name__=='__main__':
    kml__data_array = []

    print("Read KML Data...")
    kml_filename = "Data/TrackLog_1FADE111-3226-4B7C-9EB8-D722E324C67E.kml"
    kml_dataframe = make_dataframe(kml_filename, 0)

    print("Done!")
    