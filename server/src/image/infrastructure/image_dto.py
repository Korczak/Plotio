from src.image.domain.image import ImageAttributes


class ImageDto:
    def __init__(self, name: str, content: str, orig_content: str, attributes: ImageAttributes) -> None:
        self.name = name
        self.content = content
        self.orig_content = orig_content
        self.attributes = attributes