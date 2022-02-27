import cv2


def expose_image(img, value=30):        
        for x in range(0, img.shape[0]):
            for y in range(0, img.shape[1]):
                img[x, y] = max(img[x, y] * value, 255)
        
        return img
    
def add_brightness_and_contrast(img, brightness: int, contrast: int):
    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            img[x, y] = max(min(img[x, y] * contrast + brightness, 255), 0)
    
    return img

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def threshold_2_row(img, threshold_1: int, threshold_2: int):
    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            if img[x,y] < threshold_1:
                img[x,y] = 0
            elif img[x,y] < threshold_2:
                img[x,y] = 122
            else:
                img[x,y] = 255
    return img
