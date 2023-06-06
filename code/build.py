import os
import pathlib
import sys
import secrets
import json
import shutil

# import PyInstaller.__main__ as pyi

ICON = "logo.ico"

OPTIONS = [
    '--onefile',  # Kompiliere in eine einzige ausführbare Datei
    f'--icon={ICON}',
    '--distpath', '.'  # Speichere die kompilierte Datei im aktuellen Ordner
]


class AnkiError:
    class ProjectNotFoundError(Exception):
        def __init__(self, reason: str = "Could not find project"):
            super().__init__(reason)
    
    class UnknownError(Exception):
        def __init__(self, reason: str = "An unknown error oncured"):
            super().__init__(reason)
    

def start(project_name: str):
    PROJECT = project_name
    PATH = pathlib.Path(__file__).parent
    FILES = f"{PATH}/{PROJECT}"
    return PROJECT, PATH, FILES
        
class build_file():
    def __init__(self, PROJECT, PATH, FILE) -> None:
        self.PROJECT, self.PATH, self.FILE = PROJECT, PATH, FILE
        self.options: list = OPTIONS
        
        with open("anki.json", "r") as file:
            self.compiler = json.load(file)
            
        with open(FILE, "r") as file:
            self.text = file.read()
            self.text = self.readCode(self.text)
            
        self.token = secrets.token_hex(8)
        with open(f"{self.token}.py", "w") as file:
            file.write(self.text)
        
    
        if "tkinter" in self.text:
            self.options.insert(0, "--windowed")
            
        print(self.options)
        self.compile(self.token)
            
    
    def compile(self, token: str):
        filename = f"{token}.py"
        options = " ".join([*OPTIONS, filename])
        os.system(f"pyinstaller {options}")
        # pyi.run([*OPTIONS, filename])
        self.clean_up(token)
        
    def clean_up(self, token):
        shutil.rmtree("build")
        os.remove(f"{token}.spec")
        os.remove(f"{token}.py")
        os.rename(f"{token}.exe", "build.exe")
        
    def readCode(self, text: str):
        for word, replace in self.compiler.items():
            start_index = 0
            while True:
                word_index = text.find(word, start_index)
                if word_index == -1:
                    break

                in_quotes = False
                quote_count = 0
                for i in range(0, word_index):
                    if text[i] == '"' or text[i] == "'":
                        quote_count += 1

                if quote_count % 2 != 0:
                    in_quotes = True

                if not in_quotes:
                    text = text[:word_index] + replace + text[word_index+len(word):]
                    start_index = word_index + len(replace)
                else:
                    start_index = word_index + 1

        return text
    
PROJECT, PATH, FILES = None, None, None

if "-f" in sys.argv:
    FILES = sys.argv[sys.argv.index("-f") + 1]
    PROJECT = FILES
    PATH = pathlib.Path(__file__).parent
elif "-p" in sys.argv:
    PROJECT, PATH, FILES = start(sys.argv[sys.argv.index("-p") + 1])
else:
    FILES = sys.argv[1]
    PROJECT = FILES
    PATH = pathlib.Path(__file__).parent
    

if not os.path.exists(FILES):
    raise AnkiError.ProjectNotFoundError(f"Could not find project '{PROJECT}' at '{PATH}'")
elif os.path.isfile(FILES):
    a = build_file(PROJECT, PATH, FILES)
elif os.path.isdir(FILES):
    raise NotImplementedError("Build project not finished yet")
    # a = build_project(PROJECT, PATH, FILES)
else:
    raise AnkiError.UnknownError()