# ---------------------------------------------------------------------------
# Utility Routines
# ---------------------------------------------------------------------------

from dateutil.parser import isoparse

# ---------------------------------------------------------------------------
# Utility routines
# -----------------------------------------------------------------------------

# Convert milliseconds since midnight to a time string
def milliseconds_to_timestr(msec_since_midnight):
    msecs = msec_since_midnight

    hours = int(msecs / (1000 * 3600))
    msecs -= hours * 1000 * 3600

    mins = int(msecs / (1000 * 60))
    msecs -= mins * 1000 * 60

    secs = int(msecs / 1000)
    msecs -= secs * 1000

    return "{:02}:{:02}:{:02}".format(hours, mins, secs)


# Convert a TimeUTC format string into milliseconds since midnight
def make_utc_from_str(utc_str):

    # First try KML ISO format
    try:
        utc_time = isoparse(utc_str)
        utc_msec = (utc_time.hour * 3600 + utc_time.minute * 60 + utc_time.second) * 1000
        return utc_msec

    except:
        pass

    # Got here so must not be ISO format so try HH:MM:SS
    try:
        (utc_hours, utc_minutes, utc_seconds) = utc_str.split(":")
        utc_msec = (int(utc_hours) * 3600 + int(utc_minutes) * 60 + int(utc_seconds)) * 1000
        return utc_msec

    except:
        print("Error converting time string - ", utc_str)
   
    return -1

