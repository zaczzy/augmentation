# Image Augmentation 增强数据
## Description
This script is meant to augment a set of images to a specified amount. It will try to iterate through the set of images in __Source__ and perform some transformations, then save the result into __Augmented__. After one iteration ends, it will restart from the first image again and will not stop until the designated limit is reached. The __tmp__ folder is needed for temporarily saving the transformed image; do not delete it, it will be emptied.
```
    本脚本功能是随机生成增强图片和注释。对图片的更改不大，增强原有数据达到指定目标张数。因对原图产生影响不大，用于均衡数量不平衡标签类用。 之前的使用是人工取出一类标签数据放入Source，用本程序增强到固定数量，再人工拷贝到训练集目录下。
```

The procedure to generate a new image involves three steps.

First step is cropping, the image will either receive no change, a crop from the top, or a crop from the bottom with equal probability. With the top crop mode, the corresponding xml will be changed as well. 上下裁剪

Second step is sharpening, the image will either receive no change, a sharpening filtering, an excessive sharpening filtering, or an edge enhancement filtering with equal probability. Since this transformation does not affect bounding boxes, corresponding xmls are simply copied. 边缘增强，图片锐化

Third step is equalizing histograms, the image's pixel histograms will be equalized with 50% probability.  直方图均衡化
                                      
With each step, the image file's name will be changed, the operation it received will be appended, corresponding xml's name will be changed.

## For Use 使用时
1. Put jpg and annotation files to into the folders under __Source__. Make sure that your images have names with specific suffix: '.jpg', and the annotations have the suffix '.xml". 
```
   源数据请放在Source里，图片放在jpg_data, 注释放在anno里
```

2. Change a few parameters to your need:

    1. In __augment_training_data.py__, set your __augment_limit__, the number of images you want after augmentation.
    ```text
       在augment_training_data.py里，修改augment_limit，它指的是你最后想要图片有多少张。
    ```
    
    2. Optionally, you can change __img_savepath__, __anno_savepath__, __imgset_savepath__, the final location of your augmented JPEG images and XML annotations, and the location of file lists.
    ``` text
        修改最终增强后的三类数据存储路径
    ```
    
    3. You also can change __source_path__, the location you need to put your files before augmentation.

3. Run __augment_training_data.py__, and get your training data folder called __Augmented__. In __Augmented__, images are stored in __JPEGImages__, and annotations are stored in __Annotations__, and the list of all image names are stored in __ImageSets/Main/trainval.txt__.

##For Extension 添加新增强处理
1. The three steps of augmentation are found to work best independently of each other. Therefore, it is better if we do not modify the steps.
    ```
        实验发现前三层增强操作可以进行叠加，而第二层的三种锐化不可相互叠加，结果会不理想，故放在同一层
    ```

2. Here are the general naming preferences of the author:
    ```
        以下为个人命名变量习惯
    ```
_imgp_= the path to the jpeg image to be modified; 、

_xmlp_ = the path to the xml file to be modified;
 
_person_ = _id_ = the name of the file, stripped of suffixes, e.g '10011.jpg' -> '10011'; 

_img_savepath_ = the path to save image; _xml_savepath_ = the path to save xml;

_trainval_ = the text file to write our file list in; 

_code_ = the 3 digit transform code, corresponding to 3 steps of transformation.

3. How the transformation code represent the transformations, see the comments in __augment_training_data.py__.
                            
4. __!__ To add another step of transformation to the augmentation procedure:

    1. Write your own __transform.py__, which should implement an function named __interface__.
    
    ``` python
        def interface(imgp, xmlp, id, img_save, xml_save, mode):
        # mode can be a string of 0, 1, 2. etc to represent a transformation you want to perform
        # make sure to return the path of your new img and xml, and the new id
        # 按照这个格式添加新的增强处理，对于同一处理的不同变种可以放在同一步，例如左裁剪，右裁剪等，在裁剪步中取其一。
        # 变换完成后返回新的文件路径和新的文件名
            return img_save + id + '_new', xml_save + id + '_new', id + new
  
    ```
   2. Modify __generate_transform()__ function in __augment_training_data.py__ to add another transform option with equal probability, or however you want.
    ```
    在随机生成转换码的程序中加一位
    ```
   
   3. Import your file __transform.py__ in __augment_training_data.py__, and modify __transform()__ to call your __transform.interface()__ function giving it the new digit.
   