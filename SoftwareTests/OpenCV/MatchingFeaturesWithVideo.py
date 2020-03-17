import numpy as np
import cv2
from matplotlib import pyplot as plt

portImage = cv2.imread('C:/Users/mings/Desktop/reference2.jpg',0)          # queryImage
sceneImage = cv2.imread('C:/Users/mings/Desktop/matcher.jpg',0) # trainImage

surf = cv2.xfeatures2d.SURF_create()
portPoints = surf.DetectAndCompute(portImage, None)
scenePoints = surf.DetectAndCompute(sceneImage, None)

[portFeatures, portPoints] = extractFeatures(portImage, portPoints)
[sceneFeatures, scenePoints] = extractFeatures(sceneImage, scenePoints)

portPairs = matchFeatures(portFeatures, sceneFeatures)

matchedPortPoints = portPoints(portPairs(:, 1), :)
matchedScenePoints = scenePoints(portPairs(:, 2), :)
img3= showMatchedFeatures(portImage, sceneImage, matchedPortPoints, matchedScenePoints, 'montage')

plt.imshow(img3,),plt.show()
