from pathlib import Path
from datetime import datetime
import os
import json
import hashlib
import shutil

class SyncHandler:
    src_folder = Path.cwd()
    dst_folder = Path.cwd()
    
    file_hash_src = []
    
    def __init__(self) -> None:
        self._load_configs()
        self.main_loop()
        pass
    
    def main_loop(self):
        while(True):
            print("[0] - exit")
            print("[1] - list files")
            print("[2] - compare files")
            print("[3] - copy files to destination")
            print("[4] - copy files and backup old ones")
            
            my_choice = int(input("Choose [0-3]: "))
            
            match my_choice:
                case 0:
                    break
                case 1:
                    self.list_files()
                case 2:
                    self.compare_files()
                case 3:
                    self.copy_files_to_dest()
                case 4:
                    self.copy_and_backup()
                case _:
                    print("ERROR: wrong number chosen!")
                    
                    
            print("===============\n\n")
    
    def _load_configs(self):
        try:
            with open("configs.json", "rb") as file_config:
                configs = json.load(file_config)
                print(configs)
                self._load_to_internals(configs)
                
        except FileNotFoundError:
            print("DEBUG: config file was not created yet!")
            print("INFO: creating new config file.")
            
            new_src_location = input("Please set new SOURCE folder location (default CWD): ")
            new_dst_location = input("Please set new DESTINATION folder location (default CWD): ")
            
            configs = {}
            
            if new_src_location != "":
                configs["src_folder"] = str(Path(new_src_location))
                self.src_folder = Path(new_src_location)
            else:
                configs["src_folder"] = str(self.src_folder)
            
            if new_dst_location != "":
                configs["dst_folder"] = str(Path(new_dst_location))
                self.dst_folder = Path(new_dst_location)
            else:
                configs["dst_folder"] = str(self.dst_folder)
            
            print(json.dumps(configs, indent=4))
            with open("configs.json", "w") as file_config:
                json.dump(configs, file_config)
                print("INFO: file config was created and saved!")
                
    def _load_to_internals(self, config: dict):
        self.src_folder = Path(config['src_folder'])
        self.dst_folder = Path(config['dst_folder'])
            
    def list_files(self):
        for file in self.src_folder.iterdir():
            print(file.name)
            
            # file_current = open(file)
            file_hash = hashlib.sha1(file.read_bytes())
            print(file_hash)
            print(file_hash.hexdigest())
            print("--------")
            print(os.stat(file))
            
    def compare_files(self):
        file_list_src = []
        file_hash_src = {}
        
        file_list_dst = []
        file_hash_dst = {}
        
        for file in self.src_folder.iterdir():
            file_list_src.append(file)
            file_hash_src[file.name] = hashlib.md5(file.read_bytes())
            
        for file in self.dst_folder.iterdir():
            file_list_dst.append(file)
            file_hash_dst[file.name] = hashlib.md5(file.read_bytes())
            
        print("{0: <20} | {1: >32} | MATCH | {2: >32}".format("FILE NAME", "SOURCE HASH", "DEST HASH"))
        
        for el in file_list_src:
            matches = set(str(file_list_dst)).intersection(str(el))
            if len(matches) == 0:
                print("{0: <20} | {1: >32} | {3: ^5} | {2: >32}".format(str(el.name), file_hash_src[el.name].hexdigest(), "No file here!", "!="))
            else:
                if_hash_equal = True if file_hash_src[el.name].digest() == file_hash_dst[el.name].digest() else False
                print("{0: <20} | {1: >32} | {3: =5} | {2: >32}".format(str(el.name), file_hash_src[el.name].hexdigest(), file_hash_dst[el.name].hexdigest(), if_hash_equal))
            
    def copy_files_to_dest(self):
        for file in self.src_folder.iterdir():
            path_dst = Path(self.dst_folder, file.name)
            
            file_dest = open(path_dst, "wb")
            file_orig = open(file, "rb")
            
            shutil.copyfileobj(file_orig, file_dest)
            
            file_orig.close()
            file_dest.close()
            print("INFO: copied file:", file.name)
    
    def copy_and_backup(self):
        for file in self.src_folder.iterdir():
            path_dst = Path(self.dst_folder, file.name)
            if path_dst.exists():
                os.replace(path_dst, Path(self.dst_folder, file.name + ".{}.bak".format(datetime.today().strftime('%H%M%S_%d%m%Y'))))
            
            file_dest = open(path_dst, "wb")
            file_orig = open(file, "rb")
            
            shutil.copyfileobj(file_orig, file_dest)
            
            file_orig.close()
            file_dest.close()
            print("INFO: copied and backed-up file:", file.name)
            
# ------------------

my_handler = SyncHandler()