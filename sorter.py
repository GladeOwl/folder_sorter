"""Sort file into subfolders based on extensions"""

import json
import os

from dotenv import load_dotenv

load_dotenv()

FOLDER_PATH: str = os.getenv("FOLDER_PATH")
with open("folders.json", "r", encoding="utf-8") as JSONFILE:
    SUB_FOLDERS: dict = json.load(JSONFILE)


def create_folders(sub_folders: dict):
    """Create folders if they don't exist"""

    for folder in sub_folders.keys():
        _path: str = os.path.join(FOLDER_PATH, folder)
        os.makedirs(_path, exist_ok=True)


def rename_exists(name: str, extension: str, folder_path: str):
    """Rename the file to be dissimilar to the existing file"""

    number: int = 1
    while True:
        new_name: str = f"{name} ({number}).{extension}"
        new_path: str = os.path.join(folder_path, new_name)

        if not os.path.exists(new_path):
            return new_path

        number += 1


def move_folder(folder: str, current_path: str):
    """Move the folder to the super folder"""

    if folder in SUB_FOLDERS:
        return

    super_folder_path: str = os.path.join(FOLDER_PATH, "Super Folder")
    new_path: str = os.path.join(super_folder_path, folder)
    os.rename(current_path, new_path)


def move_file(_file: str, current_path: str):
    """Move the file to the appropriate folder"""

    split_name: list = _file.split(".")
    extension: str = split_name.pop(-1).lower()
    name: str = "".join([str(x) for x in split_name])

    extension_exists: bool = False

    for folder, extensions in SUB_FOLDERS.items():
        if extension not in extensions:
            continue

        extension_exists = True

        folder_path: str = os.path.join(FOLDER_PATH, folder)
        new_path: str = os.path.join(folder_path, _file)

        try:
            os.rename(current_path, new_path)
        except FileExistsError:
            new_path = rename_exists(name, extension, folder_path)
            os.rename(current_path, new_path)

    if not extension_exists:
        return extension
    return None


def add_unknown_extensions(extensions: list):
    """Add extensions that don't exist in the JSON file"""

    sub_folders: dict = SUB_FOLDERS.copy()

    print(f"Folders: {list(sub_folders.keys())}")
    print(
        "Please input the correct folders for the following unknown extensions. \
          (use ! create a new folder, e.g. !name)"
    )

    for extension in extensions:
        folder_name: str = input(f"{extension} :: ")

        if "!" in folder_name:
            folder_name = folder_name.replace("!", "")
            sub_folders[folder_name] = []

        sub_folders[folder_name].append(extension)

    with open("folders.json", "w", encoding="utf-8") as jsonfile:
        jsonfile.write(json.dumps(sub_folders, indent=4))

    create_folders(sub_folders)


def sort_folder():
    """Sort the folder"""

    unknown_extensions: list = []

    for item in os.listdir(FOLDER_PATH):
        item_path: str = os.path.join(FOLDER_PATH, item)

        if not os.path.isfile(item_path):
            move_folder(item, item_path)
            continue

        output = move_file(item, item_path)
        if output is not None:
            unknown_extensions.append(output)

    return unknown_extensions


def run_sorter():
    """Run the Folder Sorter"""

    while True:
        unknown_extensions: list = sort_folder()

        if not unknown_extensions:
            break

        add_unknown_extensions(unknown_extensions)


if __name__ == "__main__":
    create_folders(SUB_FOLDERS)
    run_sorter()
