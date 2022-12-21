import ctypes
import os
import random
import requests
import json
from os.path import join
from PIL import Image



# Define Current Directory, config file locaction and asset folder
CUR_DIRECTORY = os.path.dirname(__file__)
ASSETS_FOLDER = join(CUR_DIRECTORY, '..', 'assets')
CONFIG_FILE_LOCATION = join(CUR_DIRECTORY, '..','config.json')

# Import config file
config = json.load(open(CONFIG_FILE_LOCATION, 'r'))
    
# Initialize config variables
folder = config['FOLDER']
client_id = config['CLIENT_ID']

# Constant for setting wallpaper
SPI_SETDESKWALLPAPER = 20
# ------------------------------------------------------

# Configures Id for use in code
client_id = "client_id=" + client_id

def bg_set():
    """
    Function to set the background image.
    """
    # loads config
    config = json.load(open(CONFIG_FILE_LOCATION, 'r'))

     # Check if Unsplash is enabled for image call
    if config['UNSPLASH']:
        # Request random image from Unsplash
        res = requests.get('https://api.unsplash.com/photos/random?' +
                           client_id, params={"orientation": "landscape", "query": config['TAGS']})
        download_url = json.loads(res.content)["urls"]["regular"]
        # Request the actual image from raw URL
        bg_img = requests.get(download_url, allow_redirects=True)
        # Write image from Unsplash to tmp file for reading later
        open(join(ASSETS_FOLDER, 'tmp', 'unsplash_temp.png'), "wb").write(bg_img.content)
        # Set the background image to Unsplash image
        bg_file = join(ASSETS_FOLDER, "tmp", "unsplash_temp.png")
    else:       
        # Define the image folder by joining directories and folder
        img_folder = join(ASSETS_FOLDER, folder)
        
        # Get all files from folder specified in FOLDER var
        files = os.listdir(img_folder)
         # Create a random number for fetching a random image
        rnd = random.randint(0, len(files)-1)
        # Set background image to random image from specified folder
        bg_file = join(img_folder, files[rnd])

    #Checks if Pixliation is called or not
    if config['PIXILATE']:
        # Open Image
        img = Image.open(bg_file)
        pixilation = int(config['PIXILATION_AMOUNT'])
        # Resize image down
        img_small = img.resize((pixilation,pixilation),resample=Image.Resampling.BILINEAR)
        
        # Scale image back up to size
        result = img_small.resize(img.size, Image.Resampling.NEAREST)
        bg_file = join(ASSETS_FOLDER, 'tmp','resize.png')
        result.save(bg_file)
        
    # Set Windows background for current user
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, bg_file, 3)
    
