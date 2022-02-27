from base64 import urlsafe_b64decode
import enum
import cv2
import numpy as np

from numpy import number
from sqlalchemy import null
from src.image.domain.image_dither_algorithms import *

from src.image.domain.image_processing import *
from PIL import Image, ImageEnhance
import PIL
class HistogramEqualizationType(str, enum.Enum):
    Empty = "Brak",
    Equalization = "Equalization",
    CLAHE = "CLAHE",
class DitherAlgorithmType(str, enum.Enum):
    Empty = "Brak",
    FloydSteinberg = "Floyd-Steinberg",
    FalseFloydSteinberg = "False Floyd-Steinberg",
    Stucki = "Stucki",
    Sierra = "Sierra",
    SierraLite = "Sierra lite",
    Sierra2Rows = "Sierra 2-rows",
    Threshold = "Threshold",
    Threshold2Rows = "Threshold 2-rows"
    
class Threshold2Row:
    def __init__(self, min: int, max: int):
        self.min: int = min
        self.max: int = max
    
class ImageAttributes:
    def __init__(self, shadow: number, contrast: number, brightness: number, sharpness: number, highlights: number, exposition: number, ditherAlgorithm: DitherAlgorithmType, histogramType: HistogramEqualizationType, threshold: int = null, threshold2Row: Threshold2Row = null) -> None:
        self.shadow: int = shadow
        self.contrast: int = contrast
        self.brightness: int = brightness
        self.sharpness: int = sharpness
        self.highlights: int = highlights
        self.exposition: int = exposition
        self.ditherAlgorithm: DitherAlgorithmType = ditherAlgorithm
        self.histogramEqualization: HistogramEqualizationType = histogramType
        self.threshold: int = threshold
        self.threshold2Row: Threshold2Row = threshold2Row
    

class Image:
    def __init__(self, name: str, content: str, orig_content: str, attributes: ImageAttributes) -> None:
        self.name = name
        self.image = self.parse_to_cv(content)
        self.original_image = self.parse_to_cv(orig_content)
        self.image_attributes = attributes
        
    def change_image_attributes(self, attributes: ImageAttributes):
        self.image_attributes = attributes
        exposition = self.image_attributes.exposition
        contrast = self._calculate_contrast(self.image_attributes.contrast) 
        brightness = self._calculate_brightness(self.image_attributes.brightness)
        sharpness = self._calculate_sharpness(self.image_attributes.sharpness)
        image = self.original_image.copy()
        #image = expose_image(image, exposition)
        
        image = PIL.Image.fromarray(image)
        image = ImageEnhance.Brightness(image).enhance(brightness)
        image = ImageEnhance.Contrast(image).enhance(contrast)
        image = ImageEnhance.Sharpness(image).enhance(sharpness)
        image = np.asarray(image)
        
        if self.image_attributes.histogramEqualization == HistogramEqualizationType.Equalization:
            image = cv2.equalizeHist(image)
        elif self.image_attributes.histogramEqualization == HistogramEqualizationType.CLAHE:
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            image = clahe.apply(image)
        
        
        if(self.image_attributes.ditherAlgorithm == DitherAlgorithmType.Threshold):
            _, image = cv2.threshold(image, self.image_attributes.threshold, 255, cv2.THRESH_BINARY)
        elif(self.image_attributes.ditherAlgorithm == DitherAlgorithmType.Threshold2Rows):
            image = threshold_2_row(image, self.image_attributes.threshold2Row.min, self.image_attributes.threshold2Row.max)
        elif(self.image_attributes.ditherAlgorithm == DitherAlgorithmType.FalseFloydSteinberg):
            image = false_floyd(image)
        elif(self.image_attributes.ditherAlgorithm == DitherAlgorithmType.FloydSteinberg):
            image = floyd(image, 1)
        elif(self.image_attributes.ditherAlgorithm == DitherAlgorithmType.Sierra):
            image = sierra(image)
        elif(self.image_attributes.ditherAlgorithm == DitherAlgorithmType.Sierra2Rows):
            image = sierratworow(image)
        elif(self.image_attributes.ditherAlgorithm == DitherAlgorithmType.SierraLite):
            image = sierralite(image, 1)
        elif(self.image_attributes.ditherAlgorithm == DitherAlgorithmType.Stucki):
            image = stucki(image)
            
        self.image = image
        
    def parse_to_cv(self, text: str):
        b64 = urlsafe_b64decode(str(text)); 
        npimg = np.fromstring(b64, dtype=np.uint8); 
        return cv2.imdecode(npimg, 0)

    #input contrast is [-100, 100], contrast for processing is [0, 4], where 1 is default value
    def _calculate_contrast(self, contrast):
        if contrast < 0:
            return 1 + contrast / 100
        
        return contrast/100*3 + 1
    
    #input brightness is [-100, 100], contrast for processing is [0, 2], where 1 is default value
    def _calculate_brightness(self, brightness):       
        return brightness/100 + 1
        
    #input contrast is [-100, 100], contrast for processing is [-20, 20], where 0 is default value
    def _calculate_sharpness(self, factor):
        return factor/5
        
    #input contrast is [-100, 100], contrast for processing is [0, 5], where 1 is default value
    def _calculate_pil_factor(self, factor):
        if factor < 0:
            return 1 + factor / 100
        
        return factor/100*4 + 1
        
        