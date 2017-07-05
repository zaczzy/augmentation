# Image Augmentation
## Description
This script is meant to augment a set of images to a specified amount. It will try to iterate through the set of images in __Source__ and perform some transformations, then save the result into __Augmented__. After one iteration ends, it will restart from the first image again and will not stop until designated limit is reached. The __tmp__ folder is needed for temporarily saving the transformed image, do not delete it, it will be emptied.

The procedure to generate a new image involves three steps.

First step is cropping, the image will either receive no change, a crop from the top, or a top from the bottom uniformly randomly. With the top crop mode, the corresponding xml will be changed as well.

Second step is sharpening, the image will either receive no change, a sharpening filtering, an excessive sharpening filtering, or an edge enhancement filtering uniformly randomly. Since this transformation does not affect bounding boxes, corresponding xmls are simply copied.

Third step is equalizing histograms, the image's pixel histograms will be equalized with 50% probability.

With each step, the image file's name will be changed, it will be appended the operation it received, corresponding xml's name will be changed.

## For Use
1. Put jpg and annotation files to into the folders under __Source__. Make sure that your images have names with specific suffix: '.jpg', and the annotations have the suffix '.xml".

2. Change a few parameters to your need:

    1. In __augment_training_data.py__, set your __augment_limit__, the number of images you want after augmentation.
    
    2. Optionally, you can change __img_savepath__, __anno_savepath__, the final location of your augmented JPEG images and XML annotations.
    
    3. You also can change __source_path__, the location you need to put your files before augmentation.

3. Run __augment_training_data.py__, and get your training data folder called __Augmented__. In __Augmented__, images are stored in __JPEGImages__, and annotations are stored in __Annotations__, and the list of all image names are stored in __ImageSets/Main/trainval.txt__.

##For Extension
1. The three steps of augmentation are found to be best independent of each other. Therefore, it is better if we do not modify the steps.

2. Here are the general naming preferences of the author: 
_imgp_= the path to the jpeg image to be modified; 
_xmlp_ = the path to the xml file to be modified; 
_person_ = _id_ = the name of the file, stripped of suffixes, e.g '10011.jpg' -> '10011'; 
_img_savepath_ = the path to save image; _xml_savepath_ = the path to save xml;
_trainval_ = the text file to write our file list in; 
_code_ = the 3 digit transform code, corresponding to 3 steps of transformation.

3. How the transformation code represent the transformations, see the comments in __augment_training_data.py__.
                            
4. __!__ To add another step of transformation to the augmentation procedure:

    1. Write your own __transform.py__, which should implement an function named __interface__.
    
    ``` 
        def interface(imgp, xmlp, id, img_save, xml_save, mode):
        # mode can be a string of 0, 1, 2. etc to represent a transformation you want to perform
        # make sure to return the path of your new img and xml, and the new id
            return img_save + id + '_new', xml_save + id + '_new', id + new
  
    ```
   2. Modify __generate_transform()__ function in __augment_training_data.py__ to generate another digit of transform code uniformly, or however you want.
   
   3. Import your file __transform.py__, and modify __transform()__ to call your __transform.interface()__ function giving it the new digit.