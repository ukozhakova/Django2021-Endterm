import os
from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = ['.jpg', '.png', 'jpeg']

ALLOWED_IMAGE_SIZE = 40000

def validate_size(value):                   #validator 1
    if value.size > ALLOWED_IMAGE_SIZE:
        raise ValidationError(f'Maximum allowed image size is : {ALLOWED_IMAGE_SIZE}')

def validate_extension(value):              #validator 2
    split_ext = os.path.splitext(value.name)
    if len(split_ext) > 1:
        ext = split_ext[1]
        if ext.lower() not in ALLOWED_EXTENSIONS:
            raise ValidationError(f'Please, choose another file with allowed extension: {ALLOWED_EXTENSIONS}')