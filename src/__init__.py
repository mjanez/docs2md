import os
import yaml

def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

# Define the base directory relative to the repository root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
