import os
import shutil as sh
import xml.etree.ElementTree as ET
import cv2
yMin = 3000
yMax = 0

# 1st digit. 0: none, 1: crop top, 2: crop bottom
def interface(imgp, xmlp, id, img_save, xml_save, mode):
    if mode == '0':
        img = cv2.imread(imgp)
        cv2.imwrite(img_save + id + '_nocrop', img, [cv2.IMWRITE_JPEG_QUALITY, 100])
        sh.copyfile(xmlp, xml_save + id + '_nocrop')
        return img_save + id + '_nocrop', xml_save + id + '_nocrop', id + '_nocrop'
    elif mode == '1':
        return crop(imgp, xmlp, id, img_save, xml_save, True)
    elif mode == '2':
        return crop(imgp, xmlp, id, img_save, xml_save, False)
    else:
        raise RuntimeError('WTF')



def crop(imgp, xmlp, id, img_save, xml_save, top_crop):
    global yMax, yMin
    tree = ET.parse(xmlp)
    objs = tree.findall('object')
    for obj in objs:
        ymin = int(obj.find('bndbox').find('ymin').text)
        ymax = int(obj.find('bndbox').find('ymax').text)
        yMin = ymin if ymin < yMin else yMin
        yMax = ymax if ymax > yMax else yMax
    img = cv2.imread(imgp)
    height, width, _ = img.shape
    crop_img = img
    if top_crop:
        crop_img = img[yMin / 2: height, 0: width].copy()
    else:
        crop_img = img[0:(height + yMax) / 2, 0:width].copy()
    img_savep = img_save + id + '_crop_' + str(top_crop).lower()
    cv2.imwrite(img_savep, crop_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
    xml_savep = xml_save + id + '_crop_' + str(top_crop).lower()
    sh.copyfile(xmlp, xml_savep)
    if top_crop:
        tree = ET.parse(xml_savep)
        objs = tree.findall('object')
        for obj in objs:
            obj.find('bndbox').find('ymax').text = str(int(obj.find('bndbox').find('ymax').text) - (yMin / 2))
            obj.find('bndbox').find('ymin').text = str(int(obj.find('bndbox').find('ymin').text) - (yMin / 2))
        tree.write(xml_savep)
    return img_savep, xml_savep, id + '_crop_' + str(top_crop).lower()





if __name__ == '__main__':
    # source = '/home/tx-eva-12/train'
    user = '/home/zac/PycharmProjects/'
    pic = user + 'augmentation/Source/jpg_data/'
    xml = user + 'augmentation/Source/anno/'
    for xl in os.listdir(xml):
        imgp = pic + xl[:-4] + '.jpg'
        xmlp = xml + xl
        id = xl[:-4]
        top_crop = False
        for i in range(2):
            print crop(imgp, xmlp, id, pic, xml, top_crop)
            top_crop = not top_crop
