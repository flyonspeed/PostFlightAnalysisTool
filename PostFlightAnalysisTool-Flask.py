# Flask web interface for the PostFlightAnalysisTool
# https://flask.palletsprojects.com/en/2.1.x/
# https://jinja.palletsprojects.com/en/3.1.x/templates/

import os
import sys
import io
import datetime

from pathlib import Path

from flask import Flask
from flask import render_template
   
import PostFlightAnalysisTool as pfat
#import Merge_Plot as mp
import Utils

app = Flask(__name__)   # Flask constructor
  
@app.route('/')      
def hello():
    return render_template('main_form.html')

# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------

# A decorator used to tell the application
# which URL is associated function
  
if __name__ == "__main__":
   app.run()
