import cv2
import sys

filelist = sys.argv[1]


with open(filelist) as f:
	finland_file_list = f.read().splitlines()



for imagePath in finland_file_list:
	print imagePath
	image = cv2.imread(imagePath.rstrip())
	cv2.imshow("Faces found" ,image)
	cv2.waitKey(0)