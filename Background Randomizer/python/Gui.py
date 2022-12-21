import webview
import os
from pystray import Icon, Menu as menu, MenuItem as item
from PIL import Image

# Import the join function from the os.path module and the Api class from the Api module
from os.path import join
from Api import Api


# Define Assets Folder
ASSETS_FOLDER = join(os.path.dirname(__file__), '..', 'assets')

TRAY_ICON = join(ASSETS_FOLDER, 'icon.ico') # Define Path to icon 
HTML = join(ASSETS_FOLDER, 'index.html') # Define Path to HTML
CSS = join(ASSETS_FOLDER, 'style.css') # Define Path to CSS
JS = join(ASSETS_FOLDER, 'main.js') # Define Path to Javascirpt

global gui_active
global gui_initiated
gui_active = False
gui_initiated = False

class Gui:
    # Create an instance of the Api class
    global api 
    
    api = Api()
    
    def start_gui(self, start_gui_open):
        """
        Function to start the GUI window using webview.
        
        Args:
            start_gui_open (bool): used to determine if GUI should open at startup
        """
        global window, gui_active, gui_initiated
            
        if not gui_active:
            # Open the HTML file and read its contents
            with open(HTML) as f:
                html = f.read()
            
            gui_active = True
            gui_initiated = True
        
            # Create a webview window with the specified HTML content, API, dimensions, and resizability
            window = webview.create_window("Background Randomizer", html=html, js_api=api, width=525, height=500, resizable=False, frameless=True, easy_drag=True)

            # Start the window
            webview.start(self.load_files, args=[start_gui_open])
            
    def load_files(self, start_gui_open):
        """
        Function to start the GUI window using webview.
        
        Args:
            start_gui_open (bool): used to determine if GUI should open at startup
        """
        # Open the CSS file and read its contents
        with open(CSS) as f:
            css = f.read()
        
        # Open the JS file and read its contents
        with open(JS) as f:
            js = f.read()
        
        # Loads CSS & JS to Window
        window.load_css(css)
        window.evaluate_js(js)
        
        # Redeclare global gui_active for interacting with other threads
        global gui_active
        
        # Determines if gui is active and changes window to hidden or shown based on startup
        if not start_gui_open:
            window.hide()
            gui_active = False
        else:
            window.show()
            gui_active = True

    def toggle_gui(self):
        """
        Function to toggle GUI from active and unactive states
        """
        # Redeclare global gui_active for interacting with other threads
        global gui_active
        
        # Determines if gui is active and changes window to hidden or shown
        if gui_active == True:
            window.hide()
            gui_active = False
        else:
            window.show()
            gui_active = True

    def destroy(self):
        """
        Function to destroy the GUI window.
        """
        # Redeclare global gui_active for interacting with other threads
        global gui_active
        
        # Determines if gui is active and destroys the actual window
        if gui_active == True:
            window.destroy()
            gui_active = False
        else:
            return ""


    def load_tray_icon(self):
        """
        Function to load the tray icon and create the menu options.
        """
        self.icon = Icon('mon')
        self.icon.menu = menu(item('Open',self.toggle_gui, default=True), item('Change Background',api.call_bg_set),item('Exit',self.exit_action))
        self.icon.icon = Image.open(TRAY_ICON)
        self.icon.title = "Background Randomizer"
        self.icon.HAS_DEFAULT_ACTION = True
   
        self.icon.run()
    
    def icon_setup(self):
        """
        Function to make the tray icon visible.
        """
        self.icon.visible = True
    
    def exit_action(self):
        """
        Function to handle the Exit option in the tray icon menu.
        """
        self.icon.visible = False
        self.destroy()
        api.exit_program()
        self.icon.stop()
