# import cv2
# import numpy as np
# import imutils
# import csv


# class ColorDescriptor:
#     def __init__(self, bins):
#         # store the number of bins for the 3D histogram
#         self.bins = bins

#     def describe(self, image):
#         # convert the image to the HSV color space and initialize
#         # the features used to quantify the image
#         # print("this is describe function")
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#         features = []
#         # grab the dimensions and compute the center of the image
#         (h, w) = image.shape[:2]
#         (cX, cY) = (int(w * 0.5), int(h * 0.5))
#         # divide the image into four rectangles/segments (top-left,
#         # top-right, bottom-right, bottom-left)
#         segments = [(0, cX, 0, cY), (cX, w, 0, cY),
#                     (cX, w, cY, h), (0, cX, cY, h)]
#         # construct an elliptical mask representing the center of the
#         # image
#         (axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
#         ellipMask = np.zeros(image.shape[:2], dtype="uint8")
#         cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
#         # loop over the segments
#         for (startX, endX, startY, endY) in segments:
#             # construct a mask for each corner of the image, subtracting
#             # the elliptical center from it
#             cornerMask = np.zeros(image.shape[:2], dtype="uint8")
#             cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
#             cornerMask = cv2.subtract(cornerMask, ellipMask)
#             # extract a color histogram from the image, then update the
#             # feature vector
#             hist = self.histogram(image, cornerMask)
#             features.extend(hist)
#         # extract a color histogram from the elliptical region and
#         # update the feature vector
#         hist = self.histogram(image, ellipMask)
#         features.extend(hist)
#         # return the feature vector
#         return features

#     def describe2(self, image):
#         # convert the image to the HSV color space and initialize
#         # the features used to quantify the image
#         # print("this is describe function")
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#         features = []
#         # grab the dimensions and compute the center of the image
#         (h, w) = image.shape[:2]
#         (cX, cY) = (int(w * 0.5), int(h * 0.5))
#         # divide the image into four rectangles/segments (top-left,
#         # top-right, bottom-right, bottom-left)
# # 		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),(0, cX, cY, h)]
#         # construct an elliptical mask representing the center of the
#         # image
#         (axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
#         ellipMask = np.zeros(image.shape[:2], dtype="uint8")
#         cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
#         # loop over the segments
# # 		for (startX, endX, startY, endY) in segments:
# # 			# construct a mask for each corner of the image, subtracting
# # 			# the elliptical center from it
# # 			cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
# # 			cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
# # 			cornerMask = cv2.subtract(cornerMask, ellipMask)
# # 			# extract a color histogram from the image, then update the
# # 			# feature vector
# # 			hist = self.histogram(image, cornerMask)
# # 			features.extend(hist)
#         # extract a color histogram from the elliptical region and
#         # update the feature vector
#         hist = self.histogram(image, ellipMask)
#         features.extend(hist)
#         # return the feature vector
#         return features

#     def histogram(self, image, mask):
#         # extract a 3D color histogram from the masked region of the
#         # image, using the supplied number of bins per channel
#         # print("this is  histogrm class")
#         hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
#                             [0, 180, 0, 256, 0, 256])
#         # normalize the histogram if we are using OpenCV 2.4
#         if imutils.is_cv2():
#             hist = cv2.normalize(hist).flatten()
#         # otherwise handle for OpenCV 3+
#         else:
#             hist = cv2.normalize(hist, hist).flatten()
#         # return the histogram
#         return hist


# # searcher algorithm


# class Searcher:
    
#     def search(self, queryFeatures, imagesData,):
#         results = {}

#         # loop over each document in index collection
#         for row in imagesData:
            
#             features = row["features"]

#             # calculating the distance between user image features and each image features in the db
#             d = self.chi2_distance(features, queryFeatures)

#             # add to the result dictionary (key : image file id, value: distance)
#             results[str(row["image_id"])] = d

#         # sort our results, so that the smaller distances (i.e. the
#         # more relevant images are at the front of the list)
#         results = sorted([(v, k) for (v, k) in results.items()], reverse=True)
        
#         # return results
#         return results

#     def chi2_distance(self, histA, histB, eps=1e-10):
#         # compute the chi-squared distance
#         d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
#                           for (a, b) in zip(histA, histB)])
#         # return the chi-squared distance
#         return d


import cv2
import numpy as np
import imutils
import csv


class ColorDescriptor:
    def __init__(self, bins):
        # store the number of bins for the 3D histogram
        self.bins = bins

    def describe(self, image):
        # convert the image to the HSV color space and initialize
        # the features used to quantify the image
        # print("this is describe function")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []
        # grab the dimensions and compute the center of the image
        (h, w) = image.shape[:2]
        (cX, cY) = (int(w * 0.5), int(h * 0.5))
        # divide the image into four rectangles/segments (top-left,
        # top-right, bottom-right, bottom-left)
        segments = [(0, cX, 0, cY), (cX, w, 0, cY),
                    (cX, w, cY, h), (0, cX, cY, h)]
        # construct an elliptical mask representing the center of the
        # image
        (axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
        ellipMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
        # loop over the segments
        for (startX, endX, startY, endY) in segments:
            # construct a mask for each corner of the image, subtracting
            # the elliptical center from it
            cornerMask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipMask)
            # extract a color histogram from the image, then update the
            # feature vector
            hist = self.histogram(image, cornerMask)
            features.extend(hist)
        # extract a color histogram from the elliptical region and
        # update the feature vector
        hist = self.histogram(image, ellipMask)
        features.extend(hist)
        # return the feature vector
        return features

    def describe2(self, image):
        # convert the image to the HSV color space and initialize
        # the features used to quantify the image
        # print("this is describe function")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []
        # grab the dimensions and compute the center of the image
        (h, w) = image.shape[:2]
        (cX, cY) = (int(w * 0.5), int(h * 0.5))
        # divide the image into four rectangles/segments (top-left,
        # top-right, bottom-right, bottom-left)
# 		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),(0, cX, cY, h)]
        # construct an elliptical mask representing the center of the
        # image
        (axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
        ellipMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
        # loop over the segments
# 		for (startX, endX, startY, endY) in segments:
# 			# construct a mask for each corner of the image, subtracting
# 			# the elliptical center from it
# 			cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
# 			cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
# 			cornerMask = cv2.subtract(cornerMask, ellipMask)
# 			# extract a color histogram from the image, then update the
# 			# feature vector
# 			hist = self.histogram(image, cornerMask)
# 			features.extend(hist)
        # extract a color histogram from the elliptical region and
        # update the feature vector
        hist = self.histogram(image, ellipMask)
        features.extend(hist)
        # return the feature vector
        return features

    def histogram(self, image, mask):
        # extract a 3D color histogram from the masked region of the
        # image, using the supplied number of bins per channel
        # print("this is  histogrm class")
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
                            [0, 180, 0, 256, 0, 256])
        # normalize the histogram if we are using OpenCV 2.4
        if imutils.is_cv2():
            hist = cv2.normalize(hist).flatten()
        # otherwise handle for OpenCV 3+
        else:
            hist = cv2.normalize(hist, hist).flatten()
        # return the histogram
        return hist


# searcher algorithm


class Searcher:
    
    def search(self, queryFeatures, imagesData,):
        results = {}

        # loop over each document in index collection
        for row in imagesData:
            
            features = row["features"]

            # calculating the distance between user image features and each image features in the db
            d = self.chi2_distance(features, queryFeatures)

            # add to the result dictionary (key : image file id, value: distance)
            results[str(row["image_id"])] = d

        # sort our results, so that the smaller distances (i.e. the
        # more relevant images are at the front of the list)
        # sort the dictionary based on the distance values
        results = sorted(results.items(), key=lambda x: x[1])
        
        # return results
        return results

    def chi2_distance(self, histA, histB, eps=1e-10):
        # compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
                          for (a, b) in zip(histA, histB)])
        # return the chi-squared distance
        return d
 