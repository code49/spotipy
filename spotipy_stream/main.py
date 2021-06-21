#----- intro -----

"""
This is meant to be the main, "just run this" file for the spotipy_stream viewer (i.e. a simplified, larger-font version 
for stream visibility purposes) - I might make this into multiple files at some point, might not, 
we'll see ¯\_(ツ)_/¯
"""

#----- setup dev stuff -----

from python_dev_tools import dev, final, setup #import the dev tool files, , run setup routine

#----- import required modules -----

#spotipy api modules
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


#----- code -----