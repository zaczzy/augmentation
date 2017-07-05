from __future__ import print_function
import os
from itertools import cycle
from collections import defaultdict
from random import randint
from importlib import import_module
import shutil as sh

source_path = os.path.abspath('Source')
imgset_savepath = os.path.abspath('Augmented/ImageSets/Main/')
anno_savepath = '/home/<Username>/PycharmProjects/augmentation/Augmented/Annotations/'
img_savepath = '/home/<Username>/PycharmProjects/augmentation/Augmented/JPEGImages/'

print(os.path.isfile(os.path.join(imgset_savepath, 'trainval.txt')))
trainval = open(os.path.join(imgset_savepath, 'trainval.txt'), 'w')

augment_counter = 0
im_cycle = cycle(os.listdir(os.path.join(source_path, 'jpg_data')))
next_img = next(im_cycle)
next_person = next_img[:-4]
next_xml = next_person + '.xml'
transform_history = defaultdict(set)


# generate a valid random 3 digit transform code, adds it to transform history
# 1st digit. 0: none, 1: crop top, 2: crop bottom
# 2nd digit. 0: none, 1: sharpen, 2; excessive sharpen, 3: edge enhance
# 3rd digit. 0: none, 1: equalize histogram
def generate_transform(person):
    code = str(randint(0, 2)) + str(randint(0, 3)) + str(randint(0, 1))
    while code in transform_history[person]:
        code = str(randint(0, 2)) + str(randint(0, 3)) + str(randint(0, 1))
    transform_history[person].add(code)
    return code


def transform(code, imgp, xmlp, person, img_savepath, anno_savepath, trainval):
    crop = import_module('crop')
    sharpen = import_module('sharpen')
    equal_hist = import_module('equal_hist')
    img_tmp = '/home/zac/PycharmProjects/augmentation/tmp/jpg_data/'
    xml_tmp = '/home/zac/PycharmProjects/augmentation/tmp/anno/'
    imgp, xmlp, id = crop.interface(imgp, xmlp, person, img_tmp, xml_tmp, code[0])
    imgp, xmlp, id = sharpen.interface(imgp, xmlp, id, img_tmp, xml_tmp, code[1])
    _, _, id = equal_hist.interface(imgp, xmlp, id, img_savepath, anno_savepath, code[2])
    trainval.write(id + '\n')
    print(code, id)

while augment_counter < 40:
    # get transform code
    transform_code = generate_transform(next_person)
    # get img array and xml
    imgp = os.path.join(os.path.join(source_path, 'jpg_data'), next_img)
    xmlp = os.path.join(os.path.join(source_path, 'anno'), next_xml)
    # transform the img and xml according to transform code
    # save the img and xml in save path
    transform(transform_code, imgp, xmlp, next_person, img_savepath, anno_savepath, trainval)
    sh.rmtree('tmp')
    os.mkdir('tmp')
    os.mkdir('tmp/jpg_data')
    os.mkdir('tmp/anno')
    next_img = next(im_cycle)
    next_person = next_img[:-4]
    next_xml = next_person + '.xml'
    
    augment_counter += 1
trainval.close()
