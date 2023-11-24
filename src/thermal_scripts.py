#!/usr/bin/env python
import sys, traceback
import cv2
import numpy as np
import argparse
import string
from plantcv import plantcv as pcv

### Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r","--result", help="result file.", required= False )
    parser.add_argument("-w","--writeimg", help="write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug", help="can be set to 'print' or None (or 'plot' if in jupyter) prints intermediate images.", default=None)
    args = parser.parse_args()
    return args

def get_mask_from_file(filedir):
   img, path, filename = pcv.readimage(filename=filedir)
   converted_img = cv2.resize(img, dsize=(320, 240), interpolation=cv2.INTER_CUBIC)
   mask, masked_img = pcv.threshold.custom_range(img=converted_img, lower_thresh=[0,0,0], upper_thresh=[250,50,100], channel='RGB')
   #thresh1 = pcv.threshold.dual_channels(rgb_img = converted_img, x_channel = "a", y_channel = "b", points = [(0, 0), (200, 200)], above=True)
   print(converted_img.shape)
   #a_fill_image = pcv.fill(bin_img=thresh1, size=50)
   #print(a_fill_image)
   #a_fill_image = pcv.fill_holes(a_fill_image)
   #roi1 = pcv.roi.rectangle(img=converted_img, x=10, y=30, h=100, w=200)
   #kept_mask  = pcv.roi.filter(mask=a_fill_image, roi=roi1, roi_type='partial')
   return mask

### Main workflow
def main():
    # Get options
    args = options()

    pcv.params.debug=args.debug #set debug mode
    pcv.params.debug_outdir=args.outdir #set output directory

    # Read raw thermal data

    # Inputs:
    #   filename - Image file to be read (possibly including a path)
    #   mode - Return mode of image ("native," "rgb,", "rgba", "gray", or "flir"), defaults to "native"
    thermal_data,path,filename = pcv.readimage(filename="./inputdir/G_A0_2.csv", mode="csv")


    # Rescale the thermal data to a colorspace with range 0-255

    # Inputs:
    #   gray_img - Grayscale image data
    #   min_value - New minimum value for range of interest. default = 0
    #   max_value - New maximum value for range of interest. default = 255
    scaled_thermal_img = pcv.transform.rescale(gray_img=thermal_data)


    # Threshold the thermal data to make a binary mask

    # Inputs:
    #   gray_img - Grayscale image data
    #   threshold- Threshold value (between 0-255)
    #   max_value - Value to apply above threshold (255 = white)
    #   object_type - 'light' (default) or 'dark'. If the object is lighter than the background then standard
    #                 threshold is done. If the object is darker than the background then inverse thresholding is done.
    bin_mask = pcv.threshold.binary(gray_img=thermal_data, threshold=25, object_type='dark')


    # Identify objects

    # Inputs:
    #   img - RGB or grayscale image data for plotting
    #   mask - Binary mask used for detecting contours
    #id_objects, obj_hierarchy = pcv.find_objects(img=scaled_thermal_img, mask=bin_mask)


    # Define the region of interest (ROI)

    # Inputs:
    #   img - RGB or grayscale image to plot the ROI on
    #   x - The x-coordinate of the upper left corner of the rectangle
    #   y - The y-coordinate of the upper left corner of the rectangle
    #   h - The height of the rectangle
    #   w - The width of the rectangle
    shape = scaled_thermal_img.shape
    print(shape)
    roi = pcv.roi.rectangle(img=scaled_thermal_img, x=0, y=128, h=64, w=64)

    mask = pcv.roi.filter(mask=bin_mask, roi=roi, roi_type="cutto")
    ##mask = get_mask_from_file("./inputdir/G_A0_2.jpg")
    print(roi)
    print(mask.shape)
    print(thermal_data.shape)
    # Decide which objects to keep

    # Inputs:
    #   img - RGB or grayscale image data to display kept objects on
    #   roi_contour - contour of ROI, output from pcv.roi.rectangle in this case
    #   object_contour - Contour of objects, output from pcv.roi.rectangle in this case
    #   obj_hierarchy - Hierarchy of objects, output from pcv.find_objects function
    #   roi_type - 'partial' (for partially inside, default), 'cutto', or 'largest' (keep only the largest contour)


    #roi_objects, hierarchy, kept_mask, obj_area = pcv.roi_objects(img=scaled_thermal_img,roi_contour=roi,
    #                                                              roi_hierarchy=roi_hierarchy,
    #                                                              object_contour=id_objects,
    #                                                              obj_hierarchy=obj_hierarchy,
    #                                                              roi_type='cutto')


    ##### Analysis #####

    # Analyze thermal data

    # Inputs:
    #   img - Array of thermal values
    #   mask - Binary mask made from selected contours
    #   histplot - If True plots histogram of intensity values (default histplot = False)
    #   label - Optional label parameter, modifies the variable name of observations recorded
    #analysis_img = pcv.analyze_thermal_values(thermal_array=thermal_data, mask=bin_mask, histplot=True, label="default")

    analysis_img = pcv.analyze.thermal(thermal_img=thermal_data, labeled_mask=mask, n_labels=1, bins=10, label="default")
    # Pseudocolor the thermal data

    # Inputs:
    #     gray_img - Grayscale image data
    #     obj - Single or grouped contour object (optional), if provided the pseudocolored image gets
    #           cropped down to the region of interest.
    #     mask - Binary mask (optional)
    #     background - Background color/type. Options are "image" (gray_img, default), "white", or "black". A mask
    #                  must be supplied.
    #     cmap - Colormap
    #     min_value - Minimum value for range of interest
    #     max_value - Maximum value for range of interest
    #     dpi - Dots per inch for image if printed out (optional, if dpi=None then the default is set to 100 dpi).
    #     axes - If False then the title, x-axis, and y-axis won't be displayed (default axes=True).
    #     colorbar - If False then the colorbar won't be displayed (default colorbar=True)
    #pseudo_img = pcv.visualize.pseudocolor(gray_img = thermal_data, mask=kept_mask, cmap='viridis',
    #                                       min_value=31, max_value=35)
    pseudo_img = pcv.visualize.pseudocolor(gray_img = thermal_data, mask=mask, cmap='jet', min_value=16, max_value=30)
    # Write shape and thermal data to results file
    pcv.outputs.save_results(filename="therm_res")
    #pcv.print_results(filename=args.result)
    outdir = str(args.outdir) + "/tutorial.png"
    print(outdir)
    pcv.print_image(img=pseudo_img, filename= outdir)
if __name__ == '__main__':
    main()
