import os
import json
import requests
import base64
from pathlib import Path

# F8:21:8E:B8:E0:85

# GitHub-Zugriffstoken
access_token = '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'
blacklist = ["desktop.ini", "Upload.py", "tmp.py", "address.list", "log.txt"]

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


# Repository-Informationen
folder_path = Path(__file__).resolve().parent
version = ""
data = ""
with open(f"{folder_path}/files/metadata.json", "r", encoding="utf-8") as file:
    data = json.loads(file.read())
    
version = increment_version(data["data"]["version"])
data["data"]["version"] = version

with open(f"{folder_path}/files/metadata.json", "w", encoding="utf-8") as file:
    data = json.dumps(data, indent=4)
    file.write(data)
    
repository_owner = 'jtg-code'
repository_name = 'anki-overdrive-windows-sdk'
branch_name = f'Stable-{version}'

# Pfad zum Ordner mit den Dateien, die hochgeladen werden sollen



def create_branch():
    url = f'https://api.github.com/repos/{repository_owner}/{repository_name}/git/refs'
    headers = {'Authorization': f'token {access_token}'}
    payload = {
        'ref': f'refs/heads/{branch_name}',
        'sha': get_default_branch_sha()
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f'Branch "{branch_name}" wurde erfolgreich erstellt.')
    else:
        print(f'Fehler beim Erstellen des Branches. Statuscode: {response.status_code}')

def get_default_branch_sha():
    url = f'https://api.github.com/repos/{repository_owner}/{repository_name}/branches'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        branches = response.json()
        default_branch = next(branch for branch in branches if branch['name'] == 'empty')  # Ändere 'main' zu deinem Standard-Branch-Namen
        return default_branch['commit']['sha']
    else:
        print(f'Fehler beim Abrufen des Standard-Branches. Statuscode: {response.status_code}')

def upload_files():
    base_url = f'https://api.github.com/repos/{repository_owner}/{repository_name}/contents'
    headers = {'Authorization': f'token {access_token}'}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                file_name = os.path.basename(file_path)
                if file_name.endswith(".pyc"):
                    continue
                content = f.read()
                content = content.decode("utf-8")
                encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
                relative_path = os.path.relpath(file_path, folder_path)
                file_directory = os.path.dirname(relative_path)
                
                if file_name in blacklist:
                    continue
                
                if file_directory:
                    payload = {
                        'path': file_directory + '/' + file_name,
                        'branch': branch_name,
                        'message': f'Upload von {file}',
                        'content': encoded_content
                    }
                    response = requests.put(f'{base_url}/{file_directory}/{file_name}', headers=headers, json=payload)
                else:
                    payload = {
                        'path': file_name,
                        'branch': branch_name,
                        'message': f'Upload von {file}',
                        'content': encoded_content
                    }
                    response = requests.put(f'{base_url}/{file_name}', headers=headers, json=payload)

                if response.status_code == 201:
                    print(f'Datei "{file}" erfolgreich hochgeladen.')
                else:
                    print(f'Fehler beim Hochladen der Datei "{file}". Statuscode: {response.status_code}')
                    
                    
def merge_branches():
    url = f'https://api.github.com/repos/{repository_owner}/{repository_name}/merges'
    headers = {'Authorization': f'token {access_token}'}
    payload = {
        'base': 'main',
        'head': branch_name,
        'commit_message': f'Merge {branch_name} into main'
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f'Branch "{branch_name}" wurde erfolgreich in main gemerged.')
    elif response.status_code == 409:
        print(f'Konflikt beim Mergen des Branches {branch_name} in main. Konflikte müssen manuell gelöst werden.')
    else:
        print(f'Fehler beim Mergen des Branches in main. Statuscode: {response.status_code}')


# Hauptprogramm
if __name__ == "__main__":
    create_branch()
    upload_files()
    merge_branches()

