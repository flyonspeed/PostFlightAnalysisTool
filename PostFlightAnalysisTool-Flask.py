# This Python file uses the following encoding: utf-8
import os
import sys
import io
import datetime

from pathlib import Path

from flask import Flask    
   
import PostFlightAnalysisTool as pfat
#import Merge_Plot as mp
import Utils

app = Flask(__name__)   # Flask constructor
  
@app.route('/')      
def hello():
    return  \
'<label for="myfile">Select a file:</label>' \
'<input type="file" id="myfile" name="myfile">'

# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------

# A decorator used to tell the application
# which URL is associated function
  
if __name__ == "__main__":
   app.run()
