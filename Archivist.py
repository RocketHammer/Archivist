import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlDir
from pyforms.controls import ControlButton
from pyforms.controls import ControlCombo
from pyforms import start_app
from datetime import datetime
import calendar
import shutil
import os

class GUIWindow(BaseWidget):
    def __init__(self):
        super().__init__("LogFormat")

        # Create controls
        self._runButton = ControlButton('Run')
        self._srcNav = ControlDir(label="Source: ")
        self._destNav = ControlDir(label="Destination: ")
        self._user = ControlCombo("User: ")

        # Organize layout
        self.formset = ['_user', '_srcNav', '_destNav', '_runButton', ' ']

        # Link events
        self._runButton.value = self._runAction
        self._srcNav.changed_event = self._NavUpdate
        self._destNav.changed_event = self._NavUpdate

        # Set initial values
        self._runButton.enabled = os.path.exists(self._srcNav.value) and os.path.exists(self._destNav.value)
        self._srcNav.value = "C:\\Users\\Travis\\Desktop\\Source"
        self._destNav.value = "C:\\Users\\Travis\\Desktop\\Dest"
        users = ["Sam", "Travis"]
        for item in users:
            self._user.add_item(item)

    def _runAction(self):
        source = self._srcNav.value
        dest = self._destNav.value
        user_path = os.path.join(dest, self._user.value)

        with open(os.path.join(user_path, 'results.txt'), 'w') as resultsFile:
            #Make user directory
            if not os.path.exists(user_path):
                os.mkdir(user_path)
                resultsFile.write("New directory: " + user_path + "\n")

            for f in os.listdir(source):
                valid_file = True
                file_path = os.path.join(source, f)
                file, extension = os.path.splitext(f)

                if extension == '.mp4':
                    file_type = "Video"
                elif extension == '.jpg':
                    file_type = "Image"
                else:
                    valid_file = False
                    resultsFile.write("ERROR: Unsupported file type: " + f + "\n")

                # So far, MP4 and JPG from Google Pixel 2 have same metadata and can be handled identically.
                # If this is ever not the case, the above if-elif statement will need to include code for parsing
                # specific metadata
                if valid_file:
                    file_time = datetime.fromtimestamp(os.stat(os.path.join(source, f)).st_mtime)

                    # Make directory for the year if it doesn't exist
                    year_path = os.path.join(user_path, str(file_time.year))
                    if not os.path.exists(year_path):
                        os.mkdir(year_path)
                        resultsFile.write("New directory: " + year_path + "\n")

                    # Make directory for the month if it doesn't exist
                    month_name = calendar.month_abbr[file_time.month]
                    month_path = os.path.join(year_path, month_name)
                    if not os.path.exists(month_path):
                        os.mkdir(month_path)
                        resultsFile.write("New directory: " + month_path + "\n")

                    # Make directory for the day if it doesn't exist
                    day_path = os.path.join(month_path, str(file_time.day))
                    if not os.path.exists(day_path):
                        os.mkdir(day_path)
                        resultsFile.write("New directory: " + day_path + "\n")

                    newfile_name = "{}_{}`{}`{}".format(file_type, str(file_time.hour), str(file_time.minute), str(file_time.second))
                    newfile_path = os.path.join(day_path, newfile_name + extension)
                    if not os.path.exists(newfile_path):
                        #shutil.move(file_path, newfile_path)
                        shutil.copy(file_path, newfile_path)
                        resultsFile.write(file_path + " moved to " + newfile_path + "\n")

    def _NavUpdate(self):
        if os.path.exists(self._srcNav.value) and os.path.exists(self._destNav.value):
            self._runButton.enabled = True

if __name__ == "__main__":
    start_app(GUIWindow, geometry=(200, 200, 400, 200))