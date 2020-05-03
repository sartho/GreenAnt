import numpy as np
import cv2
import os
import imutils

class IMGresizer(object):
	"""docstring for ClassName"""
	def __init__(self,size,fileloc,arg):
		super(IMGresizer, self).__init__()
		self.size=size
		self.arg=arg
		self.fileloc=fileloc

	def ReSize(self):
		for arg in self.arg:
			imgloc=self.fileloc+arg
			fl_nm=os.path.splitext(imgloc)[0]+'_'+str(self.size)+'.jpg'
			cv2.imwrite(fl_nm,self.ResizeIMG(imgloc))
			print (arg)

	def ResizeIMG(self,imgloc):
		img=cv2.imread(imgloc, cv2.IMREAD_UNCHANGED)

		ht_rt=round(self.size/img.shape[0],3)
		wd_rt=round(self.size/img.shape[1],3)
			
		if ht_rt<=wd_rt:
			scale=ht_rt

		else: 
			scale=wd_rt

		width=int(img.shape[1] * scale)
		height=int(img.shape[0] * scale)
		dim = (width, height)

		resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

		row=(abs((self.size-height)/2))
		col= (abs((self.size-width)/2))

		M=np.float32([[1,0,col],[0,1,row]])
		return cv2.warpAffine(resized,M,(self.size,self.size))
		#return resized

	def GetIMG(self):
		fl_nm=(self.fileloc).strip('.jpg')+'_'+str(self.size)+'.jpg'
		cv2.imwrite(fl_nm,self.ResizeIMG(self.fileloc))
		fl_nm=fl_nm.split('/')[-1]
		return fl_nm

	def CropIMG(self,image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		#gray = cv2.GaussianBlur(gray, (5, 5), 0)
		# threshold the image, then perform a series of erosions +
		# dilations to remove any small regions of noise
		thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1]
		#return gray
		thresh = cv2.erode(thresh, None, iterations=2)
		thresh = cv2.dilate(thresh, None, iterations=2)
		# find contours in thresholded image, then grab the largest
		# one
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		c = max(cnts, key=cv2.contourArea)
				# determine the most extreme points along the contour
		extLeft = tuple(c[c[:, :, 0].argmin()][0])
		extRight = tuple(c[c[:, :, 0].argmax()][0])
		extTop = tuple(c[c[:, :, 1].argmin()][0])
		extBot = tuple(c[c[:, :, 1].argmax()][0])
		# draw the outline of the object, then draw each of the
		# extreme points, where the left-most is red, right-most
		# is green, top-most is blue, and bottom-most is teal
		cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
		cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
		cv2.circle(image, extRight, 8, (0, 255, 0), -1)
		cv2.circle(image, extTop, 8, (255, 0, 0), -1)
		cv2.circle(image, extBot, 8, (255, 255, 0), -1)

		return image

#arg=['admin.jpg','1.jpeg','2.png','3.jpeg','4.jpg','5.jpeg','6.jpg','7.jpeg']
arg=['admin.jpg']
IMG=IMGresizer(2000,'./static/DPs/',arg)
dst=IMG.ResizeIMG('./static/DPs/'+arg[0])

est=IMG.CropIMG(IMG)

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow('img',est)
cv2.waitKey(0)
cv2.destroyAllWindows()