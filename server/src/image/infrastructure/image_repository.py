from typing import List
from src.image.domain.image import Image
from src.image.infrastructure.image_dto import ImageDto


class ImageRepository:
    
    def __init__(self) -> None:
        self._image_db: List[ImageDto] = []

    def add_image(self, image: Image):
        imageDto = ImageDto(image.name, image.content)

        self._image_db.append(imageDto)
        
    def get_image(self, name: str):
        return [image for image in self._image_db if image.name == name]
