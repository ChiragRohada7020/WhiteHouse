from flask import Blueprint
import os

products_bp = Blueprint('products', __name__)

from . import routes



products_upload_folder = 'static/uploads'

# Ensure the upload folder exists
os.makedirs(products_upload_folder, exist_ok=True)
products_bp.config = {
    'UPLOAD_FOLDER': products_upload_folder
}
  # Create a folder named 'uploads' in your project directory

