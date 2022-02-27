import base64
from typing import List

import cv2
from src.image.domain.image import Image
from src.image.infrastructure.image_dto import ImageDto


class ImageRepository:
    
    def __init__(self) -> None:
        self._image_db: ImageDto = None

    def add_image(self, image: Image):
        content_str = base64.b64encode(cv2.imencode('.jpg', image.image)[1]).decode()
        original_content_str = base64.b64encode(cv2.imencode('.jpg', image.original_image)[1]).decode()
        imageDto = ImageDto(image.name, content_str, original_content_str, image.image_attributes)

        self._image_db = imageDto
        
    def update_image(self, image: Image):
        content_str = base64.b64encode(cv2.imencode('.jpg', image.image)[1]).decode()
        original_content_str = base64.b64encode(cv2.imencode('.jpg', image.original_image)[1]).decode()
        
        imageDto = ImageDto(image.name, content_str, self._image_db.orig_content, image.image_attributes)

        self._image_db = imageDto
        
    def get_image(self) -> Image:
        if(self._image_db == None):
            return None
        return Image(self._image_db.name, self._image_db.content, self._image_db.orig_content, self._image_db.attributes)

