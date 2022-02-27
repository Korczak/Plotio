from enum import Enum
from src.events.image_added import ImageAdded
from src.image.domain.image import DitherAlgorithmType, HistogramEqualizationType, ImageAttributes, Threshold2Row
from src.image.infrastructure.image_repository import ImageRepository
from pydantic import BaseModel
from pubsub import pub

class Threshold2RowInput(BaseModel):
    threshold_1: int
    threshold_2: int
    

class ImageAttributeInput(BaseModel):
    shadow: int
    contrast: int
    brightness: int
    sharpness: int
    highlights: int
    exposition: int
    ditherAlgorithm: DitherAlgorithmType
    histogramType: HistogramEqualizationType 
    threshold: int
    threshold2Row: Threshold2RowInput
    

class EditImageService:
    def __init__(self, repository: ImageRepository) -> None:
        self.image_repository: ImageRepository = repository

    def edit_image_attributes(self, attributes: ImageAttributeInput):
        image = self.image_repository.get_image()
        if image == None:
            return
        
        image_attributes = ImageAttributes(
            attributes.shadow, 
            attributes.contrast, 
            attributes.brightness, 
            attributes.sharpness, 
            attributes.highlights, 
            attributes.exposition, 
            attributes.ditherAlgorithm, 
            attributes.histogramType, 
            attributes.threshold, 
            Threshold2Row(attributes.threshold2Row.threshold_1, attributes.threshold2Row.threshold_2)
        )
           
        image.change_image_attributes(image_attributes)
        self.image_repository.update_image(image)

    def approve_image(self):
        image = self.image_repository.get_image()
        pub.sendMessage("ImageAdded", arg1=ImageAdded(image.name, image.image))