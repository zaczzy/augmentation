from __future__ import division
import cv2
import numpy as np
import os
import shutil as sh

pic = '/media/tx-eva-21/data/augmentation/Source/JPEGImages/'
xml = '/media/tx-eva-21/data/augmentation/Source/Annotations/'
kernel_sharpen = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
kernel_excess = np.array([[1, 1, 1], [1, -7, 1], [1, 1, 1]])
kernel_edge = np.array([[-1, -1, -1, -1, -1],
                             [-1, 2, 2, 2, -1],
                             [-1, 2, 8, 2, -1],
                             [-1, 2, 2, 2, -1],
                             [-1, -1, -1, -1, -1]]) / 8.0

# 2nd digit. 0: none, 1: sharpen, 2; excessive sharpen, 3: edge enhance
def interface(imgp, xmlp, id, img_save, xml_save, mode):
    img = cv2.imread(imgp)
    if mode == '0':
        cv2.imwrite(img_save + id + '_nosharpen', img, [cv2.IMWRITE_JPEG_QUALITY, 100])
        sh.copyfile(xmlp, xml_save + id + '_nosharpen')
        return img_save + id + '_nosharpen', xml_save + id + '_nosharpen', id + '_nosharpen'
    elif mode == '1':
        sharpened = cv2.filter2D(img, -1, kernel_sharpen)
        cv2.imwrite(img_save + id + '_sharpen', sharpened, [cv2.IMWRITE_JPEG_QUALITY, 100])
        sh.copyfile(xmlp, xml_save + id + '_sharpen')
        return img_save + id + '_sharpen', xml_save + id + '_sharpen', id + '_sharpen'
    elif mode == '2':
        excess = cv2.filter2D(img, -1, kernel_excess)
        cv2.imwrite(img_save + id + '_excess', excess, [cv2.IMWRITE_JPEG_QUALITY, 100])
        sh.copyfile(xmlp, xml_save + id + '_excess')
        return img_save + id + '_excess', xml_save + id + '_excess', id + '_excess'
    elif mode == '3':
        edge = cv2.filter2D(img, -1, kernel_edge)
        cv2.imwrite(img_save + id + '_edge', edge, [cv2.IMWRITE_JPEG_QUALITY, 100])
        sh.copyfile(xmlp, xml_save + id + '_edge')
        return img_save + id + '_edge', xml_save + id + '_edge', id + '_edge'
    else:
        raise RuntimeError('WTF')

if __name__ == '__main__':
    for img in os.listdir(pic):
        person = img[:-4]
        img = cv2.imread(pic + img)
        # cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Original', 800, 800)
        # cv2.imshow('Original', img)
        output_1 = cv2.filter2D(img, -1, kernel_sharpen)
        cv2.imwrite(pic + person + '_sharpen' + '.jpg', output_1, [cv2.IMWRITE_JPEG_QUALITY, 100])
        # cv2.namedWindow('Sharpening', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Sharpening', 800, 800)
        # cv2.imshow('Sharpening', output_1)
        sh.copyfile(xml + person + '.xml', xml + person + '_sharpen.xml')



