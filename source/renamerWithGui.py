import os, sys, shutil
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from fileB import Ui_Dialog  # Import the generated UI class

class MyApp(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open_directory_dialog)
        self.selected_directory = None  # Variable to store the selected directory path
        self.pushButton_2.clicked.connect(self.label_files)
        self.pushButton_3.clicked.connect(self.wifi_switcher)

    def open_directory_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Optional: Make the dialog read-only
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)

        if directory:
            # Check if the selected directory ends with "\yuzu\sdmc\ultimate\mods"
            if not directory.endswith("/yuzu/sdmc/ultimate/mods"):
                self.show_error_message("Selected directory must end with '/yuzu/sdmc/ultimate/mods'")
                return

            # Set the selected directory to the variable
            self.selected_directory = directory



    def ask_user_to_proceed(self, directory):
        msg_box = QMessageBox()
        msg_box.setText(f"Do you want to process the directory '{directory}'?")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = msg_box.exec_()
        return result

    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setText(message)
        error_box.setWindowTitle("Error")
        error_box.exec_()

    # New function for "wifi_switcher"
    def wifi_switcher(self):
        # Define the directory path you want to work with
        directory = self.selected_directory  # Use the selected directory

        if directory:
            # Check if the selected directory ends with "\yuzu\sdmc\ultimate\mods"
            if not directory.endswith("/yuzu/sdmc/ultimate/mods"):
                self.show_error_message("Selected directory must end with '/yuzu/sdmc/ultimate/mods'")
                return
        else:
            self.show_error_message("Please select a directory")
            return
            
        # Ask the user if they want to use ONLY 'wifi safe' folders
        msg_box = QMessageBox()
        msg_box.setText("Do you want to use ONLY 'wifi safe' folders?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec_()

        if result == QMessageBox.Yes:
            use_wifi_safe_only = True
        else:
            use_wifi_safe_only = False


        # Function to move a folder from one directory to another
        def move_folder(source_path, destination_path):
            folder_name = os.path.basename(source_path)
            destination_folder = os.path.join(destination_path, folder_name)
            shutil.move(source_path, destination_folder)

        # Path to the "NOT IN USE" folder
        not_in_use_folder_path = os.path.join(directory, 'NOT IN USE')

        # If the user wants to use ONLY 'wifi safe' folders
        if use_wifi_safe_only:
            # Move all "(not_wifi_safe)_" folders into the "NOT IN USE" folder
            folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
            for folder in folders:
                if folder.startswith('(not_wifi_safe)_'):
                    move_folder(os.path.join(directory, folder), not_in_use_folder_path)
        # If the user doesn't want to use ONLY 'wifi safe' folders
        else:
            # Move all folders from the "NOT IN USE" folder up one directory level
            items = os.listdir(not_in_use_folder_path)
            for item in items:
                item_path = os.path.join(not_in_use_folder_path, item)
                if os.path.isdir(item_path):
                    move_folder(item_path, directory)


    def label_files(self):

        directory = self.selected_directory

        if directory:
            # Check if the selected directory ends with "\yuzu\sdmc\ultimate\mods"
            if not directory.endswith("/yuzu/sdmc/ultimate/mods"):
                self.show_error_message("Selected directory must end with '/yuzu/sdmc/ultimate/mods'")
                return
        else:
            self.show_error_message("Please select a directory")
            return
        
        # Function to remove prefixes from folder names
        def remove_prefix(folder_path, prefix):
            folder_name = os.path.basename(folder_path)
            if folder_name.startswith(prefix):
                new_folder_name = folder_name[len(prefix):]
                new_folder_path = os.path.join(os.path.dirname(folder_path), new_folder_name)
                os.rename(folder_path, new_folder_path)

        # List all directories in the specified directory
        folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

        # Iterate through the directories and remove prefixes like "(wifi_safe)_" or "(not_wifi_safe)_"
        for folder in folders:
            folder_path = os.path.join(directory, folder)
            remove_prefix(folder_path, '(wifi_safe)_')
            remove_prefix(folder_path, '(not_wifi_safe)_')
            remove_prefix(folder_path, '_')

        ########################################################3
        folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

        # Function to rename a folder by adding a flag at the beginning
        def rename_folder(folder_path, flag):
            folder_name = os.path.basename(folder_path)
            new_folder_name = f"{flag}_{folder_name}"
            new_folder_path = os.path.join(os.path.dirname(folder_path), new_folder_name)
            os.rename(folder_path, new_folder_path)

        # Function to ask the user if a folder is "wifi safe"
        def is_wifi_safe(folder_name):
            msg_box = QMessageBox()
            msg_box.setText(f"Is folder '{folder_name}' wifi safe?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            result = msg_box.exec_()
            return result == QMessageBox.Yes

        # Iterate through the directories and ask if they are wifi safe
        for folder in folders:
            if folder == 'NOT IN USE' or folder == 'hdr' or folder == 'hdr-assets' or folder == 'hdr-stages':
                continue
            
            folder_path = os.path.join(directory, folder)

            if is_wifi_safe(folder):
                rename_folder(folder_path, '(wifi_safe)')
            else:
                rename_folder(folder_path, '(not_wifi_safe)')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
