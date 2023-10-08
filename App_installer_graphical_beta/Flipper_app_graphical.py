from git import Repo  
import os
import shutil
import tkinter as tk
from tkinter import filedialog
import platform  

class FirmwareInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Flipper Firmware Installer")

        self.app_name_label = tk.Label(root, text="Enter the Application Name:")
        self.app_name_label.pack()

        self.app_name_entry = tk.Entry(root)
        self.app_name_entry.pack()

        self.start_button = tk.Button(root, text="Start", command=self.choose_firmware)
        self.start_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def choose_firmware(self):
        self.app_name = self.app_name_entry.get()
        self.result_label.config(text="Please choose a firmware:")
        
        self.firmware_popup = tk.Toplevel(self.root)
        self.firmware_popup.title("Choose Firmware")

        self.selected_firmware = tk.StringVar()
        self.firmware_choices = {
            'Official Firmware': "https://github.com/flipperdevices/flipperzero-firmware.git",
            'Roguemaster': "https://github.com/RogueMaster/flipperzero-firmware-wPlugins.git",
            'Unleashed': "https://github.com/DarkFlippers/unleashed-firmware.git",
            'Xtreme': "https://github.com/Flipper-XFW/Xtreme-Firmware.git"
        }

        for firmware_name, firmware_url in self.firmware_choices.items():
            tk.Radiobutton(self.firmware_popup, text=firmware_name, variable=self.selected_firmware, value=firmware_url).pack()

        self.choose_button = tk.Button(self.firmware_popup, text="Choose", command=self.download_and_extract_firmware)
        self.choose_button.pack()

    def download_and_extract_firmware(self):
        selected_firmware_url = self.selected_firmware.get()
        if selected_firmware_url:
            folder_name = "flipperc"
            os.mkdir(folder_name)
            Repo.clone_from(selected_firmware_url, folder_name)

            app_user_folder = os.path.join(folder_name, "applications_user", self.app_name)
            os.makedirs(app_user_folder)

            fam_files = select_files("fam")
            c_files = select_files("c")

            for fam_file in fam_files:
                shutil.copy(fam_file, app_user_folder)
            for c_file in c_files:
                shutil.copy(c_file, app_user_folder)

            os.chdir(folder_name)

            if platform.system() == "Windows":
                os.system(f"fbt fap_{self.app_name}")
                os.system(f"fbt launch_app APPSRC={self.app_name}")
            else:
                os.system(f"./fbt fap_{self.app_name}")
                os.system(f"./fbt launch_app APPSRC={self.app_name}")

            self.result_label.config(text="Installation completed.")
        else:
            self.result_label.config(text="Please select a firmware.")

def select_files(extension):
    file_paths = filedialog.askopenfilenames(filetypes=[(f"{extension.upper()} Files", f"*.{extension}")])
    return file_paths

if __name__ == "__main__":
    root = tk.Tk()
    installer = FirmwareInstaller(root)
    root.mainloop()
