import os
import datetime

def create_folder():
    now = datetime.datetime.now()
    now_str = now.strftime("%Y%m%d_%H%M%S")

    # Create a new folder with the current date and time
    folder_path = f"./data/results/{now_str}"
    os.makedirs(folder_path, exist_ok=True)

    return folder_path

def save_parameters(folder_path):
    # Read the content of config.py as a string
    with open("config.py", "r") as config_file:
        config_content = config_file.read()

    # Save the content of config.py as a text file
    with open(f"{folder_path}/config.txt", "w") as file:
        file.write(config_content)