import os
from PIL import ImageFile

from django.core.exceptions import ValidationError

def validate_file_hook(file):
    valid_file_extensions = ['.mp4, .png, .jpg, .gif, .jpeg']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')