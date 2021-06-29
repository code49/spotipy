#----- intro -----

"""
<add introductory comments here> 
"""

#----- load environment variables -----

#setup dotenv properly
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
print(find_dotenv())
load_dotenv(find_dotenv())

#----- create function to return environment variables to main file -----

def getSettings():
    settings = {
    #for each environment variable, use os.getenv() to load the value its key
    
    }
    
    return settings
