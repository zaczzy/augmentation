from __future__ import division
import cv2
from numpy import *
import os
import shutil as sh


# def adjust_gamma(image, gamma=1.0):
#     invGamma = 1.0 / gamma
#     table = array([((i / 255.0) ** invGamma) * 255 for i in arange(0, 256)]).astype("uint8")
#     return cv2.LUT(image, table)


# 3rd digit. 0: none, 1: equalize histogram
def interface(imgp, xmlp, id, img_save, xml_save, mode):
    img = cv2.imread(imgp)
    if mode == '0':
        cv2.imwrite(img_save + id + '_nohist', img, [cv2.IMWRITE_JPEG_QUALITY, 100])
        sh.copyfile(xmlp, xml_save + id + '_nohist')
        return img_save + id + '_nohist', xml_save + id + '_nohist', id + '_nohist'
    elif mode == '1':
        hist = cv2.equalizeHist(img)
        cv2.imwrite(img_save + id + '_hist', hist, [cv2.IMWRITE_JPEG_QUALITY, 100])
        sh.copyfile(xmlp, xml_save + id + '_hist')
        return img_save + id + '_hist', xml_save + id + '_hist', id + '_hist'
    else:
        raise RuntimeError("WTF")


if __name__ == '__main__':
    # source = '/home/tx-eva-12/train'
    pic = '/media/tx-eva-21/data/augmentation/Source/JPEGImages/'
    xml = '/media/tx-eva-21/data/augmentation/Source/Annotations/'
    for file in os.listdir(pic):
        img = cv2.imread(pic +'/'+file, flags=0)
        Img = cv2.equalizeHist(img)
        cv2.imwrite(pic + file[:-4]+'_hist.jpg', Img, [cv2.IMWRITE_JPEG_QUALITY, 100])
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        # cl1 = clahe.apply(img)
        # cv2.imwrite(pic + file[:-4]+'_clahe.jpg', cl1, [cv2.IMWRITE_JPEG_QUALITY, 100])
        sh.copyfile(xml + file[:-4] + '.xml', xml + file[:-4] + '_hist.xml')
        # sh.copyfile(xml + file[:-4] + '.xml', xml + file[:-4] + '_clahe.xml')

