from pymitter import EventEmitter
from src.events.image_added import ImageAdded
from src.image.infrastructure.image_repository import ImageRepository
from src.image.domain.image import Image
from pydantic import BaseModel
from pubsub import pub
from enum import Enum



class AddImageResult(str, Enum):
    Added = "Added",
    ImageNotBinaryError = "ImageNotBinaryError",
    ImageTooBigError = "ImageTooBigError"

class AddImageInput(BaseModel):
    name: str
    content: str

class AddImageService:
    def __init__(self, repository: ImageRepository) -> None:
        self.image_repository: ImageRepository = repository

    def add_image(self, new_image: AddImageInput):
        base64Image = new_image.content.split(',')
        image = Image(new_image.name, base64Image[len(base64Image) - 1])

        if not image.is_binary():
            return AddImageResult.ImageNotBinaryError

        if not image.is_size_ok(400, 500):
            return AddImageResult.ImageTooBigError
        self.image_repository.add_image(image)
        pub.sendMessage("ImageAdded", arg1=ImageAdded(image.name, image.content))
        return AddImageResult.Added



