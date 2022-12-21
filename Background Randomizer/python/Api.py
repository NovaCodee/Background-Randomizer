import json
import Randomizer  # import the Randomizer module
import threading
import os
from os.path import join
import winshell
import win32com.client
import time

# create a reference to the Randomizer module
wp = Randomizer  

# Define the path to the assets and config folders
CUR_DIRECTORY = os.path.dirname(__file__)
ASSETS_FOLDER = join(CUR_DIRECTORY, '..', 'assets')
CONFIG_FILE_LOCATION = join(CUR_DIRECTORY, '..', 'config.json')
DEV_DIRECTORY = join(CUR_DIRECTORY, '..', 'dev tools')
START_DIRECTORY = join(
    os.path.expanduser("~"),
    "AppData",
    "Roaming",
    "Microsoft",
    "Windows",
    "Start Menu",
    "Programs",
    "Startup",
)


class Api:

    def exit_program(self):
        """
        Exit the program.
        """
        # Create an event to exit the loop
        exit_event = threading.Event()
        exit_event.set()

        # Keep checking the exit event until it is set, then exit the program
        while exit_event.is_set():
            exit_event.wait(1)
            os._exit(0)

    def call_bg_set(self):
        """
        Call the bg_set function of the Randomizer module
        """
        wp.bg_set()  # call the bg_set function

    def toggle_gui_api(self):
        """
        Toggle the GUI window.
        """
        # Conditional import of Gui due to threading
        import Gui

        Gui.Gui().toggle_gui()

    def update_settings(self, config_values):
        """
        Update the value of a setting in the config.json file.

        Args:
            config_values (dict): A dictionary of config values to update.
        """
        # load the config file
        with open(CONFIG_FILE_LOCATION, 'r') as file:
            config = json.load(file)

        # Runs Autostart to confirm autostart has been configiured with new settings
        self.autostart_setup()

        # Update the value of each setting in the config
        for key in config.keys():
            config[key] = config_values[key]

        # Save the updated config to the file
        with open(CONFIG_FILE_LOCATION, 'w') as file:
            json.dump(config, file)

    def update_single_setting(self, s_key, s_value):
        """
        Update the value of a single setting in the config.json file.

        Args:
            s_key (str): The key of the setting to update.
            s_value: The new value for the setting.
        """
        #  Load the config file
        with open(CONFIG_FILE_LOCATION, 'r') as file:
            config = json.load(file)

        # Update the value of the specified setting
        config[s_key] = s_value

        # Save the updated config to the file
        with open(CONFIG_FILE_LOCATION, 'w') as file:
            json.dump(config, file)

    def load_config(self):
        """
        Load the config.json file and return the contents
        """
        # load the config file
        with open(CONFIG_FILE_LOCATION, 'r') as file:
            config = json.load(file)

        return config

    def create_shortcut(self, location, target_program):
        """
        Create a shortcut to the program in the specified location.

        Args:
            location (str): The location where the shortcut should be created.
            target_program (str): The path to the program to create a shortcut to.
        """
        # Determine the path to the shortcut based on the location
        if location == "Desktop":
            desktop = winshell.desktop()
            path = join(desktop, 'Background Randomizer.lnk')
            self.update_single_setting('SHORTCUT_CREATED', True)
        else:
            path = join(location, 'Background Randomizer.lnk')
            self.update_single_setting('AUTOSTART_SHORTCUT_CREATED', True)

        # Get the path to the target program and the icon file
        icon = join(ASSETS_FOLDER, 'icon.ico')
        target = join(location, target_program)
        # Create a shortcut using the win32com library
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.IconLocation = icon
        shortcut.save()

    def delete_shortcut(self, location):
        """
        Delete the shortcut to the program from the specified location.

        Args:
            location (str): The location where the shortcut should be deleted.
        """

        # Determine the path to the shortcut based on the location
        if location == "Desktop":
            desktop = winshell.desktop()
            os.remove(join(desktop, 'Background Randomizer.lnk'))
            self.update_single_setting('SHORTCUT_CREATED', False)
        else:
            os.remove(join(location, 'Background Randomizer.lnk'))
            self.update_single_setting('AUTOSTART_SHORTCUT_CREATED', False)

    def autostart_setup(self):
        """
        Set up the program to start automatically when the user logs in.
        """
        # Paths to start files
        gui_start = join(DEV_DIRECTORY, 'Gui Start.bat')
        non_gui_start = join(DEV_DIRECTORY, 'Start.bat')

        # load the config file
        with open(CONFIG_FILE_LOCATION, 'r') as file:
            config = json.load(file)

        # Check if autostart is enabled
        if config['AUTOSTART']:

            # Check if autostart with GUI is enabled
            if config['AUTOSTART_GUI']:
                # Delete existing shortcut if it exists
                if os.path.exists(join(START_DIRECTORY, 'Background Randomizer.lnk')) == True:
                    self.delete_shortcut(START_DIRECTORY)
                # Create a shortcut to the GUI start file
                self.create_shortcut(START_DIRECTORY, gui_start)
            else:
                # Delete existing shortcut if it exists
                if os.path.exists(join(START_DIRECTORY, 'Background Randomizer.lnk')) == True:
                    self.delete_shortcut(START_DIRECTORY)
                # Create a shortcut to the non-GUI start file
                self.create_shortcut(START_DIRECTORY, non_gui_start)
        else:
            # Delete existing shortcut if it exists
            if os.path.exists(join(START_DIRECTORY, 'Background Randomizer.lnk')) == True:
                self.delete_shortcut(START_DIRECTORY)

    def background_schedule(self):
        """
        Function to schedule the task to change the background image.
        """
        while True:

            # load the config file
            with open(CONFIG_FILE_LOCATION, 'r') as file:
                config = json.load(file)

            time_interval = int(config['SLIDESHOW_INTERVAL']) * 60

            time.sleep(time_interval)
            wp.bg_set()  # call the bg_set function
