#----- intro -----

"""
This is meant to be the main, "just run this" file for the spotipy_stream viewer (i.e. a simplified, larger-font version 
for stream visibility purposes) - I might make this into multiple files at some point, might not, 
we'll see ¯\_(ツ)_/¯
"""

#----- setup dev stuff -----

from python_dev_tools import dev, final, setup #import the dev tool files, run setup routine

#----- import required modules -----

#spotipy api modules
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

#modules necessary to creating the visualization window
import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk as itk
from PIL import Image

#time for sleep()
import time

#multithreading for updating information and the visualization at the same time
import threading

#----- setup spotify constants -----
#in the future, it might be worthwhile to create a "settings" file of some variety to accomplish this

#spotipy api env variables - needed to create spotify_object (first would need to be updated if switching users)
username = "kcm4s9xdvua5ft5glrsxii3ki"
client_id = "60a52b9a3da546e6a7ef6248cb5ef464"
client_secret = "ea8bc44cc56e4f56aad11e073f7b2ee7"
scope = "user-read-currently-playing"
redirect_uri = "http://localhost:8888/callback"

#time between spotipy/tkinter info updates
update_delay = 2

#----- setup visualization constants -----

#tkinter window
window_title = "Spotify Stream Utility" #this is the title of the tkinter window
window_geometry = "800x300" #this is the size of the tkinter window, formatted as "widthxheight"

#font styles
font_styles = {
    "song": tkFont.Font(family="Arial", size=30, weight="bold"), #bolder, larger font style for song font
    "artist": tkFont.Font(family="Arial", size=20) #slimmer, smaller artist font
}

#text maximum lengths - FIX THIS LATER!
maximum_lengths = {
    "song": 25,
    "artist": 25
}

#placement coordinates
placement_coordinates = {
    "album_image": {"x": 0, "y": 0},
    "song_text": {"x": 320, "y": 85},
    "artist_text": {"x": 320, "y": 150}
}

#label padding
label_padding = {
    "song": {"x": 10, "y": 10},
    "artist": {"x": 10, "y": 10}
}

#default image size
default_image_size = 320

#----- setup spotipy api functions -----

def setupSpotifyObject(username, scope, client_id, client_secret, redirect_uri):
    """
    Function that sets up the spotify api token and subsequently the spotify object.

    Parameters
    ----------

    username: str
        spotify username of the intended user - note: not the display name of the user (mine, for example, is kcm4s9xdvua5ft5glrsxii3ki, not d.chan)

    client_id: str
        spotify api application client id - this can be found on the spotify developer dashboard
    
    client_secret: str
        spotify api application client secret - this can also be found on the spotify developer dashboard

    scope: str
        user-read-currently-playing (shouldn't need more than this for this application)

    redirect_uri: str
        http://localhost:8888/callback (just needs to be a live link, which this is)

    Returns
    -------

    spotify_object: spotipy object with scope "user-read-currently-playing"

    """

    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    return spotipy.Spotify(auth=token)



#----- setup tkinter/visualization -----

def shorten_text(content, length):
    """
    Shorten given texts to given lengths.

    Parameters
    ----------

    content: str
        text content to shorten

    length: int
        length to shorten the text to

    Returns
    -------

    content: str
        text content, shortened to at least length long
    """

    #check if content is too long
    if len(content) > length:
        
        #shorten content to the maximum length
        content = content[:length-3]

        #this ensures there aren't spaces before the ellipsis
        while content[-1] == " ":
            content = content[:len(content) - 1]

        #add ellipsis to the end of the shorten content
        content = content + "..."

    return content

#create necessary tkinter objects FINISH THIS FIRST!

class Start:
    """
    This is simply a class that handles actually operating the tkinter window. It needs to be a class in order to work without user input.
    """

    #initialize the tkinter window, don't worry too much about this
    def __init__(self, parent):
        self.label = tk.Label(window, text="")
        self.label.pack()
        self.label.after(3000, self.update_tkinter_variables) #this kick-starts updating of the tkinter variables

    def update_tkinter_variables(self):
        """
        Update all of the tkinter widgets based on spotipy api data.
        """

        dev.devPrint("updating tkinter variables...")

        #for all string variables
        tkinter_variable_list = [
            (artist_text, "artist text", True),
            (song_text, "song text", True),
        ]
        for object_o, name, shorten in tkinter_variable_list:
            try_except(object_o, name, shorten)

        #artist image
        try:
            image = itk.PhotoImage(Image.open("./images/album.jpg"))
        except:
            time.sleep(update_delay)
            try:
                image = itk.PhotoImage(Image.open("./images/album.jpg"))
            except:
                image = itk.PhotoImage(Image.open("./images/noalbumimage.jpg"))

        album_image_tk.configure(image=image)
        album_image_tk.image = image
        
        final_print("updating tkinter variables")

        self.label.after(update_delay*1000, self.update_tkinter_variables)

#----- setup multithreading -----

#----- run everything -----
