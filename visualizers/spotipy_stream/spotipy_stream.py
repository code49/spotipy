#----- intro -----

"""
This is meant to be the main, "just run this" file for the spotipy_stream viewer (i.e. a simplified, larger-font version 
for stream visibility purposes); it should also serve as an easy jumping off point for creating your own custom spotify visualizer
"""
#----- setup spotipy-playback functions -----

from SpotipyFunction_Set import playback

#----- setup spotify constants -----
#in the future, it might be worthwhile to create a "settings" file of some variety to accomplish this

#spotipy api env variables - n needed to create spotify_object (first would need to be updated if switching users)
username = settings["USERNAME"]
client_id = settings["CLIENT_ID"]
client_secret = settings["CLIENT_SECRET"]
scope = "user-read-currently-playing"
redirect_uri = "http://localhost:8888/callback"

#time between spotipy/tkinter info updates
update_delay = 1

#----- create tk window object -----

#this needs to be done before the other objects are setup because an instance must be running for some configuration work can be done

#setup window according to window parameters
window = tk.Tk()

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
    "song": 24,
    "artist": 38
}

#placement coordinates
placement_coordinates = {
    "album_image": {"x": 0, "y": 0},
    "song_text": {"x": 310, "y": 85},
    "artist_text": {"x": 310, "y": 150},
    "progress_bar": {"x": 302, "y": 279}
}

#label padding
label_padding = {
    "song": {"x": 10, "y": 10},
    "artist": {"x": 10, "y": 10}
}

#default image size
default_image_size = 320

#----- create other necessary tkinter objects -----python main.py 

#customize window
window.title(window_title)
window.geometry(window_geometry)

#setup text labels
song_text = tk.StringVar()
song_text_tk = tk.Label(window, padx=label_padding["song"]["x"], pady=label_padding["song"]["y"], textvariable=song_text, font=font_styles["song"]) 
song_text_tk.place(x = placement_coordinates["song_text"]["x"], y = placement_coordinates["song_text"]["y"])

artist_text = tk.StringVar()
artist_text_tk = tk.Label(window, padx=label_padding["artist"]["x"], pady=label_padding["artist"]["y"], textvariable=artist_text, font=font_styles["artist"])
artist_text_tk.place(x = placement_coordinates["artist_text"]["x"], y = placement_coordinates["artist_text"]["y"])

#setup image - default to no_album_image.jpg
album_image = itk.PhotoImage(Image.open("./images/no_album_image.jpg"))
album_image_tk = tk.Label(window, image=album_image)
album_image_tk.place(x = placement_coordinates["album_image"]["x"], y = placement_coordinates["album_image"]["y"])

#setup progress bar
progress_bar_tk = tkttk.Progressbar(window, orient=HORIZONTAL, length=500, mode="determinate")
progress_bar_tk.place(x = placement_coordinates["progress_bar"]["x"], y = placement_coordinates["progress_bar"]["y"])

#----- setup spotipy api functions -----

def setupSpotifyObject(username, scope, client_id, client_secret, redirect_uri):
    """
    Function that sets up the spotify api token and subsequently the spotify object.

    Parameters
    ----------"

    username: str
        spotify username of the intended user - note: not the display name of the user (mine, for example, is kcm4s9xdvua5ft5glrsxii3ki, not d.chan)

    client_id: str
        spotify api application client id - this can be found on the spotify developer dashboard
    
    client_secret: str
        spotify api application client secret - this can also be found on the spotify developer dashboard

    scope: str
        scope of the resulting spotify object

    redirect_uri: str
        http://localhost:8888/callback (just needs to be a live link, which this is)

    Returns
    -------

    spotify_object: spotipy object 
        spotipy object with scope "user-read-currently-playing"

    """

    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    return spotipy.Spotify(auth=token)

def shortenText(content, length):
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

def chooseImage(images_list, default_size):
    """
    Returns the URL of the image closest to the desired size without going over.

    Parameters
    ----------

    images_list: list
        list of image dictionaries returned by the spotipy api. dictionaries are formatted as
        {'height': height, 'url': url, 'width': width}

    default_size: int
        default (also largest) size for the image

    Returns
    -------

    image_url: str
        string containing the url for the image with the correct size; "no image" if no image meets the size requirements exists
    """

    #cycle through every image in the list, backwards because they are ordered from large --> small
    try:
        for i in range(0, len(images_list)):
            if images_list[-i]["height"] > default_image_size: #assuming square images (i.e. same height and width)
                if i == 1:
                    return "no image"
                else:
                    return images_list[-(i - 1)]["url"] #returning the url of the image previous (i.e. the next smaller image)
                break #technically speaking, this should never be reached, but just in case
    
    #if anything errors (likely due to no images, which seem to occur from obscure but slightly older songs/artists, e.g. Arrumie Shannon)
    except:
        return "no image"

def updateTkinterVariables(spotify_object):
    """
    Function that updates the all of the various labels and images and returns them.

    Parameters
    ----------
    
    spotify_object: spotify object
        spotify object with scope 'user-read-currently-playing"

    Returns
    -------

    song_string: str
        the song's name as a string

    artist_string: str
        the song's artist name as a string

    album_image_filepath: str
        the filepath to the album image as a string
    """

    #add in a check just to ensure network problems don't crash the program
    try:
        dev.devPrint(f"checking play status: {playback.check_playing(spotify_object)}")
    except:
        dev.devPrint("checking play status: failed, likely due to network problems")

    #check if spotify is currently playing; this should prevent errors
    if playback.check_playing(spotify_object):

        #get the basic song info for the song
        artist, song_name, album_name, song_ID = playback.basic_song_info(spotify_object)

        #udpate various labels/images
        song_string = f"{shortenText(song_name, maximum_lengths['song'])}"
        artist_string = f"{shortenText(artist, maximum_lengths['artist'])}"

        final.finalPrint(f"{song_string} by {artist_string}")

        #get the image lists for the song
        try:
            album_image_data, aritst_image_data = playback.song_image_info(spotify_object)
        except:
            spotify_object = setupSpotifyObject(username, scope, client_id, client_secret, redirect_uri)
            album_image_data, aritst_image_data = playback.song_image_info(spotify_object)

        dev.devPrint(f"album image url: {chooseImage(album_image_data, default_image_size)}")

        #update album image accordingly
        resource = urllib.request.urlopen(chooseImage(album_image_data, default_image_size))
        output = open("./images/album.jpg","wb")
        output.write(resource.read())
        output.close()

        final.finalPrint(f"album image: {chooseImage(album_image_data, default_image_size)}")

        #update the album_image_filepath as well
        album_image_filepath = "./images/album.jpg"

        #update the value for the progress bar
        current_progress, total_length = playback.playback_time_info(spotify_object, "ms")
        progress_bar_tk['value'] = (current_progress/total_length)*100

        dev.devPrint(f"current progress: {(current_progress/total_length)*100}%")

    else: #this should only run when nothing is playing, but it's also good if something unexpectedly breaks

        dev.devPrint("some error occured (or, more likely, nothing is playing)...setting labels and images to defaults.")
        #set labels to placeholders
        song_string = "not playing anything"
        artist_string = shortenText("\"TempT > flame\" - TempT", maximum_lengths["artist"])

        #set image to the default red square
        album_image_filepath = "./images/no_album_image.jpg"

        #value of the progress bar will remain the same as last update

        final.finalPrint("some issue occurred, labels have been set to defaults.")
    
    return song_string, artist_string, album_image_filepath

#----- setup tkinter/visualization -----

class Start:
    """
    This is simply a class that handles actually operating the tkinter window. It needs to be a class in order to work without user input.
    """

    #initialize the tkinter window, don't worry too much about this
    def __init__(self, windwow, spotify_object):
        self.label = tk.Label(window, text="")
        self.label.pack()
        self.label.after(3000, lambda: self.updateTkinter(spotify_object)) #this kick-starts updating of the tkinter variables

    def updateTkinter(self, spotify_object):
        """
        Update all of the tkinter widgets based on spotipy api data.

        Parameters
        ----------

        spotify_object: spotipy api object
            spotipy api object with scope 'user-read-currently-playing'

        Returns
        -------
        
        None
        """

        dev.devPrint("updating tkinter...")

        song_string, artist_string, album_image_filepath = updateTkinterVariables(spotify_object)

        #set string variables
        song_text.set(song_string)
        artist_text.set(artist_string)

        #artist image
        try:
            image = itk.PhotoImage(Image.open(album_image_filepath))
        except:
            image = itk.PhotoImage(Image.open("./images/no_album_image.jpg"))

        album_image_tk.configure(image=image)
        album_image_tk.image = image
        
        final.finalPrint("updating tkinter variables...")
        final.finalPrint("-----------------------------")

        try:
            self.label.after(update_delay*1000,lambda: self.updateTkinter(spotify_object))
        except:
            spotify_object = setupSpotifyObject(username, scope, client_id, client_secret, redirect_uri)
            self.label.after(update_delay*1000,lambda: self.updateTkinter(spotify_object))

#----- run everything -----

def main():
    """
    This is just meant to be a function that runs everything, technically speaking this isn't needed now because I'm not using multithreading anymore, but oh well.
    
    Parameters
    ----------

    Returns
    -------
    
    """

    final.finalPrint("starting spotify_stream components...")
    
    #setup spotify object
    spotify_object = setupSpotifyObject(username, scope, client_id, client_secret, redirect_uri)

    #create instance of class start, run update_tknter variables
    start = Start(window, spotify_object)
    
    final.finalPrint("all components have finished starting...")
    time.sleep(2)
    # final.clear()

    #start the tkinter window update loop
    window.mainloop()

main()
