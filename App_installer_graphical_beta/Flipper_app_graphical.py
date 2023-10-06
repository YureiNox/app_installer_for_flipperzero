import os
import shutil
import tkinter as tk
from tkinter import filedialog
from git import Repo  # Importation de la classe Repo depuis le module git

def select_files(extension):
    file_paths = filedialog.askopenfilenames(filetypes=[(f"{extension.upper()} Files", f"*.{extension}")])
    return file_paths

def clone_repository():
    repo_urls = {
        'Official Firmware': "https://github.com/flipperdevices/flipperzero-firmware.git",
        'Roguemaster': "https://github.com/RogueMaster/flipperzero-firmware-wPlugins.git",
        'Unleashed': "https://github.com/DarkFlippers/unleashed-firmware.git",
        'Xtreme': "https://github.com/Flipper-XFW/Xtreme-Firmware.git"
    }

    selected_repo = repo_choice_var.get()
    repo_url = repo_urls.get(selected_repo)

    if repo_url:
        folder_name = "flipperc"
        os.mkdir(folder_name)
        Repo.clone_from(repo_url, folder_name)

        app_name = app_name_entry.get()
        app_user_folder = os.path.join(folder_name, "applications_user", app_name)
        os.makedirs(app_user_folder)

        fam_files = select_files("fam")
        c_files = select_files("c")

        for fam_file in fam_files:
            shutil.copy(fam_file, app_user_folder)
        for c_file in c_files:
            shutil.copy(c_file, app_user_folder)

        os.chdir(folder_name)
        os.system(f"./fbt fap_{app_name}")
        os.system(f"./fbt launch_app APPSRC={app_name}")

        result_label.config(text="enjoy !!!")
    else:
        result_label.config(text="Please select a valid repository.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Flipper Firmware Downloader")

# Étiquettes
repo_choice_label = tk.Label(root, text="Select a Firmware Repository:")
repo_choice_label.pack()
app_name_label = tk.Label(root, text="Enter the Application Name:")
app_name_label.pack()

# Liste déroulante pour le choix du référentiel
repo_choices = ['Official Firmware', 'Roguemaster', 'Unleashed', 'Xtreme']
repo_choice_var = tk.StringVar(root)
repo_choice_var.set(repo_choices[0])
repo_choice_dropdown = tk.OptionMenu(root, repo_choice_var, *repo_choices)
repo_choice_dropdown.pack()

# Entrée de texte pour le nom de l'application
app_name_entry = tk.Entry(root)
app_name_entry.pack()

# Bouton pour cloner le dépôt et exécuter les commandes
clone_button = tk.Button(root, text="Clone Repository and Execute", command=clone_repository)
clone_button.pack()

# Étiquette de résultat
result_label = tk.Label(root, text="")
result_label.pack()

# Lancer la boucle Tkinter
root.mainloop()
