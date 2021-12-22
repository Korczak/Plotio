from pymitter import EventEmitter
from src.events.image_added import ImageAdded
from src.image.infrastructure.image_repository import ImageRepository
from src.image.domain.image import Image
from pydantic import BaseModel
from pubsub import pub


class AddImageInput(BaseModel):
    name: str
    content: str

class AddImageService:
    def __init__(self, repository: ImageRepository) -> None:
        self.image_repository: ImageRepository = repository

    def add_image(self, new_image: AddImageInput):
        base64Image = new_image.content.split(',')
        image = Image(new_image.name, base64Image[len(base64Image) - 1])

        self.image_repository.add_image(image)
        pub.sendMessage("ImageAdded", arg1=ImageAdded(image.name, image.content))



