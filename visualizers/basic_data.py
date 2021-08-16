#----- intro -----

"""
This file is meant to create a class with functions that do all basic processing of 
the data received from SpotipyFunction_Set for the purposes of displaying information
to the user (e.g. creating image objects, processing "basic" song data)
"""

#"setup dev stuff," "load environment variables," and "import required modules"
#aren't needed here since this file will be imported into run.py and subsequently be passed into the various widget classes

#----- code -----

class BasicData():

    """
    This class is meant to aggregate all basic processing of the data received from 
    SpotipyFunction_Set as well as some easy helper functions; see above. 
    """

    def __init__(self, spotipy_object, path_to_images, dev_print, final_print):

        #make the spotipy object a class property so other methods can access it
        self.spotipy_object = spotipy_object
        
        #do the same for the path_to_images; this makes it easy to navigate and edit the images
        self.path_to_images = path_to_images

        #setup the two print functions as class properties for use internally
        self.devPrint = dev_print
        self.finalPrint = final_print

    #----- unchanged SpotipyFunction_Set functions -----

    def basicSongInfo(self, spotipy_object) -> "tuple[str, str, str, str]":
        """
        return basic song information, as returned by the spotipy API

        Parameters:
        -----------
        
        spotipy_object: SpotipyFunction_Set class instance
            Spotipy2 class instance

        Returns:
        --------
        
        tuple[artist, songName, albumName, songId]:
            artist: str 
                The artist name as a string 
            songName: str 
                The name of the song as a string 
            albumName: str 
                The name of the album as a string 
            songID: str 
                The Spotify song id as a string

        """

        return spotipy_object.Playback.basic_song_info()

    #----- text handling -----

    def shortenText(self, content, max_length) -> str:
        """
        shorten given texts to given lengths.

        Parameters:
        ----------

        content: str
            text content to shorten

        max_length: int
            length to shorten the text to, if necessary

        Returns:
        -------

        content: str
            text content, shortened to at least length long
        """

        #check if content is too long
        if len(content) > max_length:
            
            #shorten content to the maximum length
            content = content[:max_length-3]

            #this ensures there aren't spaces before the ellipsis
            while content[-1] == " ":
                content = content[:len(content) - 1]

            #add ellipsis to the end of the shorten content
            content = content + "..."

        return content

    #----- image handling -----

    def pickImageUrl(self, image_list, max_image_size, priority="width") -> "tuple[str, bool]":
        """
        pick an image url from a given url list, as given by the spotify API;
        picks an image of equal size or smaller than the given value.

        Parameters:
        -----------

        image_list: list
            list of images to choose from, as given by the spotify API

        max_image_size: int
            integer representing the maximum size (in the given direction) of the image chosen

        priority: str
            either "width" or "height" depending on which should be prioritised for being closest to the 
            max_image_size without going over; defaults to "width"

        Returns:
        --------

        tuple[image_url, success]:
            image_url: str
                url of the chosen image, "" if something fails

            success: bool
                boolean representing whether an image was successfully chosen or not

        """

        #cycle through every image in the list, backwards because they are ordered from large --> small
        try:
            for i in range(0, len(image_list)):
                if image_list[-i][priority] > max_image_size: #assuming square images (i.e. same height and width), but if not assume width is more important
                    if i == 1:
                        return ("", False)
                    else:
                        return (image_list[-(i - 1)]["url"], True) #returning the url of the image previous (i.e. the next smaller image)
                    break #technically speaking, this should never be reached, but just in case
        
        #if anything errors (likely due to no images, which seem to occur from obscure but slightly older songs/artists, e.g. Arrumie Shannon)
        except:
            return ("", False)
        
    def getImageObject(self, image_url=None, filepath_to_image=None) -> "PIL_image_object":
        """
        returns an image object representing either the requested image, which is given in either url format 
        or filepath format; defaults to image_url format if both are given.
        
        Parameters:
        -----------

        image_url: str
            string representing the url of the requested image; defaults to None
        
        filepath_to_image: str
            string representing the filepath of the requested image; defaults to None

        Returns:
        --------

        results: PIL image object
            PIL image object representing the requested image
        """

        if image_url != None and filepath_to_image != None:
            if image_url != None:
                return urllib.request.urlopen(image_url)
            else:
                #CODE TO READ FROM FILEPATH, GET PIL OBJECT FROM THAT
                pass
        else:
            raise TypeError("getImageObject(): requested an image object, but did not provide an image_url or a filepath_to_image")
            exit

    def setImage(self, image_name, path_to_image, image_object) -> "tuple[bool, str]":
        """
        sets the value of a given .jpg image to the given PIL image object;
        returns true or false depending on whether it is successful or not.

        Parameters:
        -----------
        
        image_name: str
            string representing what the image is called (e.g. "artist_image.jpg")
        
        path_to_image: str
            string representing the path from the working directory to where the image is

        image_object: PIL image object
            PIL image object representing what the .jpg image should be set to, as returned by
            urllib.request.urlopen()

        Returns:
        --------

        tuple[success, error_str]:
            success: bool
                boolean representing whether setting the image's value was successful or not
            
            error_str: str
                string representing the returned error message, if any; otherwise is empty
        """
        
        success = True
        error_str = ""

        #attempt to set the requested image to the given PIL image object value
        try:
            output = open((path_to_image + image_name), "wb")
            output.write(image_object.read())
            output.close()

        except:
            success = False
            error_str = "error str here"
        
        #return the tuple of success, error_str
        return (success, error_str)

    def handleImage(self, spotipy_object, image_type, path_to_images, image_name, failsafe_image_name, max_image_size, priority="width") -> None:
        """
        function that handles aggregates the last 3 functions together to setup images for future retrieval; 
        if that fails, setup the backup image instead.
        
        Parameters:
        -----------

        spotipy_object: SpotipyFunction_Set class instance
            Spotipy2 class instance
        
        image_type: str
            "artist" or "album" depending on the desired type of image

        path_to_images: str
            string representing the filepath to the image's location
        
        image_name: str
            string representing the name of the image (e.g. "artist_image.jpg")
        
        max_image_size: int
            integer representing the maximum size (in the given direction) of the image chosen

        priority: str
            either "width" or "height" depending on which should be prioritised for being closest to the 
            max_image_size without going over; defaults to "width"

        Returns:
        --------

        None
        """

        #get the list of album or artist images according to what is requested
        if image_type == "artist":
            image_list = spotipy_object.Playback.song_image_info()[0]
        elif image_type == "album":
            image_list = spotipy_object.Playback.song_image_info()[1]
        else:
            raise TypeError(f"handleImage(): expected 'artist' or 'album', instead got invalid image_type: {str(image_type)}")
            exit

        #set the image, as requested
        try:
            self.setImage(image_name, path_to_images, self.getImageObject(image_url=self.pickImageUrl(image_list, max_image_size, priority)))
        except: #error handling
            self.devPrint(f"handleImage(): WARN; failed to properly setup {image_name} with a/an {image_type} image...defaulting to using {failsafe_image_name}")
            self.devPrint(f"handleImage(): WARN; reason for failure: {'reason_for_failure'}")
            try: #trying to use the failsafe image
                self.setImage(failsafe_image_name, path_to_images, self.getImageObject(image_url=self.pickImageUrl(image_list, max_image_size, priority)))
            except: #failsafe image failed, exit the program
                self.finalPrint(f"handleImage(): FAIL; failed to properly setup {image_name} with {failsafe_image_name}")
                self.finalPrint(f"handleImage(): FAIL; reason for failure: {'reason_for_failure'}")
                exit

    #----- progress bar handling -----

    def getProgressBarValue(self, current_value, total_value) -> int:
        """
        gets the proper 'value' for a Tkinter progress bar, according to current_value and total_value

        Parameters:
        -----------

        current_value: int
            integer representing the "current value" portion of the Tkinter progress bar
        
        total_value: int
            integer representing the "total value" the Tkinter progress bar should represent

        Returns:
        --------

        value: int
            integer representing the 'value' that should be inputted into the Tkinter progress bar 
        """

        return ((current_value/total_value)*100)

    #----- url handling -----