import cv2
from numpy import *
import os, sys


def SaltAndPepper(src, percentage):
    NoiseImg = src
    NoiseNum = int(percentage * src.shape[0] * src.shape[1])
    for i in range(NoiseNum):
        randX = random.random_integers(0, src.shape[0] - 1)
        randY = random.random_integers(0, src.shape[1] - 1)
        if random.random_integers(0, 1) == 0:
            NoiseImg[randX, randY] = 0
        else:
            NoiseImg[randX, randY] = 255
    return NoiseImg


if __name__ == '__main__':
    # source = '/home/tx-eva-12/train'
    source = '/media/tx-eva-21/data/augmentation/Source'
    for file in os.listdir(source):
        img = cv2.imread(source +'/'+file, flags=0)
        gimg = cv2.GaussianBlur(img, (7, 7), sigmaX=0)
        Pers = [0.1, 0.05]
        for i in Pers:
            NoiseImg = SaltAndPepper(gimg, i)
            fileName = file +'_' + str(i) + '.jpg'
            cv2.imwrite(fileName, NoiseImg, [cv2.IMWRITE_JPEG_QUALITY, 100])
