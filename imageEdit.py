#!/usr/bin/env python

"""imageEdit.py: Solves transparency issues regarding UI images for ModuleWorks SampleIntegration.
                 After exporting vector based images to png and filling up the transparent space with the
                 color 255 0 255 (purple) aliased lines appear in a light purple color when showing the image in UI.

                 Here we set a tolerance around 255 0 255 and we search for all the purple similar colors in image and
                 replace them with 255 0 255, so that SI can take out this RGB values and replace them with UI
                 background color. All the ugly purple artifacts disappear. Everybody says WOOHOOO! """

__author__      = "Mathias Rohler"
__copyright__   = "Copyright 2015, ModuleWorks"

import wx, os, sys
# What to do that import of PIL works, when you get the error message that module wasn't found.
# Install PIL and Pillow with an installer of your choice. (easy_install)
# Now import should work
#
# if it doesnt work either we try to find a different solution:
try:
    from PIL import Image
except:
    import Image as Image


def get_file_list():
    # proceed asking to the user the new file to open
    """

    :rtype : list with file names
    """
    openFileDialog = wx.FileDialog(None, "Choose images to adjust", "", "",
                                   "PNG and GIF files (*.png;*.gif)|*.png;*.gif|PNG|*.png|GIF|*.gif|JGP files (*.jpg)|*.jpg",
                                   wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE | wx.FD_PREVIEW)

    if openFileDialog.ShowModal() == wx.ID_OK:
        image_directory = openFileDialog.GetDirectory()
        list_file_name = openFileDialog.GetFilenames()
    else:
        list_file_name = None
        image_directory = None

    return image_directory, list_file_name


def imageCorrection(image_directory, list_file_name):
    # load image from folder
    pulse_dlg = wx.ProgressDialog(title="Adjusting ...",
                                  message="",
                                  maximum=100,
                                  style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME)

    k = 1
    for imagename in list_file_name:

        updmessage = 'Adjusting ... ' + imagename + ' - ' + str(int(round((k / float(len(list_file_name))) * 100))) + ' %'

        (keepGoin, skip) = pulse_dlg.Update(int(round((k / float(len(list_file_name))) * 100)), updmessage)
        if not keepGoin:
            break

        imagebgr = Image.open(image_directory + '\\' + imagename)

        #convert to RGB
        imagebgr = imagebgr.convert('RGB')

        imagebgr.LOAD_TRUNCATED_IMAGES = True
        # load into px var to access coordinates
        px = imagebgr.load()
        # get width and height of image
        (width, height) = imagebgr.size

        # watch out for purple similar pixels and overdraw them ...
        for i in range(0, width):
            for ii in range(0, height):
                RGB = list(px[i, ii])
                if 200 <= RGB[0] <= 255 and 0 <= RGB[1] <= 165 and 245 <= RGB[2] <= 255:
                    imagebgr.putpixel((i, ii), tuple([255, 0, 255]))

        #save
        if not os.path.exists(image_directory + '\\adjusted_images'):
            os.mkdir(image_directory + '\\adjusted_images')
            imagebgr.save(image_directory + '\\adjusted_images\\' + imagename, 'gif')
        else:
            imagebgr.save(image_directory + '\\adjusted_images\\' + imagename, 'gif')

        # replace the 255 0 255 with white pixels 255 255 255 for preview
        for i in range(0, width):
            for ii in range(0, height):
                RGB = list(px[i, ii])
                if RGB == [255, 0, 255]:
                    imagebgr.putpixel((i, ii), tuple([255, 255, 255]))

        #save
        if not os.path.exists(image_directory + '\\adjusted_images\\preview\\'):
            os.mkdir(image_directory + '\\adjusted_images\\preview\\')
            imagebgr.save(image_directory + '\\adjusted_images\\preview\\' + imagename, 'gif')
        else:
            imagebgr.save(image_directory + '\\adjusted_images\\preview\\' + imagename, 'gif')

        k += 1


def main():
    app = wx.PySimpleApp()
    image_directory, list_file_name = get_file_list()
    if list_file_name is not None and image_directory is not None:
        imageCorrection(image_directory, list_file_name)

    os.system('explorer ' + image_directory)


if __name__ == '__main__':
    main()
