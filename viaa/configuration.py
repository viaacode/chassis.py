import os
import sys
import yaml

class ConfigParser():
    path = sys.path.append(os.getcwd())
    
    config = {}
    def __init__(self):
        cfg = {}
        # Take config from commandline arguments
        # Take config from environment variables
        # Take config from the user's config file
        if os.path.isfile(os.getcwd() + "/config.yml"):
            with open(os.getcwd() + "/config.yml", "r") as ymlfile:
                cfg: dict = yaml.load(ymlfile, Loader=yaml.FullLoader)
        # Fallback to default
        else:
            cfg = {"viaa":{"logging": {"level": 20}}}
            
        if "viaa" in cfg:    
            self.config = cfg["viaa"]
    