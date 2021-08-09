# spotipy tools (*name subject to change*)

## introduction

Frankly, I very much dislike the Spotify desktop app: there is limited spacing customization to prioritise the information most important to me, and there is no real way to clearly see and appreciate the beautifully-done album covers. This project intends to create a more customizable and more simple version of the Spotify interface, prioritizing the most important information and control functions first and foremost.

As this project is meant to act as a way to customize your Spotify viewing experience, feel free to copy and use it as you see fit. I've currently using the [Tkinter]() library to display information due to the relatively simple setup and control, but of course you're free to use whatever you want (PyGame, CLI, etc.). If you're a beginner and want to get to know how to use Tkinter and the various widgets available for it, check out [this]() W3D schools site.

***

## setup

This project was written in Python 3.9.5, but should work for all versions 3.0 and above. If you encounter an issue with the project using a Python 3 version before 3.9.5, contact me at <davidlechan@gmail.com> and I'll do my best to fix the issue.

### other libraries/projects

Basic setup of the project is quite simple, as even though two other projects are used (sharkhead2's [SpotipyFunction_Set](https://github.com/TheSharkhead2/SpotipyFunction_Set) and code49's [python_dev_tools](https://github.com/code49/python_dev_tools)), the most recent supported versions of each project should be packaged in with each 'Master' release of the project.

### Spotify API credentials

In order to be able to get data from the [Spotify API](), certain account-specific credentials are required, these being client_id, client_secret, and spotify_username. To get these, simply navigate to [Spotify for Developers](). sign in with your spotify account (no need to worry, there is no difference between a 'normal' and 'developer' spotify account), and create an app. Doing so should bring up a window with all the necessary API credential information. As a note, app creation will ask for a redirect_uri - this is essentially what the site will redirect users to in case authentication fails or something - www.google.com should suffice for this. Cloning the project from git and doing these steps should be sufficient for basic functionality from the command line.

### (optional) AHK shortcut setup

However, in addition to basic command line functionality, tools are already built in to use [AutoHotKey](https://www.autohotkey.com/) to make simple shortcuts. If you've got AutoHotKey installed, simply compile the desired .ahk script (each is labeled for the desired type of visualization) and do with the resulting .exe file what you want. Some custom ones I've made for my own use are available in the "application_icons" folder, but feel free to make your own (remember to get a .ico file if you're on OS X or a .icns, .rsc, or .bin file for Windows). My recommendation for making quick and dirty icons is the pixel art editor [Piskel](https://www.piskelapp.com/) (note that you'll need to find a service to convert files to icon format, fortunately many are available online for free), but of course you can use what you're more comfortable with as well.

***

## current visualizations/tools

- spotipy_stream: a simple widget that's useful for streamers looking to show chat what ((*totally* DMCA-free) music they're listening to
- spotipy_viewer: a slightly more complex widget meant for widespread desktop use, with fancy features like links to music videos, lyrics, and artist profiles; has multiple modes depending on presumed use case
- spotipy_controller: a simple widget for controlling music playback, meant to be used in conjunction with visualization widgets

## directory directory

See below a simple guide to navigating the project's code. This is here to help in case you want to customize the project or add your own features.

```
spotipy  
-----| /application icons/: this folder contains some sample files I made for use as AutoHotKey shortcut icons  
-----| /sample data/: this folder contains some sample files of data (more specifically data for Everglow's D+1) returned by the Spotify API, mostly for testing and reference reasons  
-----| /python_dev_tools/: this folder contains the latest supported version of code49:python_dev_tools (see above), used for various developer help functions  
-----| /SpotipyFunction_Set/: this folder contains the latest supported version of sharkhead2:SpotipyFunction_Set (see above), used for all Spotify API calls  
-----| /visualizers/: this folder contains all widgets relating to Spotify visualizations  
----------| basic_data.py: this file contains functions for getting basic song data needed for visualization, meant to be an easy way to get started creating a custom visualizer  
----------| spotipy_stream.py: this file contains the code for the spotify_stream viewer  
----------| spotipy_viewer.py: this file contains the code for the spotify_viewer (desktop) viewer  
-----| /tools/: this folder contains all widgets not related to visualizing spotify (e.g. controlling music playback)  
----------| spotipy_controller.py: this file contains the code for the spotify_controller, used for controlling music playback  
-----| run.py: this file contains the code for allowing code to be run more simply from the command line  
-----| ENVIRONMENT/CONFIG FILE HERE  
```

## known limitations

One of the greatest limitations to working with Spotify data and functions is, of course, the Spotify API. Currently, I'm using the [SpotipyFunction_Set](https://github.com/TheSharkhead2/SpotipyFunction_Set), which is a project I was a part of that serves to attempt to simplify the process of getting data from Spotify in Python. 

### authentication

One of the most biggest limitations to [Spotipy]() (the translation layer [SpotipyFunction_Set](https://github.com/TheSharkhead2/SpotipyFunction_Set) is using to make API calls) and the Spotify API in general is the periodic need for reauthentication or refreshing of the API token. Currently, [SpotipyFunction_Set](https://github.com/TheSharkhead2/SpotipyFunction_Set) gets around this by automatically refreshing the token whenever an error is encountered by an API-calling function, but obviously this comes with the caveat of also covering up non-authentication-related issues. However, we're currently working on using Spotify's API to refresh the token more specifically to when the program needs reauthentication, but in the meantime be warned that some API related issues may occur without erroring.

### friends

No, I don't mean that you don't have any friends, either real or on Spotify.  
This issue lies with the fact that the Spotify API doesn't offer methods for getting friend data, whether that be getting a list of the current user's friends, getting friend playback data, etc. Perhaps Spotify will eventually add some sort of route to allow public access to such data, but my presumption is that since friends would need to approve data access and the Spotify API has been left largely untouched since 2014, Spotify may never do this. 

### podcasts

Due to the way Spotify categorizes it's audio offerings, there is a slight difference between how podcast and song data is stored/managed. As 99.99% of what I listen to on Spotify is music, I've chosen to more or less ignore the case of podcasts, so be warned that listening to podcasts may cause issues with the code in this project.

### queue

One last known limitation to the Spotify API is the fact that there is no way to get data about the user's queued songs. This means that the closest thing we can do to getting a user's "queue" is to get data about the songs in whatever collection (i.e. album or playlist) the user is currently playing from and presume that represents the upcoming songs in the user's queue.

***

## planned future features

## f-a-q