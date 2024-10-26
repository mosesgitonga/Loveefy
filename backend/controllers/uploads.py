import os
import uuid
from datetime import datetime
from PIL import Image
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import logging

from models.engine.DBStorage import DbStorage
from models.uploads import Upload  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'uploads'

def serialize_upload(upload):
    return {
        "id": upload.id, 
        "user_id": upload.user_id,
        "image_path": upload.image_path,
        "is_primary": upload.is_primary,
    }
class UploadHandler():
    def __init__(self):
        self.storage = DbStorage()
        self.ALLOWED_EXTENSIONS = {
            'png', 'jpeg', 'jpg', 'gif', 'webp', 'svg', 'bmp', 'tiff', 'ico',
            'heic', 'heif', 'avif'
        }

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def get_user_directory(self, user_id) -> str:
        current_time = datetime.now()
        year_month = current_time.strftime("%Y_%m")
        dir_path = os.path.join(UPLOAD_FOLDER, year_month, str(user_id))
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def create_thumbnail(self, image_path, thumbnail_path, size=(150, 150), quality=95) -> None:
        try:
            with Image.open(image_path) as img:
                img.thumbnail(size)
                img.save(thumbnail_path, "WEBP", quality=quality)
        except Exception as e:
            logger.error(f"Failed to create thumbnail for {image_path}: {str(e)}")
            raise

    def is_directory_empty(self, directory) -> bool:
        return not any(os.scandir(directory))

    @jwt_required()
    def upload_image(self):
        user_id = get_jwt_identity()
        if request.method == 'POST':
            try:
                if 'file' not in request.files:
                    return jsonify({"message": "No file part"}), 400

                file = request.files['file']
                if file.filename == '':
                    return jsonify({"message": "No selected file"}), 400

                if not self.allowed_file(file.filename):
                    return jsonify({"message": "File type not allowed"}), 400

                filename = secure_filename(file.filename)
                user_dir = self.get_user_directory(user_id)

                # Save the original file temporarily
                temp_path = os.path.join(user_dir, 'temp_' + filename)
                file.save(temp_path)

                # Generate a unique filename for the thumbnail
                thumbnail_filename = str(uuid.uuid4()) + ".webp"
                thumbnail_path = os.path.join(user_dir, thumbnail_filename)

                self.create_thumbnail(temp_path, thumbnail_path, size=(300, 300), quality=100)

                # Calculate thumbnail size
                thumbnail_size_in_mb = os.path.getsize(thumbnail_path) / (1024 * 1024)

                # Removing the temporary file
                os.remove(temp_path)

                existing_primary = self.storage.get(Upload, user_id=user_id, is_primary=True)

                # If a primary exists, set it to False (demote it)
                if existing_primary:
                    existing_primary.is_primary = False
                    self.storage.new(existing_primary)
                    self.storage.save() 

                is_primary = True

                #extract image path that will work on react public dir
                current_time = datetime.now()
                year_month = current_time.strftime("%Y_%m")
                image_path = f"/{year_month}/{user_id}/{thumbnail_filename}"


                new_upload = Upload(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    image_path=image_path,
                    is_primary=is_primary,
                    file_size=thumbnail_size_in_mb
                )

                # Save to database using storage class
                self.storage.new(new_upload)
                self.storage.save()

                return jsonify({"thumbnail_path": thumbnail_path, "message": "Image uploaded successfully"}), 200
            except Exception as e:
                logger.error(f"An error occurred while processing the file: {str(e)}")
                return jsonify({"message": "An error occurred while processing the file", "error": str(e)}), 500

    def view_user_gallery(self, data):
        user_id = getattr(data, 'userId', None)  

        if not user_id:
            return jsonify({"message": "Invalid or missing userId"}), 400  

        try:
            images = self.storage.get_all(Upload, user_id=user_id)
            if not images:
                return jsonify({"message": "No images found", "data": []}), 404

            serialized_images = [serialize_upload(upload) for upload in images]
            
            return jsonify(serialized_images), 200  
        except Exception as e:
            print(f"Error retrieving images for user {user_id}: {e}")
            return jsonify({"message": "Internal Server Error"}), 500