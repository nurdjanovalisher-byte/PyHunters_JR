from enum import Enum
import os



class Path(Enum):
    PROMPTS = os.path.join('resources', 'prompts')
    IMAGES_DIR = os.path.join('resources', 'images')
    MESSAGES = os.path.join('resources', 'messages')
    IMAGES = os.path.join('resources', 'images', '{file}.jpg')
