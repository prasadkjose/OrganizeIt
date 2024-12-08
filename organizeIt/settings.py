# settings.py - Configuration for organizeIt project

from pathlib import Path
import os
import logging

# setup configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

# The project root path
ROOT_DIR = Path(__file__).resolve().parent

# The path to the configs directory
CONFIG_DIR = os.path.join(ROOT_DIR, "configs")