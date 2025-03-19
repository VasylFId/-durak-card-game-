# app/utils.py
import os
import secrets
from PIL import Image
from flask import current_app

def save_picture(form_picture):
    """
    Save and resize a profile picture uploaded through the form.
    
    Args:
        form_picture: The uploaded file object from the form
        
    Returns:
        str: The filename of the saved picture
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img', picture_fn)
    
    # Resize image
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn