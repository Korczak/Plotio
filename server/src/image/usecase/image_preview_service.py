import base64

import cv2
from src.image.infrastructure.image_repository import ImageRepository
    

class ImagePreviewService:
    def __init__(self, repository: ImageRepository) -> None:
        self.image_repository: ImageRepository = repository

    def get_image(self):
        image = self.image_repository.get_image()
        if image == None:
            return
        content_str = base64.b64encode(cv2.imencode('.jpg', image.image)[1]).decode()
        return content_str