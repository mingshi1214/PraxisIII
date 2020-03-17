import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('C:/Users/mings/Desktop/reference2.jpg',0)          # queryImage
img2 = cv2.imread('C:/Users/mings/Desktop/matcher.jpg',0) # trainImage

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params,search_params)

matches = flann.knnMatch(des1,des2,k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]
good=[]
# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]
        good.append(m)

draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = 0)

img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

dst_pt = [ kp2[m.trainIdx].pt for m in good]
xsum=0
ysum=0
xmax=0
xmin=100000
ymax=0
ymin=100000
for i in dst_pt:
    xsum=xsum+i[0]
    if i[0]>xmax:
        xmax=i[0]
    if i[0]<xmin:
        xmin=i[0]

    ysum=ysum+i[1]

xave=xsum/len(dst_pt)
yave=ysum/len(dst_pt)

circle1 = plt.Circle((xave, yave), 50, color='red')

plt.imshow(img3,), plt.show(circle1), plt.show()
