"""setup file for anki-sdk

Raises:
    ImportDisabled: Dont import this file
    
"""
import os
import sys
import requests
from pathlib import Path
import zipfile

args = [arg.lower() for arg in sys.argv]

UPDATE_PACKAGE = "--update" in args
UPGRADE_PACKAGE = "--upgrade" in args

def getPath():
    main = Path(__file__).resolve().parent
    return main

path = getPath()

def main():
    """Main function for default setup

    Returns:
        car_list (list): list with car address
    """
    with open(f"{path}/files/requirements.txt", "r",  encoding="utf-8") as file:
        for index in file.readlines():
            print(f"Installing {index}")
            os.system(f"pip install {index}")
            print(f"Installed {index}")

    active = ""
    while not active:
        active = input("Search only for active vehicles? (Y/N) ")
        active = active.lower()
        scan = False
        if active == "y":
            scan = True
        elif active == "n":
            scan = False
        else:
            active = ""
    import anki_sdk.utils as util
    car_list: list = util.scanner(scan)
    return car_list

def increment_version(version: str):
    """_summary_

    Args:
        version (str): old version

    Returns:
        str: New version
    """
    major, minor, patch = version.split('.')
    
    if patch == '9':
        minor = str(int(minor) + 1)
        patch = '1'
    else:
        patch = str(int(patch) + 1)
        
    if minor == "10":
        major = str(int(major) + 1)
        patch = "1"
        minor = "0"
        
    
    return '.'.join([major, minor, patch])




def update(install: bool):
    """Update the package"""
    import anki_sdk as sdk
    current_version: str = sdk.all_data["data"]["version"]
    version: str = increment_version(current_version)
    link: str = str(sdk.all_data["extra"]["download"])
    link = link.replace("[VERSION]", str(version))
    
    if link:
        data = requests.get(link)
        if data.text == "404: Not Found":
            raise NotImplementedError("No update available")
        
        if not os.path.exists(f"{path}/update"): 
            os.mkdir("update")

        print("Downloading...")
        
        with open(f"{path}/update/Stable-{version}.zip", "wb") as file:
            file.write(data.content)
            
        with zipfile.ZipFile(f"{path}/update/Stable-{version}.zip","r") as zip_ref:
            zip_ref.extractall(f"{path}/update")
                
        os.remove(f"{path}/update/Stable-{version}.zip")
        if os.path.exists(f"{path}/update/Stable-{version}"):
            os.remove(f"{path}/update/Stable-{version}")
            
            
        os.rename(f"{path}/update/anki-overdrive-windows-sdk-Stable-{version}", f"{path}/update/Stable-{version}")
                    
        if install:
            Upgrade(f"{path}/update/Stable-{version}")
    else:
        raise NotImplementedError("No update available")
        
        
def Upgrade(directory: str = path):
    """Upgrade anki sdk

    Args:
        directory (str): Directory with new files_. Defaults to path.
    """
    print("Upgrading...")
    try:
        os.system(f"python {directory}/debug.py")
    except Exception as e:
        print("Error: ", e)
      
if __name__ == "__main__":
    if not UPDATE_PACKAGE:
        if not os.path.exists("address.list"):
            open(f"{path}/files/address.list", "x")
        else:
            with open(f"{path}/files/address.list", "w", encoding="utf-8") as f:
                f.write("")
            
                
        with open(f"{path}/files/address.list", "a", encoding="utf-8") as f:
            for i in main():
                f.write(f"Address: {i}\n")
    else:
        update(UPGRADE_PACKAGE)
else:
    from anki_sdk.exceptions import ImportDisabled
    raise ImportDisabled("Only for setup dont import this file")
