import enum
from typing import List, Optional
from base64 import urlsafe_b64decode, b64decode, b64encode
import numpy as np
import cv2

class Image:
    def __init__(self, name: str, content: str) -> None:
        self.name = name
        self.content = content        
        b64 = urlsafe_b64decode(str(content)); 
        npimg = np.fromstring(b64, dtype=np.uint8); 
        self.img = cv2.imdecode(npimg, 0)

    def is_binary(self) -> bool:
        colors = {};
        for x in range(0, self.img.shape[0]):
            for y in range(0, self.img.shape[1]):
                if(self.img[x, y] not in colors):
                    colors[self.img[x, y]] = 1

        if(len(colors.keys()) == 2):
            return True

        return False


    def is_size_ok(self, width_max, height_max) -> bool:
        if(self.img.shape[0] > width_max and self.img.shape[1] > height_max):
            return False
        return True

