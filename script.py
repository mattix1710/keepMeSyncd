from pathlib import Path
import os
import json
import hashlib

class SyncHandler:
    src_folder = Path.cwd()
    dst_folder = Path.cwd()
    
    file_hash_src = []
    
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
            
# ------------------

my_handler = SyncHandler()

my_handler._load_configs()

my_handler.list_files()

my_handler.compare_files()