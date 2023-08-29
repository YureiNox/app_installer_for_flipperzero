from git import Repo
import os
import shutil
from tkinter import filedialog

def select_files(extension):
    file_paths = filedialog.askopenfilenames(filetypes=[(f"{extension.upper()} Files", f"*.{extension}")])
    return file_paths

folder_name = "flipperc"
os.mkdir(folder_name)

firmware_choice = input("firmware selection: \n1- official firmware --> https://github.com/flipperdevices/flipperzero-firmware\n2- roguemaster --> https://github.com/RogueMaster/flipperzero-firmware-wPlugins\n3- unleashed --> https://github.com/DarkFlippers/unleashed-firmware\n4- xtreme --> https://github.com/Flipper-XFW/Xtreme-Firmware\npick one: ")

if firmware_choice == '1':
    repo_url = "https://github.com/flipperdevices/flipperzero-firmware.git"
    Repo.clone_from(repo_url, folder_name)

if firmware_choice == '2':
    repo_url = "https://github.com/RogueMaster/flipperzero-firmware-wPlugins.git"
    Repo.clone_from(repo_url, folder_name)

if firmware_choice == '3':
    repo_url = "https://github.com/DarkFlippers/unleashed-firmware.git"
    Repo.clone_from(repo_url, folder_name)

if firmware_choice == '4':
    repo_url = "https://github.com/Flipper-XFW/Xtreme-Firmware.git"
    Repo.clone_from(repo_url, folder_name)

fam_files = select_files("fam")
c_files = select_files("c")

app_name = input("Enter the name of the application: ")

app_user_folder = os.path.join(folder_name, "applications_user", app_name)
os.makedirs(app_user_folder)

for fam_file in fam_files:
    shutil.copy(fam_file, app_user_folder)
for c_file in c_files:
    shutil.copy(c_file, app_user_folder)

os.chdir(folder_name)

os.system(f"./fbt fap_{app_name}")
os.system(f"./fbt launch_app APPSRC={app_name}")

print("enjoy !!!")