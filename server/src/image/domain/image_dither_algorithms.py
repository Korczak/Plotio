import cv2
import numpy as np

def minmax(v):
    if v > 255:
        v = 255
    if v < 0:
        v = 0
    return v

def hist_eq(im):
	clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
	cl1 = clahe.apply(im)
	return cl1
def set_pixel(im,x,y,new):
	im[x,y]=new

def stucki(im):   # stucki algorithm for image dithering
	w8= 8/42.0;
	w4= 4/42.0;
	w2= 2/42.0;
	w1= 1/42.0;
	width,height=im.shape
	for y in range(0,height-2):
		for x in range(0,width-2):
			old_pixel=im[x,y]
			if old_pixel<127:
				new_pixel=0
			else:
				new_pixel=255	
			set_pixel(im,x,y,new_pixel)
			quant_err=old_pixel-new_pixel
			set_pixel(im,x+1,y, im[x+1,y] + w8 * quant_err);
			set_pixel(im,x+2,y, im[x+2,y]+ w4 * quant_err);
			set_pixel(im,x-2,y+1, im[x-2,y+1] + w2 * quant_err);
			set_pixel(im,x-1,y+1, im[x-1,y+1] + w4 * quant_err);
			set_pixel(im,x,y+1, im[x,y+1] + w8 * quant_err);
			set_pixel(im,x+1,y+1, im[x+1,y+1] + w4 * quant_err);
			set_pixel(im,x+2,y+1, im[x+2,y+1] + w2 * quant_err);
			set_pixel(im,x-2,y+2, im[x-2,y+2] + w1 * quant_err);
			set_pixel(im,x-1,y+2, im[x-1,y+2] + w2 * quant_err);
			set_pixel(im,x,y+2, im[x,y+2] + w4 * quant_err);
			set_pixel(im,x+1,y+2, im[x+1,y+2] + w2 * quant_err);
			set_pixel(im,x+2,y+2, im[x+2,y+2]+ w1 * quant_err);
	return im

def burkes(im):   # stucki algorithm for image dithering
	w8= 8/42.0;
	w4= 4/42.0;
	w2= 2/42.0;
	width,height=im.shape
	for y in range(0,height-2):
		for x in range(0,width-2):
			old_pixel=im[x,y]
			if old_pixel<127:
				new_pixel=0
			else:
				new_pixel=255	
			set_pixel(im,x,y,new_pixel)
			quant_err=old_pixel-new_pixel
			set_pixel(im,x+1,y, im[x+1,y] + w8 * quant_err);
			set_pixel(im,x+2,y, im[x+2,y]+ w4 * quant_err);
			set_pixel(im,x-2,y+1, im[x-2,y+1] + w2 * quant_err);
			set_pixel(im,x-1,y+1, im[x-1,y+1] + w4 * quant_err);
			set_pixel(im,x,y+1, im[x,y+1] + w8 * quant_err);
			set_pixel(im,x+1,y+1, im[x+1,y+1] + w4 * quant_err);
			set_pixel(im,x+2,y+1, im[x+2,y+1] + w2 * quant_err);

	return im

def jjn(im):
	w7= 7/48.0;
	w5= 5/48.0;
	w3=3/48.0;
	w1=1/48.0;
	width,height=im.shape
	for y in range(0,height-2):
		for x in range(0,width-2):
			old_pixel=im[x,y]
			if old_pixel<127:
				new_pixel=0
			else:
				new_pixel=255	
			set_pixel(im,x,y,new_pixel)
			quant_err=old_pixel-new_pixel
			set_pixel(im,x+1,y, im[x+1,y] + w7 * quant_err);
			set_pixel(im,x+2,y, im[x+2,y]+ w5 * quant_err);
			set_pixel(im,x-2,y+1, im[x-2,y+1] + w3 * quant_err);
			set_pixel(im,x-1,y+1, im[x-1,y+1] + w5 * quant_err);
			set_pixel(im,x,y+1, im[x,y+1] + w7 * quant_err);
			set_pixel(im,x+1,y+1, im[x+1,y+1] + w5 * quant_err);
			set_pixel(im,x+2,y+1, im[x+2,y+1] + w3 * quant_err);
			set_pixel(im,x-2,y+2, im[x-2,y+2] + w1 * quant_err);
			set_pixel(im,x-1,y+2, im[x-1,y+2] + w3 * quant_err);
			set_pixel(im,x,y+2, im[x,y+2] + w5 * quant_err);
			set_pixel(im,x+1,y+2, im[x+1,y+2] + w3 * quant_err);
			set_pixel(im,x+2,y+2, im[x+2,y+2]+ w1 * quant_err);
	return im

def sierra(im):
	w5= 5/32.0;
	w4= 4/32.0;
	w3= 3/32.0;
	w2= 2/32.0;
	width,height=im.shape
	for y in range(0,height-2):
		for x in range(0,width-2):
			old_pixel=im[x,y]
			if old_pixel<127:
				new_pixel=0
			else:
				new_pixel=255	
			set_pixel(im,x,y,new_pixel)
			quant_err=old_pixel-new_pixel
			set_pixel(im,x+1,y, im[x+1,y] + w5 * quant_err);
			set_pixel(im,x+2,y, im[x+2,y]+ w3 * quant_err);
			set_pixel(im,x-2,y+1, im[x-2,y+1] + w2 * quant_err);
			set_pixel(im,x-1,y+1, im[x-1,y+1] + w4 * quant_err);
			set_pixel(im,x,y+1, im[x,y+1] + w5 * quant_err);
			set_pixel(im,x+1,y+1, im[x+1,y+1] + w4 * quant_err);
			set_pixel(im,x+2,y+1, im[x+2,y+1] + w2 * quant_err);
			set_pixel(im,x-1,y+2, im[x-1,y+2] + w2 * quant_err);
			set_pixel(im,x,y+2, im[x,y+2] + w3 * quant_err);
			set_pixel(im,x+1,y+2, im[x+1,y+2] + w2 * quant_err);
	return im

def sierratworow(im):
	w4= 4/16.0;
	w3= 3/16.0;
	w2= 2/16.0;
	w1= 1/16.0;
	width,height=im.shape
	for y in range(0,height-2):
		for x in range(0,width-2):
			old_pixel=im[x,y]
			if old_pixel<127:
				new_pixel=0
			else:
				new_pixel=255	
			set_pixel(im,x,y,new_pixel)
			quant_err=old_pixel-new_pixel
			set_pixel(im,x+1,y, im[x+1,y] + w4 * quant_err);
			set_pixel(im,x+2,y, im[x+2,y]+ w3 * quant_err);
			set_pixel(im,x-2,y+1, im[x-2,y+1] + w1 * quant_err);
			set_pixel(im,x-1,y+1, im[x-1,y+1] + w2 * quant_err);
			set_pixel(im,x,y+1, im[x,y+1] + w3 * quant_err);
			set_pixel(im,x+1,y+1, im[x+1,y+1] + w2 * quant_err);
			set_pixel(im,x+2,y+1, im[x+2,y+1] + w1 * quant_err);
	return im

def floyd(inMat, samplingF=1):
    h = inMat.shape[0]
    w = inMat.shape[1]
    for y in range(0, h-1):
        for x in range(1, w-1):
            old_p = inMat[y, x]
            new_p = np.round(samplingF * old_p/255.0) * (255/samplingF)
            inMat[y, x] = new_p   
            quant_error_p = old_p - new_p
            inMat[y, x+1] = minmax(inMat[y, x+1] + quant_error_p * 7 / 16.0)
            inMat[y+1, x-1] = minmax(inMat[y+1, x-1] + quant_error_p * 3 / 16.0)
            inMat[y+1, x] = minmax(inMat[y+1, x] + quant_error_p * 5 / 16.0)
            inMat[y+1, x+1] = minmax(inMat[y+1, x+1] + quant_error_p * 1 / 16.0)
    return inMat

def sierralite(inMat, samplingF=1):
    h = inMat.shape[0]
    w = inMat.shape[1]
    for y in range(0, h-1):
        for x in range(1, w-1):
            old_p = inMat[y, x]
            new_p = np.round(samplingF * old_p/255.0) * (255/samplingF)
            inMat[y, x] = new_p   
            quant_error_p = old_p - new_p
            inMat[y, x+1] = minmax(inMat[y, x+1] + quant_error_p * 2 / 4.0)
            inMat[y+1, x-1] = minmax(inMat[y+1, x-1] + quant_error_p * 1 / 4.0)
            inMat[y+1, x] = minmax(inMat[y+1, x] + quant_error_p * 1 / 4.0)
    return inMat

def false_floyd(inMat, samplingF=1):
    h = inMat.shape[0]
    w = inMat.shape[1]
    for y in range(0, h-1):
        for x in range(1, w-1):
            old_p = inMat[y, x]
            new_p = np.round(samplingF * old_p/255.0) * (255/samplingF)
            inMat[y, x] = new_p   
            quant_error_p = old_p - new_p
            inMat[y, x+1] = minmax(inMat[y, x+1] + quant_error_p * 3 / 8.0)
            inMat[y+1, x] = minmax(inMat[y+1, x] + quant_error_p * 3 / 8.0)
            inMat[y+1, x+1] = minmax(inMat[y+1, x+1] + quant_error_p * 2 / 8.0)
    return inMat