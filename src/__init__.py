import os

from src.resources.config import config_dict

config = config_dict[os.getenv("ENVIRONMENT_KEY")]
