from Gui import *
from Api import *
import sys
import threading
from os.path import join

# Define the path to the assets folder
CUR_DIRECTORY = os.path.dirname(__file__)
ASSETS_FOLDER = join(CUR_DIRECTORY, '..', 'assets')

# Create an instance of the Api class
api = Api()

# Create an instance of the Gui class
gui = Gui()

# Load the config file
config = api.load_config()

def check_gui():
    """
    Function to check if the GUI should be loaded at startup.
    """
    # Determine if the GUI should be loaded based on the number of command line arguments
    load_gui_at_start = len(sys.argv) >= 2

    # Start the GUI with the determined flag
    gui.start_gui(load_gui_at_start)

# If the SHORTCUT_CREATED flag in the config is not set, create a shortcut on the desktop
if not config['SHORTCUT_CREATED']:
    api.create_shortcut('Desktop', 'Gui Start.bat')

# Set up the application to run at startup
api.autostart_setup()

# Start a new thread to run the background schedule in the background
schedule_thread = threading.Thread(target=api.background_schedule)
schedule_thread.start()

# Start a new thread to run the tray icon
icon_tray_thread = threading.Thread(target=gui.load_tray_icon)
icon_tray_thread.start()

# Check if the GUI should be loaded at startup
check_gui()
