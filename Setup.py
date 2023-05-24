import os
from anki_sdk.exceptions import *

def main():
    with open("requirements.txt", "r") as f:
        for i in f.readlines():
            print(f"Installing {i}")
            os.system(f"pip install {i}")
            print(f"Installed {i}")

    active = input("Search only for active vehicles? (Y/N) ")
    if active.lower() == "y":
        active = True
    else:
        active = False

    import anki_sdk.utils as utils
    return utils.scanner(active)

if __name__ == "__main__":
    open("address.list", "x")
    with open("address.list", "a") as f:
        for i in main():
            f.write(f"Address: {i}")
else:
    raise ImportDisabled("Only for setup dont import this file")
